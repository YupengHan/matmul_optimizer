#pragma once

#include <cstdint>

#include <cuda_runtime_api.h>

namespace matmul_optimizer {

// All pointers are device pointers to row-major BF16 payloads stored as raw uint16_t bits.
bool launch_bf16_gemm_v1(
    const std::uint16_t* a_bf16,
    const std::uint16_t* b_bf16,
    std::uint16_t* c_bf16,
    int m,
    int n,
    int k,
    cudaStream_t stream);

}  // namespace matmul_optimizer
