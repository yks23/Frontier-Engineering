from __future__ import annotations

import argparse
import json
import time
from pathlib import Path


def load_instance(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def earliest_slot(intervals: list[tuple[int, int]], ready_time: int, duration: int) -> int:
    t = max(0, int(ready_time))
    for start, end in intervals:
        if t + duration <= start:
            return t
        if t < end:
            t = end
    return t


def insert_interval(intervals: list[tuple[int, int]], start: int, end: int) -> None:
    idx = 0
    while idx < len(intervals) and intervals[idx][0] <= start:
        idx += 1
    intervals.insert(idx, (start, end))


def dispatch_key(candidate: dict, rule: str) -> tuple:
    est = candidate["est"]
    duration = candidate["duration"]
    remaining = candidate["remaining"]
    ops_left = candidate["ops_left"]
    job = candidate["job"]

    if rule == "est_spt":
        return (est, duration, -remaining, -ops_left, job)
    if rule == "mwkr":
        return (est, -remaining, duration, -ops_left, job)
    if rule == "mopnr":
        return (est, -ops_left, duration, -remaining, job)
    if rule == "spt":
        return (duration, est, -remaining, -ops_left, job)
    if rule == "lpt":
        return (-duration, est, -remaining, -ops_left, job)
    return (est, duration, -remaining, -ops_left, job)


def build_schedule(instance: dict, rule: str) -> dict:
    jobs = instance["jobs"]
    num_jobs = int(instance["num_jobs"])
    num_machines = int(instance["num_machines"])

    machine_intervals: list[list[tuple[int, int]]] = [[] for _ in range(num_machines)]
    job_next_op = [0] * num_jobs
    job_ready = [0] * num_jobs
    remaining_work = [sum(int(op["duration"]) for op in job) for job in jobs]
    ops_left = [len(job) for job in jobs]
    total_ops = sum(len(job) for job in jobs)

    scheduled_ops: list[dict] = []

    while len(scheduled_ops) < total_ops:
        candidates: list[dict] = []
        for job_id in range(num_jobs):
            op_id = job_next_op[job_id]
            if op_id >= len(jobs[job_id]):
                continue
            op = jobs[job_id][op_id]
            machine = int(op["machine"])
            duration = int(op["duration"])
            est = earliest_slot(machine_intervals[machine], job_ready[job_id], duration)
            candidates.append(
                {
                    "job": job_id,
                    "op": op_id,
                    "machine": machine,
                    "duration": duration,
                    "est": est,
                    "remaining": remaining_work[job_id],
                    "ops_left": ops_left[job_id],
                }
            )

        chosen = min(candidates, key=lambda item: dispatch_key(item, rule))
        start = int(chosen["est"])
        end = start + int(chosen["duration"])
        machine = int(chosen["machine"])
        job_id = int(chosen["job"])
        op_id = int(chosen["op"])

        insert_interval(machine_intervals[machine], start, end)
        scheduled_ops.append(
            {
                "job": job_id,
                "op": op_id,
                "machine": machine,
                "start": start,
            }
        )

        job_next_op[job_id] += 1
        job_ready[job_id] = end
        remaining_work[job_id] -= int(chosen["duration"])
        ops_left[job_id] -= 1

    makespan = max(job_ready) if job_ready else 0
    return {
        "instance_id": instance.get("instance_id", "unknown"),
        "algorithm": f"dispatch_{rule}",
        "makespan": makespan,
        "operations": scheduled_ops,
    }


def choose_best_schedule(instance: dict, time_budget_s: float) -> dict:
    rules = ["est_spt", "mwkr", "mopnr", "spt", "lpt"]
    start = time.time()
    best: dict | None = None

    for rule in rules:
        if time.time() - start > time_budget_s:
            break
        candidate = build_schedule(instance, rule)
        if best is None or int(candidate["makespan"]) < int(best["makespan"]):
            best = candidate

    if best is None:
        best = build_schedule(instance, "est_spt")

    best["algorithm"] = "multi_dispatch_rules"
    return best


# 请勿修改：CLI 接口契约由 evaluator 调用。
# 可修改：求解逻辑、派工规则和时间预算内的搜索策略。
def solve_instance(instance: dict, time_budget_s: float = 0.5) -> dict:
    return choose_best_schedule(instance, time_budget_s=time_budget_s)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--instance", required=True, help="Path to instance JSON")
    parser.add_argument("--output", required=True, help="Path to output JSON")
    parser.add_argument("--time-budget", type=float, default=0.5)
    args = parser.parse_args()

    instance = load_instance(args.instance)
    result = solve_instance(instance, time_budget_s=float(args.time_budget))

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)


if __name__ == "__main__":
    main()
