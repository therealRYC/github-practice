# Claude Code Workflow Guide

A practical playbook for using Claude Code effectively, inspired by how Boris Cherny
(creator of Claude Code) and his team actually work.

This guide focuses on the **CLI + web app combo** — how to run parallel sessions,
plan before executing, teach Claude your preferences, and build reusable workflows.
If you're newer to git, don't worry — key concepts are explained as we go.

**Who this is for**: Researchers and developers who want to get more out of Claude Code,
whether you're just starting or looking to level up.

**Sources**:
- [Boris's personal workflow](https://x.com/bcherny/status/2007179832300581177)
- [10 tips from the Claude Code team](https://x.com/bcherny/status/2017742741636321619)
- [Workflow analysis (Substack)](https://karozieminski.substack.com/p/boris-cherny-claude-code-workflow)
- [InfoQ coverage](https://www.infoq.com/news/2026/01/claude-code-creator-workflow/)
- [Team tips writeup](https://paddo.dev/blog/claude-code-team-tips/)

---

## The Core Philosophy

Boris runs **5 terminal sessions** and **5-10 web sessions** simultaneously. That's not
showing off — it reflects a set of principles his team has converged on:

### Parallelization over optimization
Don't try to make one Claude session perfect. Run multiple sessions on independent tasks.
Think of Claude sessions like compute resources you distribute across problems.

### Plan first, execute second
Start every non-trivial task in **Plan Mode**. Go back and forth with Claude until you
like the plan. Only then switch to auto-accept mode. This prevents Claude from making
40 unintended changes before you notice.

### Let Claude self-improve
Maintain a `CLAUDE.md` file and update it whenever Claude makes a mistake. Over time,
Claude learns your preferences, style conventions, and project-specific rules. The team
updates theirs multiple times per week.

### Give Claude verification tools
Boris calls this "the most important thing." When Claude can run tests, check builds,
or verify its own output, the quality of results improves by **2-3x**. Always ask Claude
to verify, not just implement.

### Codify repetitive workflows
Anything you do more than twice should become a slash command. Boris uses `/commit-push-pr`
dozens of times daily. Your future self (and teammates) will thank you.

---

## Git Concepts You'll Need

If you're comfortable with branches and worktrees, skip to the next section.

### Branches (quick refresher)

A **branch** is an independent line of development. You create a branch, make changes on
it, then merge it back. This keeps your `main` branch clean while you experiment.

```bash
# Create and switch to a new branch
git checkout -b fix-divide-bug

# Do work, commit, then push
git add calculator.py
git commit -m "Fix divide-by-zero bug"
git push -u origin fix-divide-bug
```

Branches are fine for **sequential** work — finish one task, switch to the next.

### Git Worktrees

A **worktree** is a separate checkout of your repo in a different folder. Each worktree
can be on a different branch, and you can work in them simultaneously.

Think of it this way:
- **Branch alone**: one folder, switch between branches (only one active at a time)
- **Worktree**: multiple folders, each on its own branch (all active simultaneously)

```
your-repo/                     # main worktree (main branch)
├── .git/
├── calculator.py
└── ...

../your-repo-fix-divide/       # worktree 1 (fix-divide branch)
├── calculator.py
└── ...

../your-repo-add-tests/        # worktree 2 (add-tests branch)
├── calculator.py
└── ...
```

Boris's team runs **3-5 worktrees** simultaneously, each with its own Claude session.
This is how they achieve true parallelization without merge conflicts.

### Basic worktree commands

```bash
# Create a new worktree on a new branch
git worktree add ../my-repo-feature-x -b feature-x

# List all worktrees
git worktree list

# Remove a worktree after you're done (merge the branch first)
git worktree remove ../my-repo-feature-x
```

### When to use worktrees vs. just branches

| Situation | Use |
|-----------|-----|
| One task at a time | Branches are fine |
| Two+ tasks simultaneously with Claude sessions | Worktrees |
| Quick experiment you'll discard | Branch |
| Long-running parallel work | Worktrees |

**Tip**: The Claude Code team uses shell aliases for quick worktree switching:
`za` for worktree A, `zb` for worktree B, etc. They also color-code their terminal
tabs per worktree so they never lose track.

---

## Setting Up Your Environment

### Prerequisites

| Tool | How to get it |
|------|---------------|
| **git** | Likely already installed. Check with `git --version` |
| **GitHub CLI (`gh`)** | `brew install gh` (macOS) or [cli.github.com](https://cli.github.com) |
| **Claude Code CLI** | `curl -fsSL https://claude.ai/install.sh \| bash` (or `npm i -g @anthropic-ai/claude-code`) |
| **claude.ai account** | Pro or Max plan needed for cloud sessions (`&`) |

### Terminal setup

Any terminal works, but the Claude Code team uses **Ghostty** for its synchronized
rendering, 24-bit color, and proper Unicode support. On Windows/WSL, your existing
terminal (Windows Terminal, etc.) is fine.

Run `/statusline` inside Claude Code to enable a status bar showing your current git
branch and token usage — helpful when juggling multiple sessions.

### Claude GitHub App (needed for `&` cloud sessions)

The Claude GitHub App lets cloud sessions clone your repo, create branches, and push
changes.

1. First time you use `&` in Claude Code, it should prompt you to install it
2. Or install manually: GitHub → Settings → Integrations → Applications → "Claude"
3. Grant access to your repos (all repos or select specific ones)

---

## The Daily Workflow

Boris uses several patterns depending on the situation. Here they are, from simplest to
most advanced.

### Pattern A: Local Terminal Session

The most common pattern. One terminal, one task, focused work.

```bash
# 1. Pull latest changes
git pull

# 2. Start Claude Code
claude

# 3. Enter plan mode (Shift+Tab twice, or just say "plan first")
> Plan how to fix the divide function to handle zero division

# 4. Iterate on the plan until you're happy with it

# 5. Approve the plan, switch to auto-accept mode (Shift+Tab once)
#    Claude executes the plan

# 6. Verify
> Run the tests to make sure everything passes

# 7. Commit and push (or use a /commit-push-pr slash command)
```

**When to use**: Focused work on a single task. This is your bread and butter.

### Pattern B: Cloud Session (`&`)

Run a task asynchronously on Anthropic's servers. Great for tasks you want to fire and
forget, or when you'll switch devices.

```bash
# From inside Claude Code — prefix with &
> & Fix the divide function in calculator.py to handle division by zero

# Or from the command line directly
claude --remote "Fix the divide function to handle division by zero"
```

**Monitoring your cloud sessions**:
- Inside Claude Code: type `/tasks` to see all running sessions
- On the web: check claude.ai — your sessions appear there
- On your phone: the Claude iOS app shows active sessions

**Teleporting back**: When a cloud session finishes (or while it's running), you can
"teleport" into it from your terminal:
1. Type `/tasks` in Claude Code
2. Select the session
3. Press `t` to teleport — the session transfers to your terminal

**When to use**: Tasks you want to run while you do other things. Tasks you'll pick up
on a different device. Anything you'd otherwise wait around for.

### Pattern C: Parallel Local Sessions

Run multiple Claude instances at once, each working on a different task. This is the
biggest productivity unlock according to Boris's team.

**Simple version (different branches, same folder)**:
```bash
# Terminal 1
git checkout -b fix-divide
claude
> Fix the divide function...

# Terminal 2 (after Terminal 1's Claude is running)
git checkout -b add-tests
claude
> Add tests for the average function...
```

> **Warning**: This can cause conflicts if both sessions touch the same files.

**Better version (git worktrees)**:
```bash
# Create worktrees
git worktree add ../practice-fix-divide -b fix-divide
git worktree add ../practice-add-tests -b add-tests

# Terminal 1
cd ../practice-fix-divide
claude
> Fix the divide function...

# Terminal 2
cd ../practice-add-tests
claude
> Add tests for the average function...

# Clean up when done
git worktree remove ../practice-fix-divide
git worktree remove ../practice-add-tests
```

Each worktree is fully isolated — no conflicts possible.

**When to use**: You have 2+ independent tasks. The tasks don't touch the same files
(or you're using worktrees). You want to get more done in the same amount of time.

### Pattern D: CLI Planning → Desktop Parallel Execution

Plan interactively in the CLI (where the back-and-forth Q&A is strongest), then
spin up multiple parallel sessions in the Desktop app to execute.

```bash
# Step 1: Plan in CLI (strongest for interactive refinement)
claude
> Plan how to refactor the calculator module into a class-based design.
> What about edge cases for negative exponents?
> OK, write this plan to CLAUDE.md so parallel sessions can follow it.

# Step 2: Commit and push the plan
> Commit and push everything

# Step 3: Open Desktop app, open the same repo
# Click "+ New session" multiple times — each gets its own worktree
#   Session 1: "Implement the Calculator class per the plan in CLAUDE.md"
#   Session 2: "Write comprehensive tests per the plan in CLAUDE.md"
#   Session 3: "Update documentation per the plan in CLAUDE.md"

# Step 4: When sessions finish, merge branches into main
```

**Why this works**: The CLI's Plan Mode interaction is great for iterative thinking.
The Desktop app's parallel sessions with worktree isolation are great for execution.
Writing the plan to `CLAUDE.md` bridges the two — the Desktop sessions read it
automatically and follow the agreed-upon approach.

**When to use**: You have multiple independent tasks and want the best of both
interfaces — CLI for planning, Desktop for parallel execution.

### Pattern E: Cross-Device Workflow

Start work in one place, continue in another.

```
Work desktop          Home laptop           Phone
─────────────         ─────────────         ─────────
Start task locally    Pull and continue     Monitor via
  or use &              or teleport         claude.ai
Push to branch        /tasks + t            or iOS app
```

**Example flow**:
```bash
# At work: start a cloud session before leaving
> & Refactor the calculator module to use a class-based design

# At home: check on it
claude
> /tasks
# Select the session, press 't' to teleport into it

# On phone: check progress on claude.ai or the iOS app
```

**When to use**: Your work day spans locations or devices.

---

## Plan Mode: The Most Important Habit

Plan Mode is how you prevent Claude from going off the rails. Boris says he starts
almost every task this way.

### How to enter Plan Mode

- **Inside Claude Code**: Press `Shift+Tab` twice (cycles through modes)
- **Or just ask**: "Plan how you'd approach this before making any changes"

### The pattern

1. **Enter plan mode** — Claude reads code and proposes an approach
2. **Iterate** — Ask questions, push back, refine. "What about edge cases?"
   "Use approach X instead." Go back and forth until you like the plan.
3. **Approve** — Once the plan is solid, tell Claude to proceed
4. **Auto-accept mode** — Press `Shift+Tab` once so Claude can execute without
   prompting you for every file edit. Claude usually one-shots it after good planning.

### Pro tips from the team

- **Second opinion**: Spin up a second Claude instance and paste the plan in.
  Ask it to critique the plan "as a staff engineer." This catches blind spots.

- **Re-plan when stuck**: If Claude gets lost mid-task, don't keep pushing.
  Go back to Plan Mode: "Stop. Let's re-plan. What's the current state and what
  should we do differently?"

- **Challenge-based prompts**: After Claude proposes a plan, try: "Grill me on
  these changes and don't make a PR until I pass your test." Or after a weak
  implementation: "Knowing everything you know now, scrap this and implement the
  elegant solution."

---

## CLAUDE.md: Teaching Claude Your Preferences

`CLAUDE.md` is a markdown file in your project root that Claude reads at the start of
every session. It's how you give Claude persistent memory about your project.

### What to put in it

- **Project context**: What the repo is, what it does, key architecture decisions
- **Style conventions**: Naming, formatting, patterns you prefer
- **Mistakes to avoid**: Things Claude has gotten wrong before
- **Testing patterns**: How to run tests, what framework you use
- **Safety rules**: "Never touch prod", "Always run tests before committing"

### The self-improvement loop

This is the key insight from Boris's team: **Claude should update its own CLAUDE.md**.

After Claude makes a mistake or you correct it, say:

```
Update CLAUDE.md so you don't make that mistake again.
```

Over time, your CLAUDE.md becomes a living document of project knowledge. The team's
file is about 2,500 tokens and gets updated multiple times per week.

### Example entries

```markdown
## Testing
- Run tests with: `pytest test_calculator.py -v`
- Always run tests after changing calculator.py
- Test edge cases: empty inputs, zero, negative numbers

## Style
- Use snake_case for functions and variables
- Include docstrings on public functions
- Keep functions under 20 lines

## Common Mistakes
- Don't forget to handle empty list in average() — check before dividing
- The power() function must handle negative exponents — use ** operator
- Always validate divisor != 0 in divide()
```

### Where CLAUDE.md lives

- **Project root** (checked into git) — shared with your team
- `~/.claude/CLAUDE.md` — personal preferences across all projects
- Each directory can have its own CLAUDE.md for nested context

This repo's own `CLAUDE.md` is an example — look at it to see the format in practice.

### Using CLAUDE.md as cross-machine memory

Conversations don't sync across machines, but `CLAUDE.md` does (via Git). This makes
it your primary tool for continuity across devices.

**Before ending a session**, ask Claude:

```
Update CLAUDE.md with what we accomplished today, current status, and next steps.
```

Claude will write a summary into `CLAUDE.md`. Commit and push. When you pull on
another machine, Claude reads it automatically and picks up where you left off.

**Other memory tools**:
- `claude --continue` — resumes the most recent conversation (same machine only)
- `claude --resume` — interactive picker for past sessions (same machine only)
- `/compact` — condenses the current conversation into a summary (stays local)
- **Session summaries** — Claude auto-saves summaries to `~/.claude/projects/` locally,
  but these don't sync across machines

**The practical workflow**: Git-committed `CLAUDE.md` is the only memory that follows
you between machines. Everything else is local-only. Make updating it a habit.

---

## Slash Commands & Skills

Slash commands are reusable prompts stored as markdown files. They're how you codify
workflows you repeat often.

### How they work

1. Create a markdown file in `.claude/commands/`
2. Write the prompt inside it
3. Use it in Claude Code by typing `/project:command-name`

### Boris's most-used commands

| Command | What it does |
|---------|-------------|
| `/commit-push-pr` | Commits changes, pushes, and creates a PR — used dozens of times daily |
| `/test-and-fix` | Runs the test suite, then fixes any failures |
| `/review-changes` | Reviews staged changes before committing |
| `/worktree` | Sets up a new worktree with a Claude session |
| `/techdebt` | Finds and removes code duplication |

### Creating your own

```bash
# Create the commands directory
mkdir -p .claude/commands

# Create a simple command
cat > .claude/commands/test-and-fix.md << 'EOF'
Run the test suite with `pytest -v`. If any tests fail, fix the failing code
(not the tests) and re-run until all tests pass. Show me the final results.
EOF
```

Then in Claude Code:
```
> /project:test-and-fix
```

### Advanced: Skills with arguments

Commands can accept arguments using `$ARGUMENTS`:

```markdown
<!-- .claude/commands/fix-bug.md -->
Look at this bug report and fix it:

$ARGUMENTS

After fixing, run the relevant tests to verify.
```

Usage:
```
> /project:fix-bug divide() crashes when given zero as the second argument
```

### The philosophy

Anything you do more than twice should become a command. Your command library becomes
institutional knowledge — when a new team member clones the repo, they inherit all
your battle-tested workflows.

---

## Subagents: Keeping Context Clean

As you work on complex tasks, Claude's context window fills up. Subagents are
separate Claude instances that handle subtasks without polluting your main session.

### How to use them

Append "use subagents" to your request:

```
> Refactor the calculator module. Use subagents for each function.
```

Or be specific about what to delegate:

```
> Review this PR. Use a subagent to check test coverage and another to review
> the implementation for security issues.
```

### When to use subagents

| Task | Why subagents help |
|------|-------------------|
| Verification / code review | Keeps verification separate from implementation |
| Large analysis tasks | Prevents context overload in your main session |
| Multi-step workflows | Each step gets its own clean context |
| Build validation | Offload "run and check" loops |

### Boris's subagent patterns

- **Code simplifier**: Reviews code and suggests simplifications
- **Verify app**: Runs the app and checks that it works as expected
- **Build validator**: Runs the build and reports any issues
- **Staff reviewer**: Reviews changes "as a staff engineer" looking for problems

### Context hygiene tip

If your main session is getting long and Claude seems to be losing track of things,
that's a sign you should be using subagents more. Keep your main session focused on
orchestration; delegate the heavy lifting.

---

## Verification: The "Most Important Thing"

Boris emphasizes this more than anything else: **give Claude a way to verify its own
work**. This single practice improves output quality by 2-3x.

### Types of verification

| Type | Example |
|------|---------|
| **Run tests** | "Fix the bug, then run `pytest -v` to verify" |
| **Check build** | "Make the change, then run `npm run build` to confirm it compiles" |
| **Browser testing** | Claude can test web UIs using browser automation |
| **Diff behavior** | "Prove this works by diffing behavior between the old and new branch" |

### The pattern

Don't just say:
```
> Fix the divide function
```

Say:
```
> Fix the divide function to handle division by zero, then run the tests
> to verify everything passes
```

Or even better:
```
> Fix the divide function to handle division by zero. Verify by:
> 1. Running pytest -v
> 2. Testing manually with divide(10, 0) and divide(10, 2)
> 3. Checking that the error message is clear
```

### Make verification automatic

Use **PostToolUse hooks** to run verification after every edit. For example, Boris's
team runs their code formatter automatically:

```json
// In your Claude Code settings
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "your-formatter || true"
      }
    ]
  }
}
```

This catches formatting issues on every edit — the last 10% of problems that would
otherwise fail CI.

---

## Permissions & Safety

Claude Code asks for permission before running commands. This is good for safety but
can be tedious for common operations.

### Using `/permissions` to pre-allow safe commands

Inside Claude Code, type `/permissions` to configure what Claude can run without asking.

**Good to allow**:
```
pytest *           # Test runner
python *           # Python execution
npm run build      # Build commands
npm run test       # Test commands
git status         # Git reads
git diff           # Git reads
```

**Do NOT allow**:
```
rm -rf *           # Destructive operations
git push --force   # Dangerous git operations
docker rm *        # Container deletion
```

### The right approach

Boris's team uses `/permissions` rather than `--dangerously-skip-permissions`. This
gives Claude enough freedom to be productive while keeping guardrails on anything
destructive.

### Hook-based permission gates

Advanced: You can route permission requests through a hook that uses Opus to evaluate
whether a command is safe before auto-approving. This acts as an AI security gate
for automated workflows.

---

## Key Features Worth Knowing

### Extended Thinking

Extended thinking lets Claude reason more deeply before responding. It's especially
useful for complex debugging, architectural decisions, and multi-step refactors.

**How to use it**:
- Toggle on/off with `Shift+Tab` cycling through modes, or just ask: "Think deeply about this"
- In the CLI: `claude --model opus` for the most capable reasoning
- Best for: debugging tricky issues, planning complex refactors, reviewing security implications

Extended thinking costs more tokens but significantly improves quality on hard problems.
Don't use it for simple tasks — save it for when you're stuck or the stakes are high.

### Session Continuity (`--continue` and `--resume`)

Claude Code conversations are local and don't sync across machines. But you can
resume previous sessions on the same machine:

```bash
# Continue the most recent conversation
claude --continue

# Resume a specific past session (interactive picker)
claude --resume
```

This is useful when you close your terminal accidentally or want to pick up where you
left off after a break. Note: this only works on the same machine where the session ran.

### MCP Servers (Model Context Protocol)

MCP lets you connect Claude Code to external tools and data sources — databases,
APIs, browsers, design tools, and more.

```bash
# Add an MCP server
claude mcp add server-name -- command arg1 arg2

# List configured servers
claude mcp list

# Example: add a filesystem MCP server
claude mcp add filesystem -- npx -y @anthropic-ai/mcp-filesystem /path/to/dir
```

**Common MCP use cases**:
- **Browser automation**: Test web UIs, take screenshots, interact with pages
- **Database access**: Query databases directly from Claude Code
- **API integration**: Connect to Slack, Linear, Jira, etc.

MCP servers are configured per-project (in `.claude/`) or globally.

### Hooks

Hooks run shell commands automatically in response to Claude Code events. They're
powerful for enforcing team standards and catching issues early.

```json
// .claude/settings.json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "black --check $CLAUDE_FILE_PATH || true"
      }
    ]
  }
}
```

**Hook events**:
- `PreToolUse` — runs before a tool executes (can block it)
- `PostToolUse` — runs after a tool executes (good for formatters, linters)
- `Notification` — runs when Claude sends a notification

Hooks are how Boris's team auto-formats code on every edit — catching "the last 10%
of problems that would otherwise fail CI."

---

## Quick Reference Card

### Essential commands

| Action | Command |
|--------|---------|
| Start Claude Code | `claude` |
| Start in Plan Mode | `Shift+Tab` twice inside Claude |
| Auto-accept mode | `Shift+Tab` once (after planning) |
| Cloud session | `& your task here` |
| Cloud session from CLI | `claude --remote "your task"` |
| Check cloud sessions | `/tasks` |
| Teleport into session | `/tasks` → select → `t` |
| Configure permissions | `/permissions` |
| Enable status line | `/statusline` |
| Use a slash command | `/project:command-name` |

### When to use what

| Situation | Use |
|-----------|-----|
| Focused single task | Local terminal (Pattern A) |
| Fire-and-forget task | Cloud session (Pattern B) |
| Multiple independent tasks | Parallel sessions (Pattern C) |
| Plan carefully, then execute in parallel | CLI + Desktop (Pattern D) |
| Switching devices | Cloud + teleport (Pattern E) |
| Task is complex | Plan Mode first |
| Claude keeps making the same mistake | Update CLAUDE.md |
| You repeat the same workflow | Create a slash command |
| Context window getting full | Use subagents |

### Troubleshooting

| Problem | Solution |
|---------|----------|
| `&` doesn't work | Install Claude GitHub App (see setup section) |
| Can't teleport | Need clean git state + same claude.ai account |
| Cloud session can't access repo | Check GitHub App repo permissions |
| Claude forgets your preferences | Add them to CLAUDE.md |
| Claude goes off track | Re-enter Plan Mode and re-plan |
| Permission prompts are annoying | Use `/permissions` to pre-allow safe commands |
| Context window filling up | Use subagents to offload subtasks |

### Voice dictation tip

On macOS, press `fn` twice to activate voice dictation. You speak ~3x faster than you
type, which means more detailed prompts with less effort. The Claude Code team considers
this an underrated productivity boost.

---

## Further Reading

- [Boris's workflow post](https://x.com/bcherny/status/2007179832300581177) — the original thread
- [10 tips from the team](https://x.com/bcherny/status/2017742741636321619) — advanced techniques
- [Git worktree docs](https://git-scm.com/docs/git-worktree) — official reference
- [WORKFLOW_COMPARISON.md](WORKFLOW_COMPARISON.md) — comparison of all Claude Code platforms (CLI, VS Code, Cursor, Desktop, Cloud)
- [PRACTICE_EXERCISES.md](PRACTICE_EXERCISES.md) — hands-on exercises using this repo
