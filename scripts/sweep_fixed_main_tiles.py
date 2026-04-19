#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = REPO_ROOT / "configs/fixed_bf16_gemm_v1.json"
DEFAULT_RUNNER = REPO_ROOT / "build/custom_runner"
DEFAULT_JSON_OUT = REPO_ROOT / "state/autotune_round18_main_tiles.json"
DEFAULT_MD_OUT = REPO_ROOT / "state/autotune_round18_main_tiles.md"
DEFAULT_CANDIDATES = [32, 64, 96, 128, 160, 192, 256, 320, 384, 480]
SUPPORTED_CANDIDATES = set(DEFAULT_CANDIDATES)
ENV_VAR = "MATMUL_FIXED_MAIN_TILE_N"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def runner_base_command(runner: Path) -> list[str]:
    if runner.suffix == ".py":
        return [sys.executable, str(runner)]
    return [str(runner)]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sweep fixed benchmark main-tile widths via MATMUL_FIXED_MAIN_TILE_N."
    )
    parser.add_argument("--runner", type=Path, default=DEFAULT_RUNNER, help="Benchmark runner binary or Python script")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="Benchmark config JSON")
    parser.add_argument("--dataset-dir", type=Path, default=None, help="Dataset directory; defaults from config")
    parser.add_argument("--json-out", type=Path, default=DEFAULT_JSON_OUT, help="Lightweight JSON summary output")
    parser.add_argument("--md-out", type=Path, default=DEFAULT_MD_OUT, help="Lightweight Markdown summary output")
    parser.add_argument(
        "--candidates",
        nargs="+",
        type=int,
        default=DEFAULT_CANDIDATES,
        help="Supported fixed main-tile widths to sweep",
    )
    parser.add_argument("--warmup", type=int, default=None, help="Override warmup iterations")
    parser.add_argument("--iters", type=int, default=None, help="Override timed iterations")
    parser.add_argument("--flush-cache-mb", type=int, default=None, help="Override cache flush scratch size in MiB")
    parser.add_argument("--skip-correctness", action="store_true", help="Skip correctness cases and run perf only")
    parser.add_argument("--stop-on-failure", action="store_true", help="Stop the sweep after the first candidate failure")
    parser.add_argument("--workdir", type=Path, default=REPO_ROOT, help="Working directory for runner invocations")
    parser.add_argument(
        "--extra-runner-arg",
        action="append",
        default=[],
        help="Extra argument appended to the runner command; may be passed multiple times",
    )
    return parser.parse_args()


def normalize_candidates(raw_candidates: list[int]) -> list[int]:
    seen: set[int] = set()
    candidates: list[int] = []
    for candidate in raw_candidates:
        if candidate not in SUPPORTED_CANDIDATES:
            raise ValueError(
                f"Unsupported candidate {candidate}; expected one of {sorted(SUPPORTED_CANDIDATES)}"
            )
        if candidate not in seen:
            candidates.append(candidate)
            seen.add(candidate)
    return candidates


def summarize_output(text: str) -> str | None:
    stripped_lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    if not stripped_lines:
        return None
    return "\n".join(stripped_lines[-20:])


