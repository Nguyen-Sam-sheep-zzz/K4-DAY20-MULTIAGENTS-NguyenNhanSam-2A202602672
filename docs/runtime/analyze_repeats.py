"""Reproduce the 6e statistics and audit without API calls (standard library only).

Run from any directory: python docs/runtime/analyze_repeats.py
Original results and supplied lab modules are read-only; outputs go to report/.
"""
import hashlib
import json
import re
import statistics
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONDITIONS = ("baseline", "subagents", "skills-auto")
TASKS = ("code-eval", "data-eval", "logs-eval")
SOURCES = ("results", "results/repeat-2", "results/repeat-3")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args):
    return subprocess.check_output(
        ["git", "-c", f"safe.directory={ROOT.as_posix()}", *args], cwd=ROOT
    ).decode("utf-8").strip()


def describe(values):
    return {"mean": statistics.mean(values), "min": min(values), "max": max(values)}


def main():
    design = read_json(ROOT / "report/repeat-design.json")
    assert git("rev-parse", "freeze") == design["freeze_commit"], "freeze tag changed"
    assert not git("diff", "freeze", "--", "src/lab", "skills"), "source/skill changed"
    freeze_time = datetime.fromisoformat(git("log", "-1", "--format=%cI", "freeze"))
    skill_root = ROOT / "skills/auto"
    skill_files = sorted(
        f for folder in skill_root.iterdir() if (folder / "SKILL.md").is_file()
        for f in folder.rglob("*") if f.is_file()
    )
    digest = hashlib.sha256()
    for f in skill_files:
        digest.update(f.relative_to(skill_root).as_posix().encode())
        digest.update(f.read_bytes())
    skill_hash = digest.hexdigest()
    assert skill_hash == design["skill_hash_linux"], "skill bytes changed"
    for name, expected in design["skill_file_sha256"].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    for name, expected in design["official_run_sha256"].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    for manifest in ("protected-file-hashes.txt", "source-document-hashes.txt"):
        for line in (ROOT / "report" / manifest).read_text(encoding="utf-8").splitlines():
            name, expected = line.rsplit(" ", 1)
            # The original manifest was recorded in Windows PowerShell.
            manifest_path = ROOT / name.replace("\\", "/")
            content = manifest_path.read_bytes()
            # A Linux clone uses LF; permit checkout newline conversion only.
            # Generated skills and original run records remain byte-exact above.
            lf = content.replace(b"\r\n", b"\n")
            candidates = (content, lf, lf.replace(b"\n", b"\r\n"))
            assert any(hashlib.sha256(data).hexdigest() == expected.lower() for data in candidates), name

    records = []
    evidence = []
    behavior = []
    for number, source in enumerate(SOURCES, 1):
        for condition in CONDITIONS:
            if number > 1:
                actual = {p.parent.name for p in (ROOT / source / condition).glob("*/run.json")}
                assert actual == set(TASKS), (source, condition, actual)
            for task in TASKS:
                path = ROOT / source / condition / task / "run.json"
                record = read_json(path)
                assert record["task"] == task and record["condition"] == condition
                assert record["role"] == "eval" and record["error"] is None, path
                assert not record["skills_modified"], path
                assert record["passed"] == sum(c["passed"] for c in record["checks"])
                assert record["total"] == len(record["checks"])
                assert abs(record["score"] - record["passed"] / record["total"]) < 1e-12
                assert record["tokens"]["input"] + record["tokens"]["output"] == record["tokens"]["total"] > 0
                assert datetime.fromisoformat(record["timestamp"]) >= freeze_time
                if condition == "skills-auto":
                    assert record["skills_sha256"] == skill_hash, path
                trace = path.with_name("trace.md")
                assert trace.is_file() and trace.stat().st_size > 0, trace
                trace_text = trace.read_text(encoding="utf-8")
                reads = re.findall(r"### Tool call: read_file\n(.*?)(?=\n\n###|\Z)", trace_text, re.S)
                behavior.append({
                    "repetition": number, "condition": condition, "task": task,
                    "subagent_calls": record["subagent_calls"], "skills_read": record["skills_read"],
                    "tokens": record["tokens"]["total"],
                    "delegations": re.findall(r"### Tool call: task\n(.*?)(?=\n\n###|\Z)", trace_text, re.S),
                    "skill_read_calls": [call for call in reads if "skills/" in call],
                })
                records.append({**record, "repetition": number, "run_path": path.relative_to(ROOT).as_posix()})
                evidence.append({
                    "run_path": path.relative_to(ROOT).as_posix(),
                    "run_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "trace_sha256": hashlib.sha256(trace.read_bytes()).hexdigest(),
                })

    per_task = []
    per_condition = []
    for condition in CONDITIONS:
        selected = [r for r in records if r["condition"] == condition]
        round_scores = [statistics.mean(r["score"] for r in selected if r["repetition"] == n) for n in (1, 2, 3)]
        totals = {}
        for label, is_rule in (("technical", False), ("rules", True)):
            checks = [c for r in selected for c in r["checks"] if c["name"].startswith("rule_") == is_rule]
            totals[label] = {"passed": sum(c["passed"] for c in checks), "total": len(checks)}
        mean_tokens = statistics.mean(r["tokens"]["total"] for r in selected)
        mean_score = statistics.mean(r["score"] for r in selected)
        per_condition.append({
            "condition": condition, "runs": 9, "score": describe([r["score"] for r in selected]),
            "round_mean_scores": round_scores, "round_mean_score_range": describe(round_scores),
            "tokens": describe([r["tokens"]["total"] for r in selected]),
            "seconds": describe([r["seconds"] for r in selected]),
            "score_per_million_tokens": mean_score / mean_tokens * 1e6,
            "total_tokens": sum(r["tokens"]["total"] for r in selected),
            "runs_read_skill": sum(r["skills_read"] > 0 for r in selected),
            "subagent_calls": sum(r["subagent_calls"] for r in selected), **totals,
        })
        for task in TASKS:
            group = [r for r in selected if r["task"] == task]
            per_task.append({
                "condition": condition, "task": task, "runs": 3,
                "scores": [r["score"] for r in group],
                "passed_total": [f"{r['passed']}/{r['total']}" for r in group],
                "score": describe([r["score"] for r in group]),
                "tokens": describe([r["tokens"]["total"] for r in group]),
                "token_samples": [r["tokens"]["total"] for r in group],
                "seconds": describe([r["seconds"] for r in group]),
                "subagent_calls": [r["subagent_calls"] for r in group],
                "skills_read": [r["skills_read"] for r in group],
                "failed_checks": [[c["name"] for c in r["checks"] if not c["passed"]] for r in group],
            })

    extra = [r for r in records if r["repetition"] > 1]
    all_attempts = [read_json(p) for p in (ROOT / "results").rglob("run.json")]
    budget = {
        "additional_task_runs": len(extra), "additional_tokens": sum(r["tokens"]["total"] for r in extra),
        "all_task_attempts": len(all_attempts),
        "all_recorded_task_tokens": sum(r["tokens"]["total"] for r in all_attempts),
        "api_smoke_tokens": 16, "curator_calls": 1, "curator_tokens": "not captured",
    }
    baseline = per_condition[0]
    comparisons = []
    for row in per_condition[1:]:
        gains = [a - b for a, b in zip(row["round_mean_scores"], baseline["round_mean_scores"])]
        comparisons.append({
            "condition": row["condition"], "reference": "baseline",
            "round_mean_score_gains": gains, "gain": describe(gains),
            "mean_token_ratio": row["tokens"]["mean"] / baseline["tokens"]["mean"],
        })
    summary = {"design": design, "per_task": per_task, "per_condition": per_condition,
               "comparisons": comparisons, "budget": budget}
    (ROOT / "report/repeat-metrics.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    audit = {
        "evaluation_records": len(records), "additional_records": len(extra), "trace_pairs": len(evidence),
        "additional_skill_runs_checked": sum(r["condition"] == "skills-auto" for r in extra),
        "skill_hash": skill_hash, "freeze_tag_unchanged": True, "source_and_skills_unchanged": True,
        "official_evaluation_run_hashes_unchanged": True, "protected_file_hashes_unchanged": True,
        "errors": [], "modified_skill_runs": [], "hash_and_timestamp_checks": "OK", "evidence": evidence,
    }
    (ROOT / "report/repeat-audit.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    (ROOT / "report/repeat-behavior-evidence.json").write_text(
        json.dumps(behavior, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Phần 6e: bảng thống kê ba lượt eval", "",
        "Lượt 1 là kết quả chính thức; lượt 2/3 từ results/repeat-2 và repeat-3. Không trộn vào table.md.", "",
        "| Điều kiện | Tác vụ | Điểm lượt 1 / 2 / 3 | Mean score | Min–max score | Mean token | Min–max token |",
        "|---|---|---|---:|---:|---:|---:|",
    ]
    for row in per_task:
        score, tokens = row["score"], row["tokens"]
        lines.append(f"| {row['condition']} | {row['task']} | {' / '.join(row['passed_total'])} | "
                     f"{score['mean']:.6f} | {score['min']:.6f}–{score['max']:.6f} | "
                     f"{tokens['mean']:,.2f} | {tokens['min']:,}–{tokens['max']:,} |")
    lines += ["", "| Điều kiện | Mean score 9 run | Mean theo vòng 1 / 2 / 3 | Min–max mean theo vòng | Mean token/run | Mean giây/run | Điểm/triệu token | Kỹ thuật | Quy ước |",
              "|---|---:|---|---:|---:|---:|---:|---:|---:|"]
    for row in per_condition:
        interval = row["round_mean_score_range"]
        lines.append(f"| {row['condition']} | {row['score']['mean']:.6f} | "
                     f"{' / '.join(f'{s:.6f}' for s in row['round_mean_scores'])} | "
                     f"{interval['min']:.6f}–{interval['max']:.6f} | {row['tokens']['mean']:,.2f} | "
                     f"{row['seconds']['mean']:.2f} | {row['score_per_million_tokens']:.2f} | "
                     f"{row['technical']['passed']}/{row['technical']['total']} | "
                     f"{row['rules']['passed']}/{row['rules']['total']} |")
    lines += ["", f"18 lượt thêm dùng {budget['additional_tokens']:,} token đo. Tổng {budget['all_task_attempts']} "
              f"lượt tác vụ dùng {budget['all_recorded_task_tokens']:,} token; smoke 16 token, curator không ghi token.",
              "", "Score là tỷ lệ 0–1; mean theo tác vụ/vòng có cùng trọng số cho ba họ. "
              "Min–max là dao động quan sát, không phải khoảng tin cậy. Token có cộng subagent; trace chỉ có luồng chính."]
    (ROOT / "report/repeat-table.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"6e: {len(records)} eval records/trace pairs, {len(extra)} additional; six additional skill runs: OK")
    print(json.dumps(budget))


if __name__ == "__main__":
    main()
