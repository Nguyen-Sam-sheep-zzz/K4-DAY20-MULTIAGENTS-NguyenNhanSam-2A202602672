"""GUIDE Phần 1 - Định nghĩa subagent (tác tử con).   >>> SINH VIÊN CÀI ĐẶT <<<

Pseudo-code: guides/pseudocode/02_subagents.md
Kiểm tra:    pytest tests/test_02_agent.py
"""


def get_subagents() -> list[dict]:
    """Trả về danh sách subagent (ít nhất 2, tên khác nhau).

    Mỗi phần tử là một dict có các khóa bắt buộc:
      "name":          tên duy nhất (chữ thường, có thể có dấu gạch ngang)
      "description":   khi nào tác tử chính nên giao việc cho subagent này (viết như một hướng dẫn hành động)
      "system_prompt": chỉ dẫn cho subagent
    Gợi ý vai trò: explorer (đọc và báo cáo), implementer (thực hiện), reviewer (kiểm tra độc lập).
    """
    return [
        {
            "name": "explorer",
            "description": (
                "Use before a non-trivial change when you need to inspect README files, "
                "docstrings, data or log formats, and identify requirements and edge cases. "
                "Send the complete task rules and relevant file paths."
            ),
            "system_prompt": (
                "You inspect specifications and existing files without modifying them. "
                "Use the delegated task rules, README files and docstrings as evidence. "
                "For code, trace shared functions and distinguish root causes from symptoms. "
                "For data or logs, inspect formats, missing values, duplicates and time zones. "
                "Return a concise checklist of requirements, relevant paths, evidence and "
                "edge cases for the main agent. Clearly identify anything not verified."
            ),
        },
        {
            "name": "reviewer",
            "description": (
                "Use after implementation or output generation to independently check "
                "the results against all task rules, docstrings and edge cases. "
                "Send the complete task rules and the paths of the changed or created files."
            ),
            "system_prompt": (
                "You review independently without modifying files. Read the delegated "
                "requirements and inspect the actual files before judging correctness. "
                "Run available tests or small Python checks and report their actual outcomes. "
                "Check output structure, data cleaning, time handling and boundary cases "
                "when relevant. Verify the main agent's completion claims against the files. "
                "Return concrete failures with paths and evidence, and list any unchecked "
                "requirements. Do not claim success for checks you did not run."
            ),
        },
    ]
