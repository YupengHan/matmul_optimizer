#include "runner_contract.h"

#include <array>
#include <cuda_bf16.h>
#include <cuda_runtime.h>
#include <cublasLt.h>
#include <cublas_v2.h>

#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <optional>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace fs = std::filesystem;

namespace matmul_optimizer {
namespace {

struct RunnerArgs {
  fs::path dataset_dir;
  std::string case_id;
  RunnerMode mode = RunnerMode::kCorrectness;
  int warmup = 0;
  int iters = 1;
  int flush_cache_mb = 0;
  int algo_index = 0;
  std::optional<fs::path> json_out;
};

struct CaseSpec {
  fs::path case_dir;
  fs::path a_bf16_path;
  fs::path b_bf16_path;
  fs::path c_ref_fp32_path;
  fs::path c_ref_bf16_path;
  int m = 0;
  int n = 0;
  int k = 0;
  double atol = 0.15;
  double rtol = 0.01;
};

void require(bool condition, const std::string& message) {
  if (!condition) {
    throw std::runtime_error(message);
  }
}

void check_cuda(cudaError_t status, const std::string& context) {
  if (status != cudaSuccess) {
    throw std::runtime_error(context + ": " + cudaGetErrorString(status));
  }
}

void check_cublas(cublasStatus_t status, const std::string& context) {
  if (status != CUBLAS_STATUS_SUCCESS) {
    std::ostringstream message;
    message << context << ": cuBLAS status " << static_cast<int>(status);
    throw std::runtime_error(message.str());
  }
}

std::string read_text_file(const fs::path& path) {
  std::ifstream input(path);
  require(input.is_open(), "failed to open text file: " + path.string());

  std::ostringstream buffer;
  buffer << input.rdbuf();
  return buffer.str();
}

int extract_json_int(const std::string& text, const std::string& key) {
  const std::string needle = "\"" + key + "\"";
  const auto key_pos = text.find(needle);
  require(key_pos != std::string::npos, "missing integer key in JSON: " + key);

  const auto colon_pos = text.find(':', key_pos + needle.size());
  require(colon_pos != std::string::npos, "missing ':' for JSON key: " + key);

  const auto value_pos = text.find_first_of("-0123456789", colon_pos + 1);
  require(value_pos != std::string::npos, "missing integer value for JSON key: " + key);

  std::size_t consumed = 0;
  return std::stoi(text.substr(value_pos), &consumed);
}

double extract_json_double_or_default(const std::string& text, const std::string& key, double default_value) {
  const std::string needle = "\"" + key + "\"";
  const auto key_pos = text.find(needle);
  if (key_pos == std::string::npos) {
    return default_value;
  }

  const auto colon_pos = text.find(':', key_pos + needle.size());
  if (colon_pos == std::string::npos) {
    return default_value;
  }

  const auto value_pos = text.find_first_of("-0123456789.", colon_pos + 1);
  if (value_pos == std::string::npos) {
    return default_value;
  }

  std::size_t consumed = 0;
  return std::stod(text.substr(value_pos), &consumed);
}

RunnerMode parse_mode(const std::string& value) {
  if (value == "correctness") {
    return RunnerMode::kCorrectness;
  }
  if (value == "perf") {
    return RunnerMode::kPerf;
  }
  throw std::runtime_error("unsupported --mode value: " + value);
}

std::string mode_to_string(RunnerMode mode) {
  return mode == RunnerMode::kCorrectness ? "correctness" : "perf";
}

RunnerArgs parse_args(int argc, char** argv) {
  RunnerArgs args;

  for (int i = 1; i < argc; ++i) {
    const std::string arg = argv[i];
    const auto next_value = [&](const std::string& name) -> std::string {
      require(i + 1 < argc, "missing value for " + name);
      return argv[++i];
    };

    if (arg == "--dataset-dir") {
      args.dataset_dir = next_value(arg);
    } else if (arg == "--case-id") {
      args.case_id = next_value(arg);
    } else if (arg == "--mode") {
      args.mode = parse_mode(next_value(arg));
    } else if (arg == "--warmup") {
      args.warmup = std::stoi(next_value(arg));
    } else if (arg == "--iters") {
      args.iters = std::stoi(next_value(arg));
    } else if (arg == "--flush-cache-mb") {
      args.flush_cache_mb = std::stoi(next_value(arg));
    } else if (arg == "--algo-index") {
      args.algo_index = std::stoi(next_value(arg));
    } else if (arg == "--json-out") {
      args.json_out = fs::path(next_value(arg));
    } else {
      throw std::runtime_error("unknown argument: " + arg);
    }
  }

  require(!args.dataset_dir.empty(), "--dataset-dir is required");
  require(!args.case_id.empty(), "--case-id is required");
  require(args.warmup >= 0, "--warmup must be >= 0");
  require(args.iters > 0, "--iters must be > 0");
  require(args.flush_cache_mb >= 0, "--flush-cache-mb must be >= 0");
  require(args.algo_index >= 0, "--algo-index must be >= 0");

  return args;
}

CaseSpec load_case_spec(const fs::path& dataset_dir, const std::string& case_id) {
  const fs::path case_dir = dataset_dir / "cases" / case_id;
  const fs::path meta_path = case_dir / "meta.json";
  const fs::path manifest_path = dataset_dir / "manifest.json";

  require(fs::exists(case_dir), "case directory not found: " + case_dir.string());
  require(fs::exists(meta_path), "case meta.json not found: " + meta_path.string());

  const std::string meta_text = read_text_file(meta_path);

  CaseSpec spec;
  spec.case_dir = case_dir;
  spec.a_bf16_path = case_dir / "A.bf16.bin";
  spec.b_bf16_path = case_dir / "B.bf16.bin";
  spec.c_ref_fp32_path = case_dir / "C_ref_fp32.bin";
  spec.c_ref_bf16_path = case_dir / "C_ref_bf16.bin";
  spec.m = extract_json_int(meta_text, "m");
  spec.n = extract_json_int(meta_text, "n");
  spec.k = extract_json_int(meta_text, "k");

  if (fs::exists(manifest_path)) {
    const std::string manifest_text = read_text_file(manifest_path);
    spec.atol = extract_json_double_or_default(manifest_text, "initial_atol", spec.atol);
    spec.rtol = extract_json_double_or_default(manifest_text, "initial_rtol", spec.rtol);
  }

  return spec;
}

template <typename T>
std::vector<T> read_binary_file(const fs::path& path, std::size_t expected_count) {
  require(fs::exists(path), "binary file not found: " + path.string());

  const auto expected_bytes = static_cast<std::uintmax_t>(expected_count * sizeof(T));
  require(fs::file_size(path) == expected_bytes, "unexpected binary size for " + path.string());

  std::vector<T> values(expected_count);
  std::ifstream input(path, std::ios::binary);
  require(input.is_open(), "failed to open binary file: " + path.string());

  input.read(reinterpret_cast<char*>(values.data()), static_cast<std::streamsize>(expected_bytes));
  require(input.good(), "failed to read binary file: " + path.string());

  return values;
}

float bf16_bits_to_float(std::uint16_t bits) {
  const std::uint32_t widened = static_cast<std::uint32_t>(bits) << 16;
  float value = 0.0f;
  std::memcpy(&value, &widened, sizeof(value));
  return value;
}

template <typename T>
class DeviceBuffer {
 public:
  DeviceBuffer() = default;

