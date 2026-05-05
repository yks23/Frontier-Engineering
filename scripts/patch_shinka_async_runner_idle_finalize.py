#!/usr/bin/env python3
"""Patch upstream ShinkaEvolve async runner idle-loop finalization bug.

When `running_jobs` is empty, `_job_monitor_task` used to sleep/continue without ever
checking `completed_generations >= num_generations`, so gen-0-only runs never set
`finalization_complete` and hang forever.

Idempotent: skips if marker already present.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

MARKER = "# FRONTIER_EVAL_IDLE_FINALIZE_PATCH"

INSERT = f"""            if not self.running_jobs:
                {MARKER}
                if (
                    self.completed_generations >= self.evo_config.num_generations
                    and len(self.active_proposal_tasks) == 0
                ):
                    if self.verbose:
                        logger.info(
                            "Evolution stopping (idle monitor): "
                            f"completed_generations={{self.completed_generations}}, "
                            f"target={{self.evo_config.num_generations}}"
                        )
                    self.should_stop.set()
                    self.slot_available.set()
                    logger.info(
                        "🏁 Job monitor (idle) setting finalization_complete signal"
                    )
                    self.finalization_complete.set()
                    break
                # Debug: Log when waiting with no jobs
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "async_runner_py",
        type=Path,
        nargs="?",
        default=None,
        help="Path to shinka/core/async_runner.py",
    )
    args = parser.parse_args()
    path = args.async_runner_py
    if path is None:
        print("error: pass path to shinka/core/async_runner.py", file=sys.stderr)
        return 2
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        print(f"already patched: {path}")
        return 0
    needle = """            if not self.running_jobs:
                # Debug: Log when waiting with no jobs
"""
    if needle not in text:
        print(f"error: patch context not found in {path}", file=sys.stderr)
        return 1
    path.write_text(text.replace(needle, INSERT, 1), encoding="utf-8")
    print(f"patched: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
