from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
RESEARCH = ROOT / "references" / "research"


def fail(name: str, detail: str) -> tuple[str, bool, str]:
    return name, False, detail


def ok(name: str, detail: str) -> tuple[str, bool, str]:
    return name, True, detail


def main() -> int:
    text = SKILL.read_text(encoding="utf-8")
    checks: list[tuple[str, bool, str]] = []

    model_count = len(re.findall(r"^### 模型\d+：", text, flags=re.M))
    checks.append(ok("心智模型数量", f"{model_count} 个") if 3 <= model_count <= 7 else fail("心智模型数量", f"{model_count} 个，不在 3-7 范围"))

    heuristic_match = re.search(r"## 决策启发式\n\n(.*?)\n\n## 表达 DNA", text, flags=re.S)
    heuristic_count = 0
    if heuristic_match:
        heuristic_count = len(re.findall(r"^\d+\. \*\*", heuristic_match.group(1), flags=re.M))
    checks.append(ok("决策启发式数量", f"{heuristic_count} 条") if 5 <= heuristic_count <= 10 else fail("决策启发式数量", f"{heuristic_count} 条，不在 5-10 范围"))

    required_sections = [
        "## 回答工作流",
        "### 🔴 CHECKPOINT：先停下的红灯",
        "### 输出骨架",
        "## 表达 DNA",
        "## 价值观与反模式",
        "## 诚实边界",
        "## 附录：调研来源",
    ]
    missing_sections = [section for section in required_sections if section not in text]
    checks.append(ok("关键章节", "全部存在") if not missing_sections else fail("关键章节", "缺失：" + ", ".join(missing_sections)))

    checkpoint_match = re.search(r"### 🔴 CHECKPOINT：先停下的红灯\n\n(.*?)\n\n### 输出骨架", text, flags=re.S)
    red_light_count = 0
    branch_count = 0
    if checkpoint_match:
        checkpoint_text = checkpoint_match.group(1)
        red_light_count = len(re.findall(r"^\d+\. \*\*.*红灯\*\*", checkpoint_text, flags=re.M))
        branch_count = len(re.findall(r"如果.+?→", checkpoint_text))
    checks.append(ok("红灯检查点", f"{red_light_count} 类") if red_light_count >= 4 else fail("红灯检查点", f"{red_light_count} 类，少于 4 类"))
    checks.append(ok("失败分支", f"{branch_count} 条") if branch_count >= 6 else fail("失败分支", f"{branch_count} 条，少于 6 条"))

    output_match = re.search(r"### 输出骨架\n\n(.*?)\n\n## 身份卡", text, flags=re.S)
    output_steps = 0
    if output_match:
        output_steps = len(re.findall(r"^\d+\. \*\*", output_match.group(1), flags=re.M))
    checks.append(ok("输出骨架", f"{output_steps} 步") if output_steps >= 5 else fail("输出骨架", f"{output_steps} 步，少于 5 步"))

    boundary_bullets = 0
    boundary_match = re.search(r"## 诚实边界\n\n(.*?)\n\n## 附录", text, flags=re.S)
    if boundary_match:
        boundary_bullets = len(re.findall(r"^- ", boundary_match.group(1), flags=re.M))
    checks.append(ok("诚实边界", f"{boundary_bullets} 条") if boundary_bullets >= 3 else fail("诚实边界", f"{boundary_bullets} 条，少于 3 条"))

    research_files = [RESEARCH / f"{i:02d}-{name}.md" for i, name in [
        (1, "writings"),
        (2, "conversations"),
        (3, "expression-dna"),
        (4, "external-views"),
        (5, "decisions"),
        (6, "timeline"),
    ]]
    missing_files = [str(path.relative_to(ROOT)) for path in research_files if not path.exists() or path.stat().st_size < 1000]
    checks.append(ok("六个研究文件", "全部存在且非空") if not missing_files else fail("六个研究文件", "缺失或过小：" + ", ".join(missing_files)))

    residual = []
    for path in research_files:
        if path.exists() and "状态：待 Agent" in path.read_text(encoding="utf-8"):
            residual.append(str(path.relative_to(ROOT)))
    checks.append(ok("占位残留", "未发现") if not residual else fail("占位残留", "残留：" + ", ".join(residual)))

    source_links = len(re.findall(r"https?://", text))
    checks.append(ok("来源链接", f"{source_links} 个") if source_links >= 8 else fail("来源链接", f"{source_links} 个，少于 8 个"))

    print("# Quality Check")
    failed = False
    for name, passed, detail in checks:
        status = "PASS" if passed else "FAIL"
        print(f"- {status}: {name} - {detail}")
        failed = failed or not passed

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