  explicit DeviceBuffer(std::size_t count)
      : count_(count) {
    if (count_ == 0) {
      return;
    }
    check_cuda(cudaMalloc(&ptr_, count_ * sizeof(T)), "cudaMalloc");
  }

  ~DeviceBuffer() {
    if (ptr_ != nullptr) {
      cudaFree(ptr_);
    }
  }

  DeviceBuffer(const DeviceBuffer&) = delete;
  DeviceBuffer& operator=(const DeviceBuffer&) = delete;

  T* get() {
    return static_cast<T*>(ptr_);
  }

  const T* get() const {
    return static_cast<const T*>(ptr_);
  }

  std::size_t bytes() const {
    return count_ * sizeof(T);
  }

 private:
  void* ptr_ = nullptr;
  std::size_t count_ = 0;
};

class StreamGuard {
 public:
  StreamGuard() {
    check_cuda(cudaStreamCreate(&stream_), "cudaStreamCreate");
  }

  ~StreamGuard() {
    if (stream_ != nullptr) {
      cudaStreamDestroy(stream_);
    }
  }

  StreamGuard(const StreamGuard&) = delete;
  StreamGuard& operator=(const StreamGuard&) = delete;

  cudaStream_t get() const {
    return stream_;
  }

 private:
  cudaStream_t stream_ = nullptr;
};

class EventGuard {
 public:
  EventGuard() {
    check_cuda(cudaEventCreate(&event_), "cudaEventCreate");
  }