def run_runner_once(
    runner_cmd: list[str],
    dataset_dir: Path,
    case_id: str,
    mode: str,
    warmup: int,
    iters: int,
    flush_cache_mb: int,
    workdir: Path,
    extra_runner_args: list[str],
    env: dict[str, str],
    scratch_dir: Path,
) -> dict[str, Any]:
    json_out = scratch_dir / f"{mode}_{case_id}.json"
    cmd = (
        runner_cmd
        + [
            "--dataset-dir",
            str(dataset_dir),
            "--case-id",
            case_id,
            "--mode",
            mode,
            "--warmup",
            str(warmup),
            "--iters",
            str(iters),
            "--flush-cache-mb",
            str(flush_cache_mb),
            "--json-out",
            str(json_out),
        ]
        + list(extra_runner_args)
    )

    completed = subprocess.run(
        cmd,
        cwd=str(workdir),
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    result: dict[str, Any] = {
        "case_id": case_id,
        "mode": mode,
        "command": cmd,
        "returncode": completed.returncode,
    }

    stdout_excerpt = summarize_output(completed.stdout)
    stderr_excerpt = summarize_output(completed.stderr)
    if stdout_excerpt is not None:
        result["stdout_excerpt"] = stdout_excerpt
    if stderr_excerpt is not None:
        result["stderr_excerpt"] = stderr_excerpt

    if completed.returncode != 0:
        result["passed"] = False
        result["error"] = f"runner exited with code {completed.returncode}"
        return result

    if not json_out.exists():
        result["passed"] = False
        result["error"] = "runner did not produce expected JSON output"
        return result

    payload = load_json(json_out)
    payload["case_id"] = case_id
    payload["mode"] = mode
    payload["command"] = cmd
    if stdout_excerpt is not None:
        payload["stdout_excerpt"] = stdout_excerpt
    if stderr_excerpt is not None:
        payload["stderr_excerpt"] = stderr_excerpt
    return payload


def evaluate_candidate(
    tile_n: int,
    runner_cmd: list[str],
    dataset_dir: Path,
    benchmark_case: str,
    correctness_cases: list[str],
    warmup: int,
    iters: int,
    flush_cache_mb: int,
    workdir: Path,
    extra_runner_args: list[str],
    skip_correctness: bool,
) -> dict[str, Any]:
    env = os.environ.copy()
    env[ENV_VAR] = str(tile_n)

    result: dict[str, Any] = {
        "tile_n": tile_n,
        "env": {ENV_VAR: str(tile_n)},
        "hot_band_columns": 7680,
        "tail_columns": 96,
        "split_description": f"64x{tile_n} main over first 7680 columns plus 64x96 tail",
    }

    with tempfile.TemporaryDirectory(prefix=f"fixed_main_tile_{tile_n}_") as temp_dir:
        scratch_dir = Path(temp_dir)
        correctness_runs: list[dict[str, Any]] = []

        if not skip_correctness:
            for case_id in correctness_cases:
                payload = run_runner_once(
                    runner_cmd=runner_cmd,
                    dataset_dir=dataset_dir,
                    case_id=case_id,
                    mode="correctness",
                    warmup=0,
                    iters=1,
                    flush_cache_mb=flush_cache_mb,
                    workdir=workdir,
                    extra_runner_args=extra_runner_args,
                    env=env,
                    scratch_dir=scratch_dir,
                )
                correctness_runs.append(payload)
                if not payload.get("passed", False):
                    break

        result["correctness_runs"] = correctness_runs
        if skip_correctness:
            result["correctness_passed"] = None
        else:
            result["correctness_passed"] = bool(correctness_runs) and all(
                item.get("passed", False) for item in correctness_runs
            )

        perf_run: dict[str, Any] | None = None
        should_run_perf = skip_correctness or result["correctness_passed"]
        if should_run_perf:
            perf_run = run_runner_once(
                runner_cmd=runner_cmd,
                dataset_dir=dataset_dir,
                case_id=benchmark_case,
                mode="perf",
                warmup=warmup,
                iters=iters,
                flush_cache_mb=flush_cache_mb,
                workdir=workdir,
                extra_runner_args=extra_runner_args,
                env=env,
                scratch_dir=scratch_dir,
            )
        else:
            perf_run = {
                "case_id": benchmark_case,
                "mode": "perf",
                "passed": False,
                "skipped": True,
                "error": "perf skipped because correctness failed",
            }

        result["perf_run"] = perf_run
        result["perf_passed"] = bool(perf_run.get("passed", False))
        runtime_ms = perf_run.get("runtime_ms", {})
        result["median_runtime_ms"] = runtime_ms.get("median")
        result["p10_runtime_ms"] = runtime_ms.get("p10")
        result["p90_runtime_ms"] = runtime_ms.get("p90")
        result["tflops"] = perf_run.get("tflops")

    if result["perf_passed"] and (skip_correctness or result["correctness_passed"]):
        result["status"] = "ok"
    elif not skip_correctness and not result["correctness_passed"]:
        result["status"] = "correctness_failed"
    else:
        result["status"] = "perf_failed"

    return result


def build_summary_markdown(summary: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Fixed Main Tile Sweep")
    lines.append("")
    lines.append(f"- timestamp: `{summary['timestamp']}`")
    lines.append(f"- runner: `{summary['runner']}`")
    lines.append(f"- dataset dir: `{summary['dataset_dir']}`")
    lines.append(f"- benchmark case: `{summary['benchmark_case']}`")
    lines.append(f"- correctness cases: `{', '.join(summary['correctness_cases'])}`")
    lines.append(f"- env var: `{summary['env_var']}`")
    lines.append(f"- default fixed path when unset: `{summary['default_split']}`")
    lines.append(f"- override fixed path when set: `{summary['override_split_template']}`")
    lines.append(f"- warmup / iters: `{summary['warmup']}` / `{summary['iters']}`")
    lines.append(f"- flush cache MiB: `{summary['flush_cache_mb']}`")
    lines.append("")

    best_tile_n = summary.get("best_tile_n")
    if best_tile_n is not None:
        lines.append("## Best Candidate")
        lines.append("")
        lines.append(f"- tile_n: `{best_tile_n}`")
        lines.append(f"- median runtime (ms): `{summary.get('best_median_runtime_ms')}`")
        lines.append(f"- TFLOP/s: `{summary.get('best_tflops')}`")
        lines.append("")

    lines.append("## Results")
    lines.append("")
    lines.append("| tile_n | correctness | perf | median ms | p10 ms | p90 ms | TFLOP/s | status |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for result in summary["results"]:
        correctness_passed = result.get("correctness_passed")
        if correctness_passed is None:
            correctness_cell = "SKIP"
        else:
            correctness_cell = "PASS" if correctness_passed else "FAIL"
        perf_cell = "PASS" if result.get("perf_passed") else "FAIL"
        lines.append(
            f"| {result['tile_n']} | {correctness_cell} | {perf_cell} | "
            f"{result.get('median_runtime_ms', 'N/A')} | {result.get('p10_runtime_ms', 'N/A')} | "
            f"{result.get('p90_runtime_ms', 'N/A')} | {result.get('tflops', 'N/A')} | {result['status']} |"
        )

    failure_lines: list[str] = []
    for result in summary["results"]:
        if result["status"] == "ok":
            continue
        if result["status"] == "correctness_failed":
            failed_case = next((item for item in result["correctness_runs"] if not item.get("passed", False)), None)
            if failed_case is not None:
                failure_lines.append(
                    f"- `tile_n={result['tile_n']}` correctness failed on `{failed_case['case_id']}`: "
                    f"`{failed_case.get('error', 'runner returned a failing correctness payload')}`"
                )
        else:
            perf_run = result["perf_run"]
            failure_lines.append(
                f"- `tile_n={result['tile_n']}` perf failed: "
                f"`{perf_run.get('error', 'runner returned a failing perf payload')}`"
            )

    if failure_lines:
        lines.append("")
        lines.append("## Failures")
        lines.append("")
        lines.extend(failure_lines)

    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    config_path = args.config.resolve()
    runner_path = args.runner.resolve()
    workdir = args.workdir.resolve()

    if not config_path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")
    if not runner_path.exists():
        raise FileNotFoundError(f"Runner not found: {runner_path}")
    if not workdir.exists():
        raise FileNotFoundError(f"Workdir not found: {workdir}")

    config = load_json(config_path)
    benchmark_policy = config["benchmark_policy"]
    benchmark_case = benchmark_policy["benchmark_case"]
    correctness_cases = list(benchmark_policy["correctness_cases"])
    dataset_dir = args.dataset_dir.resolve() if args.dataset_dir is not None else (
        REPO_ROOT / "artifacts" / "datasets" / config["dataset_id"]
    ).resolve()
    if not dataset_dir.exists():
        raise FileNotFoundError(f"Dataset directory not found: {dataset_dir}")

    warmup = args.warmup if args.warmup is not None else int(benchmark_policy["warmup_iterations"])
    iters = args.iters if args.iters is not None else int(benchmark_policy["timed_iterations"])
    flush_cache_mb = (
        args.flush_cache_mb
        if args.flush_cache_mb is not None
        else int(benchmark_policy["cache_flush_scratch_mib"])
    )
    candidates = normalize_candidates(list(args.candidates))
    runner_cmd = runner_base_command(runner_path)

    results: list[dict[str, Any]] = []
    for tile_n in candidates:
        result = evaluate_candidate(
            tile_n=tile_n,
            runner_cmd=runner_cmd,
            dataset_dir=dataset_dir,
            benchmark_case=benchmark_case,
            correctness_cases=correctness_cases,
            warmup=warmup,
            iters=iters,
            flush_cache_mb=flush_cache_mb,
            workdir=workdir,
            extra_runner_args=list(args.extra_runner_arg),
            skip_correctness=args.skip_correctness,
        )
        results.append(result)
        if args.stop_on_failure and result["status"] != "ok":
            break

    successful_results = [
        result
        for result in results
        if result["perf_passed"] and (args.skip_correctness or result["correctness_passed"])
    ]
    successful_results.sort(key=lambda item: item["median_runtime_ms"])

    summary: dict[str, Any] = {
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "runner": str(runner_path),
        "config": str(config_path),
        "dataset_dir": str(dataset_dir),
        "workdir": str(workdir),
        "env_var": ENV_VAR,
        "default_split": "64x384 main over 7680 columns + 64x96 tail",
        "override_split_template": "64x<TILE_N> main over 7680 columns + 64x96 tail",
        "benchmark_case": benchmark_case,
        "correctness_cases": correctness_cases,
        "warmup": warmup,
        "iters": iters,
        "flush_cache_mb": flush_cache_mb,
        "skip_correctness": args.skip_correctness,
        "candidates": candidates,
        "results": results,
    }

    if successful_results:
        best_result = successful_results[0]
        summary["best_tile_n"] = best_result["tile_n"]
        summary["best_median_runtime_ms"] = best_result["median_runtime_ms"]
        summary["best_tflops"] = best_result["tflops"]
        summary["ranked_tiles_by_median_runtime_ms"] = [
            {
                "tile_n": result["tile_n"],
                "median_runtime_ms": result["median_runtime_ms"],
                "tflops": result["tflops"],
            }
            for result in successful_results
        ]
    else:
        summary["best_tile_n"] = None
        summary["best_median_runtime_ms"] = None
        summary["best_tflops"] = None
        summary["ranked_tiles_by_median_runtime_ms"] = []

    json_out = args.json_out.resolve()
    md_out = args.md_out.resolve()
    write_json(json_out, summary)
    md_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.write_text(build_summary_markdown(summary), encoding="utf-8")

    return 0 if successful_results else 1


if __name__ == "__main__":
    raise SystemExit(main())
