---
name: typed-regression-maintenance
description: Use when modifying a typed package to fix multiple behavioral bugs.
---
- Add type annotations to every parameter and return value of each public function.
- Add `tests/test_regressions.py`.
- Create one test function for each bug fixed.
- Ensure the regression test file contains at least three regression tests when three or more bugs are fixed.
- Record every fix in `CHANGELOG.md` under `## Unreleased`.
- Format each changelog entry as `- fix(<function name>): <short description>`.
- Run the complete test suite using the package's required import path configuration.
- Confirm collection succeeds and all tests pass.
