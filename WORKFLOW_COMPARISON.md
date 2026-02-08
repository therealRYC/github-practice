# Claude Code Workflows: A Comparison Guide

A guide for working across multiple machines (work desktop, home desktop, laptop)
using Claude Code with GitHub as the central sync point.

---

## Table of Contents

1. [Quick Comparison Matrix](#quick-comparison-matrix)
2. [Workflow 1: Pure Terminal (CLI)](#workflow-1-pure-terminal-cli)
3. [Workflow 2: VS Code Extension](#workflow-2-vs-code-extension)
4. [Workflow 3: Cursor IDE](#workflow-3-cursor-ide)
5. [Workflow 4: Claude Desktop App](#workflow-4-claude-desktop-app)
6. [Workflow 5: Cloud Sessions & Teleport](#workflow-5-cloud-sessions--teleport)
7. [Workflow 6: JetBrains IDEs](#workflow-6-jetbrains-ides)
8. [GitHub as the Cross-Machine Backbone](#github-as-the-cross-machine-backbone)
9. [How to Start Each Session](#how-to-start-each-session)
10. [Managing Pull Requests Across Devices](#managing-pull-requests-across-devices)
11. [Recommended Multi-Machine Setup](#recommended-multi-machine-setup)
12. [Subscription Requirements](#subscription-requirements)

---

## Quick Comparison Matrix

| Feature | CLI (Terminal) | VS Code | Cursor | Desktop App | Cloud (`&`) | JetBrains |
|---------|---------------|---------|--------|-------------|-------------|-----------|
| **Visual diffs** | No (text only) | Yes | Yes | Yes | Via web UI | Yes |
| **Runs locally** | Yes | Yes | Yes | Yes | No (cloud VM) | Yes |
| **Async / background** | No | No | No | Yes (remote) | Yes | No |
| **Multi-machine sync** | Manual (Git) | Manual (Git) | Manual (Git) | Remote sessions | Native | Manual (Git) |
| **Needs IDE** | No | Yes | Yes | No | No | Yes |
| **Scriptable / CI-friendly** | Yes | No | No | No | Partial | No |
| **Teleport support** | Yes (receive) | No | No | No | Yes (send) | No |
| **Parallel sessions** | Multiple tabs | Multiple tabs | Multiple tabs | Worktree-based | Multiple `&` | Multiple tabs |
| **OS support** | macOS, Linux, Windows (WSL) | macOS, Linux, Windows | macOS, Linux, Windows | macOS only | Any (web-based) | macOS, Linux, Windows |
| **Best for** | Power users, scripting | Visual code review | Fast inline edits | Non-terminal users | Cross-machine work | JetBrains users |

---

## Workflow 1: Pure Terminal (CLI)

### What it is
The foundational Claude Code experience. You type `claude` in any terminal and interact
via natural language. Claude can read your codebase, edit files, run commands, and manage Git.

### Setup (per machine)
```bash
# Install (macOS / Linux)
curl -fsSL https://claude.ai/install.sh | bash

# Windows (PowerShell)
irm https://claude.ai/install.ps1 | iex

# Authenticate
claude   # follow browser-based sign-in prompt
```

### Key capabilities
- **Plan mode**: Ask Claude to plan before implementing. Review the plan, then approve.
- **Extended thinking**: Toggle on deeper reasoning for complex tasks (best for debugging and architecture).
- **CLAUDE.md**: Project-level instructions Claude reads automatically (this repo has one).
- **Slash commands**: Custom commands in `.claude/commands/` for repeatable workflows.
- **Session resume**: `claude --continue` resumes the last session; `claude --resume` picks from past sessions.
- **MCP servers**: Connect to external tools (databases, browsers, APIs) via `claude mcp add`.
- **Hooks**: Auto-run formatters, linters, or checks after edits via `.claude/settings.json`.
- **Unix composability**: Pipe data in, chain with other tools, use in CI/CD.

### Strengths
- Maximum control -- you see everything Claude does.
- Works in any terminal on any OS.
- Scriptable: `claude -p "explain this function"` works in scripts and pipelines.
- No IDE dependency. Works over SSH, in tmux, on remote servers.
- Lightweight. No GUI overhead.

### Weaknesses
- Diffs are shown as terminal text, not visual side-by-side.
- Requires comfort with the command line.
- Conversation history stored locally in `~/.claude/` -- does not sync across machines.

### Cross-machine strategy
- Git push/pull is your sync mechanism for code changes.
- Conversations do not sync across machines. On the **same machine**, use `claude --continue`
  to resume your last session, or `claude --resume` to pick from past sessions.
- For cross-machine continuity, commit + push from machine A, pull on machine B,
  start a fresh Claude session. Or start tasks as cloud sessions (`&`) -- see Workflow 5.

---

## Workflow 2: VS Code Extension

### What it is
An official Anthropic extension that embeds Claude Code inside VS Code. Same agent,
same capabilities, but with IDE-native affordances.

### Setup (per machine)
1. Install VS Code (if not already installed).
2. Open Extensions (`Cmd+Shift+X` / `Ctrl+Shift+X`).
3. Search "Claude Code" -- make sure the publisher is **Anthropic**.
4. Click Install. Restart VS Code if prompted.
5. Sign in with your Anthropic account.

### Key capabilities
- **Inline diff viewer**: Changes appear as visual diffs in the editor.
- **@-mentions**: Reference specific files or selections in your prompts.
- **Auto-accept mode**: Let Claude apply edits in real-time.
- **Multi-tab conversations**: Multiple Claude sessions in separate tabs.
- **MCP support**: Connect to external tools (browsers, databases, APIs).

### Strengths
- Visual diffs make reviewing Claude's changes much easier.
- Tight integration with VS Code's file explorer, diagnostics, and terminal.
- Lower barrier to entry than pure terminal for many developers.
- Also works with VS Code forks (Cursor, Windsurf, VSCodium).

### Weaknesses
- Tied to VS Code (or a compatible fork).
- Common "No available IDEs detected" error, especially on WSL.
- Slightly heavier than pure terminal.
- Not scriptable for CI/CD like the CLI.

### Cross-machine strategy
- VS Code Settings Sync can sync extension config, but not Claude conversations.
- Same as CLI: commit + push to sync code, start fresh sessions on other machines.

---

## Workflow 3: Cursor IDE

### What it is
Cursor is a VS Code fork with its own built-in AI features (Tab autocomplete, Composer,
Chat). Claude Code can be installed as an extension inside Cursor, giving you both
Cursor's AI and Claude Code simultaneously.

### Setup (per machine)
```bash
# Method 1: Extensions marketplace (may not work automatically)
# Open Cursor > Extensions > Search "Claude Code" > Install

# Method 2: Manual install (more reliable)
cursor --install-extension \
  ~/.claude/local/node_modules/@anthropic-ai/claude-code/vendor/claude-code.vsix
```

### When to use which tool (Cursor AI vs Claude Code)
- **Cursor AI**: Fast inline autocomplete, quick single-file edits, exploratory coding.
- **Claude Code**: Deep codebase analysis, multi-file refactors, test generation, Git automation.
- A useful mental model: "Cursor nudges toward convergence (getting code written fast),
  Claude Code nudges toward exploration (understanding and thoroughness)."

### Strengths
- Best-of-both-worlds if you value real-time autocomplete AND deep reasoning.
- Visual diffs from the Claude Code extension.
- All the capabilities of the VS Code extension.

### Weaknesses
- Installation can be finicky (auto-detection issues).
- Two AI subscriptions: Cursor Pro ($20/month) + Claude Pro/Max.
- Having two AI assistants can be confusing without discipline about which to use when.

### Cross-machine strategy
- Same as VS Code: Git is your sync mechanism, conversations are local.

---

## Workflow 4: Claude Desktop App

### What it is
A native desktop application that provides a GUI for Claude Code without requiring
a terminal or IDE. Includes diff review, parallel sessions via Git worktrees,
remote session management, and one-click integrations (connectors).

### Setup
1. Download from claude.com/download.
2. Install and sign in.
3. Open a project folder and start working.

### Key capabilities
- **Parallel sessions with Git worktrees**: Each session gets an isolated working copy.
- **Diff review**: Visual file-by-file diff viewer. Comment on specific lines for revisions.
- **Plan mode**: Review Claude's plan before implementation.
- **Remote sessions**: Launch long-running tasks on Anthropic cloud VMs.
- **Connectors**: One-click connections to Slack, GitHub, Linear, Notion, Google Calendar, etc.

### Local vs Remote sessions (important distinction)

The Desktop app offers **two kinds** of sessions:

| | Local session | Remote session |
|---|---|---|
| **Runs on** | Your machine | Anthropic cloud VM |
| **Uses your tools** | Yes (your R, Python, Node, etc.) | No (cloud environment only) |
| **Persists after closing app** | No | Yes |
| **Worktree isolation** | Yes (for Git repos) | Yes |
| **Resource usage** | Your CPU/RAM | Cloud resources |

**Local sessions** are the default. They use your machine's files and installed tools
directly. Multiple local sessions on the same Git repo each get their own worktree,
so they won't conflict.

**Remote sessions** run on Anthropic's infrastructure. They're useful for long-running
tasks you want to continue after closing the app, but the cloud environment may not
have specialized tools (e.g., R with your packages) installed.

### Strengths
- Most accessible entry point -- no terminal or IDE knowledge needed.
- Visual diff review is excellent.
- Local parallel sessions use worktree isolation without conflicts.
- Remote sessions mean you can close the app and check back later.

### Weaknesses
- **macOS only** as of February 2026. Windows support is on the roadmap.
- Less flexible than CLI for scripting and automation.
- Connectors require granting access to third-party services.
- Remote sessions may lack specialized tools you have locally (R packages, etc.).

### Cross-machine strategy
- Remote sessions run on Anthropic's cloud and can be accessed from any Mac where
  you are logged into your Anthropic account.
- Local sessions are machine-specific and do not sync.
- Use `CLAUDE.md` as your cross-machine memory — ask Claude to update it with session
  notes before wrapping up (see the Workflow Guide for details).

---

## Workflow 5: Cloud Sessions & Teleport

### What it is
Cloud sessions (`&`) offload Claude Code tasks to Anthropic-managed VMs. Your repo is
cloned, the task runs asynchronously, and changes are pushed to a branch. You can
monitor progress from any device and "teleport" the session to your local terminal.

**This is the primary mechanism for seamless cross-machine work.**

### How to use

```bash
# From the CLI (interactive mode) -- prefix with &
& Fix the divide function in calculator.py to handle division by zero

# From the command line directly
claude --remote "Fix the divide function"

# Multiple parallel tasks
& Add a factorial function with tests
& Add a fibonacci function with tests
```

### Monitoring
- `/tasks` in the Claude Code CLI -- shows all background sessions.
- Press `t` in the tasks view to **teleport** into a running or completed session.
- Also viewable on claude.ai and the Claude iOS app.

### Teleportation explained
Teleportation moves an entire conversation (context, history, working branch) from
the cloud to your local terminal.

```bash
# Teleport a specific session
claude --teleport <session-id>

# Or use /tasks and press 't'
```

**Requirements for teleporting:**
1. Clean Git state (no uncommitted changes).
2. You must be in a checkout of the same repository.
3. The cloud session's branch must be pushed to the remote.
4. You must be authenticated as the same claude.ai user.

**Important limitation**: Teleportation is currently **one-way only** (cloud to local).
You cannot push a local session to the cloud. If you think you might switch machines,
start with `&` from the beginning.

### Strengths
- True async: launch a task and walk away.
- Monitor from any device (desktop, web, phone).
- Teleport brings full conversation context to any machine.
- Multiple parallel tasks at once.
- No local compute needed for task execution.

### Weaknesses
- **GitHub only** -- does not work with GitLab, Bitbucket, or self-hosted Git.
- **One-way teleport** -- cannot push local sessions to cloud.
- **`&` always creates a new session** -- cannot send an existing conversation to the cloud.
- Requires the Claude GitHub App installed on the repository.
- Requires a clean Git state to teleport.

### Cross-machine strategy
This IS the cross-machine strategy:
1. Start a cloud session on your **work desktop**: `& implement feature X`
2. Monitor on your **phone** during commute (claude.ai or iOS app).
3. Teleport into your **home desktop**: `/tasks` then press `t`.
4. Continue working locally with full conversation context.

---

## Workflow 6: JetBrains IDEs

### What it is
A Claude Code plugin for JetBrains IDEs (IntelliJ, PyCharm, WebStorm, etc.).
Similar to the VS Code extension but for the JetBrains ecosystem.

### Setup
1. Open your JetBrains IDE.
2. Go to Settings > Plugins > Marketplace.
3. Search "Claude Code" and install.
4. Restart the IDE and sign in.

### Strengths
- Native integration with JetBrains' powerful refactoring and navigation tools.
- Good option if JetBrains is your preferred IDE.

### Weaknesses
- Currently in beta.
- Same local-only conversation limitations as VS Code.

---

## GitHub as the Cross-Machine Backbone

Regardless of which workflow you choose, **GitHub is your sync mechanism** for working
across machines. Here is the basic Git workflow that ties everything together:

### Clone vs Pull (important distinction)

These are different operations that beginners often confuse:

- **Clone** = download the entire repository for the first time. You do this **once
  per machine**. After that, the repo lives on your machine.
- **Pull** = update your existing local copy with the latest changes from GitHub.
  Quick and lightweight — only downloads what changed. You do this **every time you
  sit down**.

### Essential Git commands for multi-machine work

```bash
# On machine A: save your work
git add -A
git commit -m "describe what you did"
git push origin your-branch-name

# On machine B: pick up where you left off
git pull origin your-branch-name
claude   # start a new Claude session with full codebase context
```

### Setting up a new machine
```bash
# 1. Install Git
# macOS: comes pre-installed, or `brew install git`
# Linux: `sudo apt install git` or `sudo dnf install git`
# Windows: download from git-scm.com

# 2. Configure your identity (once per machine)
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# 3. Authenticate with GitHub
gh auth login   # if using GitHub CLI (recommended)
# Or set up SSH keys: https://docs.github.com/en/authentication

# 4. Clone your repo
git clone https://github.com/yourname/your-repo.git
cd your-repo

# 5. Install Claude Code
curl -fsSL https://claude.ai/install.sh | bash
claude   # sign in
```

### Branching strategy for multi-machine work
- Use **feature branches** so work-in-progress does not affect `main`.
- Push frequently -- even if the code is not done. This is your sync mechanism.
- Use descriptive branch names: `feature/add-statistics-module`, `fix/divide-by-zero`.
- When ready, create a **pull request** on GitHub to merge into `main`.

---

## How to Start Each Session

The most important habit for multi-machine work: **always pull when you sit down,
always push when you stand up.** Beyond that, the steps differ depending on whether
you're starting something new or continuing existing work.

### Starting a brand new project (do once, on any machine)

```bash
# 1. Create a folder and initialize Git
mkdir my-project
cd my-project
git init

# 2. Create at least one file (even a placeholder)
echo "# My Project" > README.md

# 3. First commit
git add README.md
git commit -m "Initial commit"

# 4. Create the repo on GitHub and push
gh repo create my-project --public --source . --push
#   use --private instead of --public for private repos

# 5. Start Claude Code
claude
```

Then on your **other machines**, clone it once:
```bash
git clone https://github.com/yourname/my-project.git
cd my-project
claude
```

That's it. The repo now exists on all machines and on GitHub.

### Starting a session on an existing project (daily routine)

Every time you sit down at any machine:

```bash
cd my-project
git pull origin main          # grab latest changes from GitHub
claude                        # start Claude Code
```

That `git pull` is the critical step -- it ensures you have whatever was pushed
from your other machines.

### Ending a session (before walking away)

```bash
# Inside Claude Code, ask it to commit:
> Commit my changes with a descriptive message

# Then push
git push origin main

# Or if you're on a feature branch:
git push origin feature/my-branch
```

### Working on a feature branch (recommended for non-trivial work)

Branches keep `main` clean while you work on something:

```bash
# Starting a new branch
cd my-project
git pull origin main
git checkout -b feature/add-login    # create a branch
claude
# ... do your work, commit along the way ...
git push origin feature/add-login    # push the branch

# When the feature is done: create a PR on GitHub to merge into main
```

Continuing that branch on another machine:
```bash
cd my-project
git fetch origin                          # download branch info from GitHub
git checkout feature/add-login            # switch to the branch
git pull origin feature/add-login         # get latest changes on it
claude                                    # continue working
```

### Using cloud sessions to bridge machines mid-task

If you know you'll switch machines during a task, start with `&`:

```bash
cd my-project
git pull origin main
claude
> & Implement the login page with form validation and tests
```

Later, on a different machine:
```bash
cd my-project
claude
> /tasks          # see your cloud sessions, press 't' to teleport
```

### Quick reference: which start sequence?

| Scenario | Steps |
|----------|-------|
| **Brand new project** | `git init` > first commit > `gh repo create` > `clone` on other machines |
| **Sitting down at any machine** | `git pull` > `claude` |
| **Walking away from any machine** | Commit > `git push` |
| **Starting a new feature** | `git pull origin main` > `git checkout -b feature/name` > `claude` |
| **Continuing a feature on another machine** | `git fetch` > `git checkout feature/name` > `git pull` > `claude` |
| **Switching machines mid-task** | Start with `& task` > teleport on other machine via `/tasks` + `t` |
| **Picking up a cloud session result** | `git fetch` > `git checkout` the branch it created > review changes |

---

## Managing Pull Requests Across Devices

You don't need to memorize `gh` commands. The most seamless approach is to let
Claude Code run them for you using natural language -- but you need `gh` installed
and authenticated on each machine so Claude has something to call.

### One-time setup: install `gh` on every machine

```bash
# macOS
brew install gh

# Ubuntu / Debian
sudo apt install gh

# Windows (PowerShell)
winget install GitHub.cli

# Then authenticate (once per machine)
gh auth login
# Choose: GitHub.com > HTTPS > Login with a web browser
# Follow the prompts -- this gives gh (and Claude) permission to manage PRs
```

**Verify it works:**
```bash
gh auth status
# Should show: Logged in to github.com as yourname
```

### The seamless workflow: just ask Claude

Once `gh` is installed, you never need to remember the commands yourself.
Inside any Claude Code session (terminal, VS Code, Cursor, etc.), just ask
in natural language:

```
> Create a pull request for this branch
> What PRs are open right now?
> Show me the checks on PR #12
> Merge the PR for feature/add-login
> What comments are on PR #5?
> Close PR #3, we're not doing that anymore
```

Claude translates these into the right `gh` commands and runs them for you.
This works identically on every machine -- work desktop, home desktop, laptop --
as long as `gh` is installed and authenticated.

### What Claude does behind the scenes

When you ask Claude to manage PRs, it runs `gh` commands like these. You don't
need to memorize them, but it helps to know what's happening:

| You say | Claude runs |
|---------|-----------|
| "Create a PR" | `gh pr create --title "..." --body "..."` |
| "What PRs are open?" | `gh pr list` |
| "Show me PR #12" | `gh pr view 12` |
| "What are the checks on PR #12?" | `gh pr checks 12` |
| "Merge PR #12" | `gh pr merge 12` |
| "Show comments on PR #5" | `gh api repos/owner/repo/pulls/5/comments` |
| "Close PR #3" | `gh pr close 3` |
| "Create a repo for this project" | `gh repo create name --source . --push` |

### What happens automatically vs what you do

| Situation | What happens | What you need to do |
|-----------|-------------|-------------------|
| **Cloud session (`&`) finishes** | Branch is pushed automatically. PR may be created automatically. | Review the PR on GitHub or ask Claude: "Show me the PR from that cloud session" |
| **Terminal session: ready to merge** | Nothing automatic -- you're in control. | Ask Claude: "Create a PR for this branch" |
| **PR needs review** | Nothing automatic. | Ask Claude: "Show me the diff on PR #7" or review on GitHub web |
| **PR is approved** | Nothing automatic. | Ask Claude: "Merge PR #7" or click Merge on GitHub web |
| **PR has failing checks** | Nothing automatic. | Ask Claude: "What checks failed on PR #7?" then fix the issues |

### When to use the GitHub web UI instead

While `gh` via Claude handles most operations, the GitHub web UI is better for some tasks:

- **Reviewing large diffs**: The web UI's side-by-side diff viewer with syntax highlighting
  is easier to read than terminal output for big changes.
- **Line-by-line code review comments**: The web UI lets you click a line and leave a comment
  directly on that line of code. `gh` cannot do this.
- **Managing repository settings**: Branch protection rules, collaborator access, webhooks.
- **Browsing PR conversations**: Long discussions with multiple reviewers are easier to
  follow in the web UI.
- **Merge conflict resolution**: GitHub's web editor for simple conflicts is convenient.

**Rule of thumb**: Use Claude + `gh` for actions (create, merge, check status).
Use the GitHub web UI for visual review and discussion.

### Cross-machine PR scenario

Here's how a PR flows across your machines:

```
WORK DESKTOP (morning):
  $ claude
  > Create a branch and implement the new search feature
  > ... Claude works, makes commits ...
  > Push this branch and create a PR
  # Claude runs: git push, then gh pr create

LAPTOP (lunch break):
  $ claude
  > What's the status of my open PRs?
  # Claude runs: gh pr list
  # You see: PR #14 "Add search feature" -- checks passing

HOME DESKTOP (evening):
  $ claude
  > Show me PR #14
  # Claude runs: gh pr view 14
  > Looks good, merge it
  # Claude runs: gh pr merge 14
  > Pull main so we're up to date
  # Claude runs: git pull origin main
```

Every step uses the same natural language. Every machine has the same capabilities
because `gh` is installed and authenticated on all of them.

---

## Recommended Multi-Machine Setup

### Minimum viable setup (all platforms)
1. Install Git and GitHub CLI (`gh`) on all machines.
2. Install Claude Code CLI on all machines.
3. Authenticate both `gh` and `claude` on each machine.
4. Clone your repos to each machine.
5. Use `git push` / `git pull` to sync code between machines.
6. Use `&` (cloud sessions) for tasks you want to access from multiple machines.

### Recommended setup for your situation (3 machines)

| Component | Work Desktop | Home Desktop | Laptop |
|-----------|-------------|-------------|--------|
| **Git + GitHub CLI** | Install | Install | Install |
| **Claude Code CLI** | Install | Install | Install |
| **Editor** | VS Code + Claude extension | VS Code + Claude extension | VS Code + Claude extension |
| **Claude GitHub App** | Install once (account-level) | Already active | Already active |

### Daily workflow example
```
MORNING (work desktop):
  $ cd my-project
  $ git pull origin main
  $ claude
  > "Let's work on the authentication feature"
  > ... make progress ...
  > /commit  (or ask Claude to commit)
  $ git push origin feature/auth

COMMUTE (phone):
  - Check claude.ai for any cloud session results
  - Review PRs on GitHub mobile app

EVENING (home desktop):
  $ cd my-project
  $ git pull origin feature/auth
  $ claude
  > "Let's continue the auth feature -- we left off at ..."
  > ... continue working ...
  $ git push origin feature/auth

ASYNC TASKS (from any machine):
  $ claude
  > & Add comprehensive tests for the auth module
  > & Update the README with new API docs
  # These run in the cloud. Check /tasks from any machine later.
```

---

## Subscription Requirements

| Plan | Monthly Cost | Claude Code | Cloud Sessions (`&`) | GitHub Actions |
|------|-------------|-------------|---------------------|----------------|
| **Free** | $0 | No | No | No |
| **Pro** | $20 | Yes | Yes | Yes (with API key) |
| **Max 5x** | $100 | Yes (higher limits) | Yes (higher limits) | Yes (with API key) |
| **Max 20x** | $200 | Yes (highest limits) | Yes (highest limits) | Yes (with API key) |
| **API only** | Usage-based | Yes | No | Yes |

**Recommendation**: Start with **Pro** ($20/month). Upgrade to **Max** if you hit
usage limits regularly. The Max plan at $100-200/month is significantly cheaper than
equivalent API usage for heavy developers.

---

## Summary: Which Workflow When?

| If you want to... | Use this |
|-------------------|----------|
| Maximum control, scripting, CI/CD | **CLI (Terminal)** |
| Visual diffs and IDE integration | **VS Code Extension** |
| Real-time autocomplete + deep reasoning | **Cursor + Claude Code** |
| No terminal, visual-first experience | **Claude Desktop App** |
| Work across multiple machines seamlessly | **Cloud Sessions (`&`)** |
| Async tasks that run while you sleep | **Cloud Sessions (`&`)** |
| JetBrains-native experience (IntelliJ, PyCharm, etc.) | **JetBrains Plugin** |
| Automate PR reviews and issue triage | **GitHub Actions** |

The workflows are not mutually exclusive. Many developers use the CLI for quick tasks,
VS Code for focused coding sessions, and cloud sessions for async/cross-machine work.
