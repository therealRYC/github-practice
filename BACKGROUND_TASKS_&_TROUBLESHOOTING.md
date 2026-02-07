# Background Tasks (`&`) Troubleshooting Guide

## The Problem

The `&` command in Claude Code CLI fails with errors like:

```
Failed to create background session: Failed to create remote session.
Try running /login and signing in with a claude.ai account (not Console).
```

This happens **even when** all of the following are true:
- OAuth login via `/login` succeeds
- Valid credentials exist in `~/.claude/.credentials.json`
- Claude GitHub App is installed with full repository access
- Git remote is correctly configured
- Claude Code is up to date
- No `ANTHROPIC_API_KEY` environment variable is set

This is a **known bug** affecting users across macOS, Linux, and WSL2.

---

## Root Cause

There is a missing initialization/registration step on the backend that only gets triggered when using the **Claude Code web client** first. The CLI alone cannot properly register a repository for remote sessions, even with all prerequisites met.

---

## Solution (Confirmed Fix)

1. Go to **[https://claude.ai/code](https://claude.ai/code)** in your browser
2. Click on your repository from the **dropdown list**
3. You don't need to run anything — just selecting the repo is enough
4. Go back to your terminal and retry the `&` command

This "registers" the repo on the backend in a way the CLI currently does not.

---

## WSL2-Specific Issues

WSL2 users may encounter additional problems due to networking and OAuth callback routing.

### Fix: Switch to Mirrored Networking

Add this to `%USERPROFILE%/.wslconfig` on the Windows side:

```ini
[wsl2]
networkingMode=mirrored
```

Then from PowerShell (as Administrator):

```powershell
wsl --shutdown
```

Restart WSL2 and try again. This resolves OAuth callback failures where the browser completes auth but the token never reaches the CLI.

### Fix: Clock Skew

WSL2's clock can drift out of sync with Windows, causing OAuth validation failures. Check with:

```bash
date
```

If the time is wrong, resync:

```bash
sudo hwclock -s
```

Or from PowerShell, restart WSL2 entirely:

```powershell
wsl --shutdown
```

---

## Other Workarounds

### Run with `--debug` flag

Some users found that `claude --debug` allows background tasks to succeed when they otherwise fail. This suggests a race condition in the session creation flow.

### Full Auth Reset

If nothing else works:

```bash
rm ~/.claude/.credentials.json
rm -rf ~/.claude/
```

Then restart Claude Code, run `/login`, go to the web UI to select your repo, and retry `&`.

---

## Related GitHub Issues

| Issue | Description | Status |
|-------|-------------|--------|
| [#18409](https://github.com/anthropics/claude-code/issues/18409) | Can't start remote session until repo is selected in web UI | Open |
| [#16831](https://github.com/anthropics/claude-code/issues/16831) | Remote/background sessions failing intermittently | Open |
| [#16403](https://github.com/anthropics/claude-code/issues/16403) | Background task creation fails with session upload error | Closed (duplicate of #13087) |
| [#16443](https://github.com/anthropics/claude-code/issues/16443) | Background session creation fails to acknowledge on frontend | Closed (duplicate) |
| [#17459](https://github.com/anthropics/claude-code/issues/17459) | OAuth tokens not persisting across sessions | Open |
| [#20756](https://github.com/anthropics/claude-code/issues/20756) | OAuth authentication broken in WSL2 | Open |
| [#13087](https://github.com/anthropics/claude-code/issues/13087) | Background tasks fail to detect valid git repository | Open |

---

## Checklist Before Filing a New Issue

If none of the above fixes work, file an issue at [github.com/anthropics/claude-code/issues](https://github.com/anthropics/claude-code/issues) and include:

- [ ] Output of `claude --version`
- [ ] Output of `claude /doctor` (if available)
- [ ] Output of `claude --debug` with the `&` command
- [ ] Your OS and environment (WSL2, native Linux, macOS)
- [ ] Contents of `~/.claude/.credentials.json` (redact tokens)
- [ ] Output of `git remote -v`