  ~EventGuard() {
    if (event_ != nullptr) {
      cudaEventDestroy(event_);
    }
  }

  EventGuard(const EventGuard&) = delete;
  EventGuard& operator=(const EventGuard&) = delete;

  cudaEvent_t get() const {
    return event_;
  }

 private:
  cudaEvent_t event_ = nullptr;
};

class CublasHandleGuard {
 public:
  CublasHandleGuard() {
    check_cublas(cublasCreate(&handle_), "cublasCreate");
  }

  ~CublasHandleGuard() {
    if (handle_ != nullptr) {
      cublasDestroy(handle_);
    }
  }

  CublasHandleGuard(const CublasHandleGuard&) = delete;
  CublasHandleGuard& operator=(const CublasHandleGuard&) = delete;

  cublasHandle_t get() const {
    return handle_;
  }

 private:
  cublasHandle_t handle_ = nullptr;
};

class CublasLtHandleGuard {
 public:
  CublasLtHandleGuard() {
    check_cublas(cublasLtCreate(&handle_), "cublasLtCreate");
  }

  ~CublasLtHandleGuard() {
    if (handle_ != nullptr) {
      cublasLtDestroy(handle_);
    }
  }

  CublasLtHandleGuard(const CublasLtHandleGuard&) = delete;
  CublasLtHandleGuard& operator=(const CublasLtHandleGuard&) = delete;

  cublasLtHandle_t get() const {
    return handle_;
  }

 private:
  cublasLtHandle_t handle_ = nullptr;
};

constexpr std::size_t kCublasLtWorkspaceBytes = 64ULL * 1024ULL * 1024ULL;
constexpr int kLtRequestedHeuristicCount = 16;

class LtMatmulPlan {
 public:
  LtMatmulPlan(cublasLtHandle_t handle, int m, int n, int k, int algo_index)
      : workspace_(kCublasLtWorkspaceBytes) {
#if defined(CUBLAS_COMPUTE_32F_FAST_16BF)
    constexpr cublasComputeType_t kComputeType = CUBLAS_COMPUTE_32F_FAST_16BF;
#else
    constexpr cublasComputeType_t kComputeType = CUBLAS_COMPUTE_32F;
#endif
    constexpr cudaDataType_t kDataType = CUDA_R_16BF;
    constexpr cudaDataType_t kScaleType = CUDA_R_32F;
    constexpr cublasOperation_t kNoTranspose = CUBLAS_OP_N;
    constexpr cublasLtOrder_t kRowMajor = CUBLASLT_ORDER_ROW;

    check_cublas(cublasLtMatmulDescCreate(&operation_desc_, kComputeType, kScaleType),
                 "cublasLtMatmulDescCreate");
    check_cublas(cublasLtMatmulDescSetAttribute(
                     operation_desc_,
                     CUBLASLT_MATMUL_DESC_TRANSA,
                     &kNoTranspose,
                     sizeof(kNoTranspose)),
                 "cublasLtMatmulDescSetAttribute transa");
    check_cublas(cublasLtMatmulDescSetAttribute(
                     operation_desc_,
                     CUBLASLT_MATMUL_DESC_TRANSB,
                     &kNoTranspose,
                     sizeof(kNoTranspose)),
                 "cublasLtMatmulDescSetAttribute transb");

    check_cublas(cublasLtMatrixLayoutCreate(&a_layout_, kDataType, m, k, k),
                 "cublasLtMatrixLayoutCreate A");
    check_cublas(cublasLtMatrixLayoutCreate(&b_layout_, kDataType, k, n, n),
                 "cublasLtMatrixLayoutCreate B");
    check_cublas(cublasLtMatrixLayoutCreate(&c_layout_, kDataType, m, n, n),
                 "cublasLtMatrixLayoutCreate C");
    check_cublas(cublasLtMatrixLayoutCreate(&d_layout_, kDataType, m, n, n),
                 "cublasLtMatrixLayoutCreate D");

    for (auto* layout : {a_layout_, b_layout_, c_layout_, d_layout_}) {
      check_cublas(cublasLtMatrixLayoutSetAttribute(
                       layout,
                       CUBLASLT_MATRIX_LAYOUT_ORDER,
                       &kRowMajor,
                       sizeof(kRowMajor)),
                   "cublasLtMatrixLayoutSetAttribute order");
    }

    check_cublas(cublasLtMatmulPreferenceCreate(&preference_), "cublasLtMatmulPreferenceCreate");
    std::size_t max_workspace_bytes = workspace_.bytes();
    check_cublas(cublasLtMatmulPreferenceSetAttribute(
                     preference_,
                     CUBLASLT_MATMUL_PREF_MAX_WORKSPACE_BYTES,
                     &max_workspace_bytes,
                     sizeof(max_workspace_bytes)),
                 "cublasLtMatmulPreferenceSetAttribute workspace");

    std::array<cublasLtMatmulHeuristicResult_t, kLtRequestedHeuristicCount> heuristics{};
    int returned_results = 0;
    check_cublas(cublasLtMatmulAlgoGetHeuristic(
                     handle,
                     operation_desc_,
                     a_layout_,
                     b_layout_,
                     c_layout_,
                     d_layout_,
                     preference_,
                     static_cast<int>(heuristics.size()),
                     heuristics.data(),
                     &returned_results),
                 "cublasLtMatmulAlgoGetHeuristic");
    require(returned_results > 0, "cuBLASLt did not return a usable heuristic");
    require(algo_index < returned_results, "requested --algo-index is larger than the available cuBLASLt heuristic count");
    heuristic_ = heuristics[algo_index];
    workspace_bytes_ = static_cast<std::size_t>(heuristic_.workspaceSize);
  }

