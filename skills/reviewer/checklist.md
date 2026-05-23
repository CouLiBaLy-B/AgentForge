---
name: code_review_checklist
description: "Standard checklist for reviewing PRs"
tags: [review, quality, security]
---
# Code Review Skill

## Checklist
1. **Logic**: Does the code do what it's supposed to?
2. **Security**: No hardcoded secrets? Input validation?
3. **Tests**: Are there new tests for the new logic?
4. **Style**: Consistent with the codebase?

## Output
Write the results to `/workspace/REVIEW.md`.
Use 🟢 for pass, 🟡 for warning, 🔴 for critical issues.
