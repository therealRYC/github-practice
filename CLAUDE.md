# CLAUDE.md — GitHub Practice Project Context

## What This Project Is

A practice repo for learning Claude Code cloud sessions (`&`) and teleport (`/tasks` + `t`). Contains a simple Python calculator module with intentional bugs and incomplete tests.

**GitHub repo**: https://github.com/therealRYC/github-practice
**Author**: Robert Chen (robchen@uw.edu, GitHub: therealRYC)
**Lab**: Fowler Lab, UW

---

## Project Status

- **Repo created and pushed to GitHub**: yes
- **Claude GitHub App installed**: yes — but `&` commands still fail (see Known Issues below)
- **Exercises completed**: none yet

---

## Files

| File | Purpose |
|------|---------|
| `calculator.py` | Simple calculator with 3 intentional bugs |
| `test_calculator.py` | Incomplete tests (only covers add, subtract, multiply) |
| `CLAUDE_WORKFLOW_GUIDE.md` | Practical playbook for using Claude Code effectively (plan mode, worktrees, verification) |
| `WORKFLOW_COMPARISON.md` | Comparison of all Claude Code interfaces (CLI, VS Code, Cursor, Desktop, Cloud, JetBrains) |
| `BACKGROUND_TASKS_&_TROUBLESHOOTING.md` | Troubleshooting guide for `&` background task failures |
| `PRACTICE_EXERCISES.md` | 5 step-by-step exercises for practicing `&` and teleport |
| `.gitignore` | Standard Python ignores |

## Known Bugs in calculator.py (intentional, for practice)

1. `divide()` — no zero-division handling
2. `power()` — doesn't handle negative exponents
3. `average()` — crashes on empty list

## Missing Test Coverage

`test_calculator.py` has no tests for `divide`, `power`, or `average`.

---

## Cloud Sessions (`&`) — How It Works

### What `&` does
Prefixing a message with `&` creates a new session on claude.ai that runs on Anthropic-managed VMs. Your repo is cloned, the task runs asynchronously, and changes are pushed to a branch.

### Requirements
- **Subscription**: Pro, Max, Team premium, or Enterprise premium
- **GitHub**: Account connected + Claude GitHub App installed on the repo
- **Clean git state** for teleporting sessions back to terminal

### Basic usage
```
& Fix the divide function in calculator.py to handle division by zero
```

### Multiple parallel tasks
```
& Add a factorial function to calculator.py with tests
& Add a fibonacci function to calculator.py with tests
```

### From command line
```bash
claude --remote "Fix the divide function"
```

### Monitoring and teleporting
- `/tasks` — check progress on all background sessions
- Press `t` in tasks view to teleport into a session
- Can also monitor from claude.ai or Claude iOS app

### Limitations
- Only works with GitHub repos (not GitLab, etc.)
- `&` always creates a new session (can't push existing conversation to cloud)
- Must be on same claude.ai account to teleport

---

## Claude GitHub App Setup

The Claude GitHub App gives Claude Code permission to clone repos, create branches, and push changes in cloud sessions.

### How to install
1. First time you use `&`, Claude Code should prompt you to install it
2. Or: GitHub → Settings → Integrations → Applications → find "Claude" → configure repository access

### Access options
- **All repositories** — grants access to everything (easiest if using `&` often)
- **Select repositories** — grant per-repo, add more later as needed

### Permissions it gets
Read/write access to code and pull requests in authorized repos.

---

## Known Issues with `&` / Remote Sessions

As of 2026-02-07, the `&` command fails with:
```
Failed to create background session: Failed to create remote session.
Try running /login and signing in with a claude.ai account (not Console).
```
Re-running `/login` does not fix it. This is a widely reported bug — see these GitHub issues:
- [#16831](https://github.com/anthropics/claude-code/issues/16831) — Remote sessions failing intermittently
- [#23927](https://github.com/anthropics/claude-code/issues/23927) — Can't create remote session despite Team account
- [#18409](https://github.com/anthropics/claude-code/issues/18409) — CLI can't start remote session until repo is selected in web UI

### Workarounds to try
1. Go to **https://claude.ai/code**, select this repo from the dropdown — this registers the repo on the backend (see `BACKGROUND_TASKS_&_TROUBLESHOOTING.md` for details). **Status**: tried once without success; may require retry or combining with steps below.
2. Use `claude --remote "task"` from the shell instead of `&` inside a session
3. Uninstall and reinstall the Claude GitHub App from GitHub → Settings → Applications
4. Run `claude --debug` (has helped some users succeed on first attempt)
5. Run `/logout`, close Claude Code, restart, and re-authenticate
6. Full auth reset: delete `~/.claude/.credentials.json`, restart Claude Code, `/login`, then select repo in web UI and retry

---

## Practice Exercises (summary)

Each exercise has both cloud (`&`) and local alternatives, so you can practice
regardless of whether remote sessions are working.

1. **Fix a bug** — fix divide-by-zero (cloud or local branch)
2. **Add missing tests** — write tests for untested functions
3. **Plan Mode** — practice planning before executing
4. **Parallel sessions** — run multiple Claude instances with worktrees
5. **Plan + parallel execution** — plan in CLI, execute in parallel (Pattern D)
6. **Cross-machine memory** — practice CLAUDE.md session handoffs

See `PRACTICE_EXERCISES.md` for full details.

---

## Git Config

Git identity is configured globally:
- `user.name`: Robert Chen
- `user.email`: robchen@uw.edu
- GitHub CLI authenticated as `therealRYC` via HTTPS