  ~LtMatmulPlan() {
    if (preference_ != nullptr) {
      cublasLtMatmulPreferenceDestroy(preference_);
    }
    if (d_layout_ != nullptr) {
      cublasLtMatrixLayoutDestroy(d_layout_);
    }
    if (c_layout_ != nullptr) {
      cublasLtMatrixLayoutDestroy(c_layout_);
    }
    if (b_layout_ != nullptr) {
      cublasLtMatrixLayoutDestroy(b_layout_);
    }
    if (a_layout_ != nullptr) {
      cublasLtMatrixLayoutDestroy(a_layout_);
    }
    if (operation_desc_ != nullptr) {
      cublasLtMatmulDescDestroy(operation_desc_);
    }
  }

  LtMatmulPlan(const LtMatmulPlan&) = delete;
  LtMatmulPlan& operator=(const LtMatmulPlan&) = delete;

  void launch(
      cublasLtHandle_t handle,
      const std::uint16_t* a_bf16,
      const std::uint16_t* b_bf16,
      std::uint16_t* c_bf16,
      cudaStream_t stream) const {
    const float alpha = 1.0f;
    const float beta = 0.0f;

    check_cublas(
        cublasLtMatmul(
            handle,
            operation_desc_,
            &alpha,
            reinterpret_cast<const __nv_bfloat16*>(a_bf16),
            a_layout_,
            reinterpret_cast<const __nv_bfloat16*>(b_bf16),
            b_layout_,
            &beta,
            reinterpret_cast<const __nv_bfloat16*>(c_bf16),
            c_layout_,
            reinterpret_cast<__nv_bfloat16*>(c_bf16),
            d_layout_,
            &heuristic_.algo,
            const_cast<std::uint8_t*>(workspace_.get()),
            workspace_bytes_,
            stream),
        "cublasLtMatmul");
  }

