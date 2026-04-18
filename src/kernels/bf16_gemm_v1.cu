#include "kernel_api.h"

#include <cuda_bf16.h>
#include <cuda_runtime.h>

namespace matmul_optimizer {
namespace {

constexpr int kTileM = 16;
constexpr int kTileN = 16;
constexpr int kTileK = 16;

// v1 placeholder kernel:
// - plain shared-memory tiled GEMM
// - BF16 inputs, FP32 accumulation, BF16 output
// - prioritizes a stable callable interface over performance work
__global__ void bf16_gemm_v1_kernel(
    const __nv_bfloat16* a,
    const __nv_bfloat16* b,
    __nv_bfloat16* c,
    int m,
    int n,
    int k) {
  __shared__ float a_tile[kTileM][kTileK];
  __shared__ float b_tile[kTileK][kTileN];

  const int row = blockIdx.y * kTileM + threadIdx.y;
  const int col = blockIdx.x * kTileN + threadIdx.x;

  float acc = 0.0f;

  for (int tile_k = 0; tile_k < k; tile_k += kTileK) {
    const int a_col = tile_k + threadIdx.x;
    const int b_row = tile_k + threadIdx.y;

    a_tile[threadIdx.y][threadIdx.x] =
        (row < m && a_col < k) ? __bfloat162float(a[row * k + a_col]) : 0.0f;
    b_tile[threadIdx.y][threadIdx.x] =
        (b_row < k && col < n) ? __bfloat162float(b[b_row * n + col]) : 0.0f;

    __syncthreads();

    #pragma unroll
    for (int kk = 0; kk < kTileK; ++kk) {
      acc += a_tile[threadIdx.y][kk] * b_tile[kk][threadIdx.x];
    }

    __syncthreads();
  }

  if (row < m && col < n) {
    c[row * n + col] = __float2bfloat16(acc);
  }
}

}  // namespace

bool launch_bf16_gemm_v1(
    const std::uint16_t* a_bf16,
    const std::uint16_t* b_bf16,
    std::uint16_t* c_bf16,
    int m,
    int n,
    int k,
    cudaStream_t stream) {
  if (a_bf16 == nullptr || b_bf16 == nullptr || c_bf16 == nullptr) {
    return false;
  }
  if (m <= 0 || n <= 0 || k <= 0) {
    return false;
  }

  const dim3 block(kTileN, kTileM);
  const dim3 grid((n + kTileN - 1) / kTileN, (m + kTileM - 1) / kTileM);

  bf16_gemm_v1_kernel<<<grid, block, 0, stream>>>(
      reinterpret_cast<const __nv_bfloat16*>(a_bf16),
      reinterpret_cast<const __nv_bfloat16*>(b_bf16),
      reinterpret_cast<__nv_bfloat16*>(c_bf16),
      m,
      n,
      k);

  return cudaGetLastError() == cudaSuccess;
}

}  // namespace matmul_optimizer
