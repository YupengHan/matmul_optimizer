#pragma once

namespace matmul_optimizer {

enum class RunnerMode {
  kCorrectness,
  kPerf,
};

struct RuntimeSummary {
  double median_ms = 0.0;
  double p10_ms = 0.0;
  double p90_ms = 0.0;
};

struct CorrectnessSummary {
  double max_abs_err = 0.0;
  double max_rel_err = 0.0;
  double mean_abs_err = 0.0;
  double atol = 0.0;
  double rtol = 0.0;
  bool bf16_exact_match = false;
};

}  // namespace matmul_optimizer