 private:
  cublasLtMatmulDesc_t operation_desc_ = nullptr;
  cublasLtMatrixLayout_t a_layout_ = nullptr;
  cublasLtMatrixLayout_t b_layout_ = nullptr;
  cublasLtMatrixLayout_t c_layout_ = nullptr;
  cublasLtMatrixLayout_t d_layout_ = nullptr;
  cublasLtMatmulPreference_t preference_ = nullptr;
  cublasLtMatmulHeuristicResult_t heuristic_{};
  DeviceBuffer<std::uint8_t> workspace_;
  std::size_t workspace_bytes_ = 0;
};

double percentile_from_sorted(const std::vector<float>& values, double fraction) {
  require(!values.empty(), "cannot compute percentile for empty runtime set");

  if (values.size() == 1) {
    return values.front();
  }

  const double position = fraction * static_cast<double>(values.size() - 1);
  const auto lower_index = static_cast<std::size_t>(std::floor(position));
  const auto upper_index = static_cast<std::size_t>(std::ceil(position));
  const double blend = position - static_cast<double>(lower_index);

  const double lower = values[lower_index];
  const double upper = values[upper_index];
  return lower + (upper - lower) * blend;
}

RuntimeSummary summarize_runtimes(std::vector<float> runtimes_ms) {
  require(!runtimes_ms.empty(), "no runtimes recorded");

  std::sort(runtimes_ms.begin(), runtimes_ms.end());
  RuntimeSummary summary;
  summary.p10_ms = percentile_from_sorted(runtimes_ms, 0.10);
  summary.median_ms = percentile_from_sorted(runtimes_ms, 0.50);
  summary.p90_ms = percentile_from_sorted(runtimes_ms, 0.90);
  return summary;
}

CorrectnessSummary evaluate_correctness(
    const std::vector<std::uint16_t>& output_bf16,
    const std::vector<float>& ref_fp32,
    const std::vector<std::uint16_t>& ref_bf16,
    double atol,
    double rtol,
    bool* passed) {
  require(output_bf16.size() == ref_fp32.size(), "output/ref_fp32 size mismatch");
  require(output_bf16.size() == ref_bf16.size(), "output/ref_bf16 size mismatch");
  require(passed != nullptr, "passed pointer must not be null");

  CorrectnessSummary summary;
  summary.atol = atol;
  summary.rtol = rtol;
  summary.bf16_exact_match = true;
  *passed = true;

  double abs_sum = 0.0;
  constexpr double kMinRelDenom = 1.0e-12;

  for (std::size_t i = 0; i < output_bf16.size(); ++i) {
    const double output = static_cast<double>(bf16_bits_to_float(output_bf16[i]));
    const double ref = static_cast<double>(ref_fp32[i]);
    const double abs_err = std::abs(output - ref);
    const double rel_err = abs_err / std::max(std::abs(ref), kMinRelDenom);
    const double tolerance = atol + rtol * std::abs(ref);

    summary.max_abs_err = std::max(summary.max_abs_err, abs_err);
    summary.max_rel_err = std::max(summary.max_rel_err, rel_err);
    abs_sum += abs_err;

    if (abs_err > tolerance) {
      *passed = false;
    }
    if (output_bf16[i] != ref_bf16[i]) {
      summary.bf16_exact_match = false;
    }
  }

  summary.mean_abs_err = abs_sum / static_cast<double>(output_bf16.size());
  return summary;
}

std::string format_number(double value) {
  std::ostringstream out;
  out << std::setprecision(10) << value;
  return out.str();
}

std::string make_success_json(
    RunnerMode mode,
    bool passed,
    const std::optional<RuntimeSummary>& runtime,
    const std::optional<CorrectnessSummary>& correctness,
    double tflops) {
  std::ostringstream json;
  json << "{\n";
  json << "  \"mode\": \"" << mode_to_string(mode) << "\",\n";
  json << "  \"passed\": " << (passed ? "true" : "false");

  if (runtime.has_value()) {
    json << ",\n";
    json << "  \"runtime_ms\": {\n";
    json << "    \"median\": " << format_number(runtime->median_ms) << ",\n";
    json << "    \"p10\": " << format_number(runtime->p10_ms) << ",\n";
    json << "    \"p90\": " << format_number(runtime->p90_ms) << "\n";
    json << "  },\n";
    json << "  \"tflops\": " << format_number(tflops);
  }

  if (correctness.has_value()) {
    json << ",\n";
    json << "  \"correctness\": {\n";
    json << "    \"max_abs_err\": " << format_number(correctness->max_abs_err) << ",\n";
    json << "    \"max_rel_err\": " << format_number(correctness->max_rel_err) << ",\n";
    json << "    \"mean_abs_err\": " << format_number(correctness->mean_abs_err) << ",\n";
    json << "    \"bf16_exact_match\": " << (correctness->bf16_exact_match ? "true" : "false") << ",\n";
    json << "    \"atol\": " << format_number(correctness->atol) << ",\n";
    json << "    \"rtol\": " << format_number(correctness->rtol) << "\n";
    json << "  }";
  }

  json << "\n}\n";
  return json.str();
}

std::string make_error_json(RunnerMode mode, const std::string& message) {
  std::ostringstream json;
  json << "{\n";
  json << "  \"mode\": \"" << mode_to_string(mode) << "\",\n";
  json << "  \"passed\": false,\n";
  json << "  \"error\": \"" << message << "\"\n";
  json << "}\n";
  return json.str();
}

void maybe_write_json(const std::optional<fs::path>& json_out, const std::string& payload) {
  if (!json_out.has_value()) {
    return;
  }

  const fs::path parent = json_out->parent_path();
  if (!parent.empty()) {
    fs::create_directories(parent);
  }

  std::ofstream output(*json_out);
  require(output.is_open(), "failed to open JSON output: " + json_out->string());
  output << payload;
  require(output.good(), "failed to write JSON output: " + json_out->string());
}

void flush_cache(DeviceBuffer<std::uint8_t>& scratch, cudaStream_t stream, std::uint8_t pattern) {
  if (scratch.get() == nullptr || scratch.bytes() == 0) {
    return;
  }
  check_cuda(cudaMemsetAsync(scratch.get(), pattern, scratch.bytes(), stream), "cudaMemsetAsync");
  check_cuda(cudaStreamSynchronize(stream), "cudaStreamSynchronize after cache flush");
}

std::size_t element_count(int rows, int cols) {
  return static_cast<std::size_t>(rows) * static_cast<std::size_t>(cols);
}

double gemm_tflops(int m, int n, int k, double runtime_ms) {
  const double flops = 2.0 * static_cast<double>(m) * static_cast<double>(n) * static_cast<double>(k);
  return flops / (runtime_ms * 1.0e9);
}

void launch_cublas_bf16_gemm(
    cublasLtHandle_t lt_handle,
    const LtMatmulPlan& lt_plan,
    const std::uint16_t* a_bf16,
    const std::uint16_t* b_bf16,
    std::uint16_t* c_bf16,
    int m,
    int n,
    int k,
    cudaStream_t stream) {
  (void)m;
  (void)n;
  (void)k;
  lt_plan.launch(lt_handle, a_bf16, b_bf16, c_bf16, stream);
}

}  // namespace

int runner_main(int argc, char** argv) {
  std::optional<RunnerArgs> args;

  try {
    args = parse_args(argc, argv);
    const CaseSpec spec = load_case_spec(args->dataset_dir, args->case_id);

    const std::size_t a_count = element_count(spec.m, spec.k);
    const std::size_t b_count = element_count(spec.k, spec.n);
    const std::size_t c_count = element_count(spec.m, spec.n);

    std::vector<std::uint16_t> a_host = read_binary_file<std::uint16_t>(spec.a_bf16_path, a_count);
    std::vector<std::uint16_t> b_host = read_binary_file<std::uint16_t>(spec.b_bf16_path, b_count);

    DeviceBuffer<std::uint16_t> d_a(a_count);
    DeviceBuffer<std::uint16_t> d_b(b_count);
    DeviceBuffer<std::uint16_t> d_c(c_count);
    DeviceBuffer<std::uint8_t> scratch(
        static_cast<std::size_t>(args->flush_cache_mb) * 1024ULL * 1024ULL);

    StreamGuard stream;
    CublasLtHandleGuard cublas_lt_handle;
    LtMatmulPlan lt_plan(cublas_lt_handle.get(), spec.m, spec.n, spec.k, args->algo_index);

    check_cuda(cudaMemcpyAsync(d_a.get(), a_host.data(), d_a.bytes(), cudaMemcpyHostToDevice, stream.get()),
               "cudaMemcpyAsync A");
    check_cuda(cudaMemcpyAsync(d_b.get(), b_host.data(), d_b.bytes(), cudaMemcpyHostToDevice, stream.get()),
               "cudaMemcpyAsync B");
    check_cuda(cudaStreamSynchronize(stream.get()), "cudaStreamSynchronize after H2D");

    std::vector<std::uint16_t>().swap(a_host);
    std::vector<std::uint16_t>().swap(b_host);

    if (args->mode == RunnerMode::kCorrectness) {
      launch_cublas_bf16_gemm(
          cublas_lt_handle.get(),
          lt_plan,
          d_a.get(),
          d_b.get(),
          d_c.get(),
          spec.m,
          spec.n,
          spec.k,
          stream.get());
      check_cuda(cudaStreamSynchronize(stream.get()), "cudaStreamSynchronize after correctness launch");

      std::vector<std::uint16_t> output_bf16(c_count);
      check_cuda(cudaMemcpy(output_bf16.data(), d_c.get(), d_c.bytes(), cudaMemcpyDeviceToHost),
                 "cudaMemcpy D2H output");

      const std::vector<float> ref_fp32 = read_binary_file<float>(spec.c_ref_fp32_path, c_count);
      const std::vector<std::uint16_t> ref_bf16 = read_binary_file<std::uint16_t>(spec.c_ref_bf16_path, c_count);

      bool passed = false;
      const CorrectnessSummary correctness =
          evaluate_correctness(output_bf16, ref_fp32, ref_bf16, spec.atol, spec.rtol, &passed);

      maybe_write_json(
          args->json_out,
          make_success_json(args->mode, passed, std::nullopt, correctness, 0.0));
      return passed ? 0 : 1;
    }

    for (int i = 0; i < args->warmup; ++i) {
      flush_cache(scratch, stream.get(), static_cast<std::uint8_t>(i));
      launch_cublas_bf16_gemm(
          cublas_lt_handle.get(),
          lt_plan,
          d_a.get(),
          d_b.get(),
          d_c.get(),
          spec.m,
          spec.n,
          spec.k,
          stream.get());
    }
    check_cuda(cudaStreamSynchronize(stream.get()), "cudaStreamSynchronize after warmup");

    EventGuard start_event;
    EventGuard stop_event;
    std::vector<float> runtimes_ms;
    runtimes_ms.reserve(static_cast<std::size_t>(args->iters));

    for (int i = 0; i < args->iters; ++i) {
      flush_cache(scratch, stream.get(), static_cast<std::uint8_t>(i + args->warmup));

      check_cuda(cudaEventRecord(start_event.get(), stream.get()), "cudaEventRecord start");
      launch_cublas_bf16_gemm(
          cublas_lt_handle.get(),
          lt_plan,
          d_a.get(),
          d_b.get(),
          d_c.get(),
          spec.m,
          spec.n,
          spec.k,
          stream.get());
      check_cuda(cudaEventRecord(stop_event.get(), stream.get()), "cudaEventRecord stop");
      check_cuda(cudaEventSynchronize(stop_event.get()), "cudaEventSynchronize stop");

      float elapsed_ms = 0.0f;
      check_cuda(cudaEventElapsedTime(&elapsed_ms, start_event.get(), stop_event.get()), "cudaEventElapsedTime");
      runtimes_ms.push_back(elapsed_ms);
    }

    const RuntimeSummary runtime = summarize_runtimes(runtimes_ms);
    const double tflops = gemm_tflops(spec.m, spec.n, spec.k, runtime.median_ms);

    maybe_write_json(
        args->json_out,
        make_success_json(args->mode, true, runtime, std::nullopt, tflops));
    return 0;
  } catch (const std::exception& ex) {
    std::cerr << "[runner-error] " << ex.what() << '\n';
    if (args.has_value()) {
      try {
        maybe_write_json(args->json_out, make_error_json(args->mode, ex.what()));
      } catch (...) {
      }
    }
    return 1;
  }
}

}  // namespace matmul_optimizer

int main(int argc, char** argv) {
  return matmul_optimizer::runner_main(argc, argv);
}
