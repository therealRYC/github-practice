<!-- Created: 2026-02-17 -->
<!-- Last updated: 2026-02-17 — Initial creation from worktree workflow conversation -->

# Claude Code CLI Worktree Workflow

A practical guide to using git worktrees with Claude Code CLI to enable parallel work
on multiple tasks simultaneously. This is the local CLI equivalent of how claude.ai web
gives each chat its own isolated copy of your repo.

**Who this is for**: Anyone using Claude Code in the terminal who wants to work on
multiple tasks at the same time without constantly switching branches.

---

## Table of Contents

- [Why Worktrees?](#why-worktrees)
- [Worktrees vs. Branches vs. Claude.ai Web](#worktrees-vs-branches-vs-claudeai-web)
- [Quickstart: Session Workflow](#quickstart-session-workflow)
- [Creating and Using Worktrees](#creating-and-using-worktrees)
- [Handling Dependencies Between Tasks](#handling-dependencies-between-tasks)
- [The Plan + Execute Pattern (Pattern D)](#the-plan--execute-pattern-pattern-d)
- [Command Reference](#command-reference)
- [Tips and Best Practices](#tips-and-best-practices)

---

## Why Worktrees?

Normally, a git repo has **one working directory** tied to **one branch**. If you want to
switch tasks, you have to stash your work, switch branches, and lose your context. With
Claude Code, this is especially painful because your Claude session was working on one set
of files, and suddenly everything changes underneath it.

**Worktrees** solve this by creating **additional working directories**, each checked out
to a **different branch**, all sharing the same `.git` history. Each worktree is a real
directory on disk with real files — not a stash or a snapshot.

This means you can:
- Open a **separate Claude Code session** in each worktree
- Work on multiple features or fixes **in parallel**
- Never stash, never context-switch, never lose your place

---

## Worktrees vs. Branches vs. Claude.ai Web

### The Problem with Just Branches

A branch is just a label pointing to a commit. Your repo can have hundreds of branches,
but you can only **check out one at a time** in a single directory.

```bash
# You're on main, Claude is helping you add factorial()
# Halfway through, you want to also fix a bug in divide()

git stash                # save your in-progress work
git checkout fix-divide  # switch to the other branch
# Now your directory has DIFFERENT file contents
# Your Claude session is now confused — it was just looking at different code!

# When you're done, switch back:
git checkout feature-factorial
git stash pop            # restore your in-progress work
```

This is like having **one desk** and having to clear it off every time you switch tasks.

### How Worktrees Fix This

```bash
git worktree add ../project-factorial -b feature-factorial
git worktree add ../project-fix-divide -b fix-divide

# Now you have THREE directories, all existing at the same time:
# my-project/            → main branch
# project-factorial/     → feature-factorial branch
# project-fix-divide/    → fix-divide branch
```

This is like having **three desks**, each with a different task laid out. You walk between
them — nothing gets stashed or shuffled.

### How Claude.ai Web Does It

When you use Claude on the web (claude.ai), each chat:

1. **Clones the entire repo** onto a cloud VM
2. Creates a new branch
3. Works in that isolated copy

Each chat gets **its own full copy of the repo on a separate computer**:

```
Cloud Chat A  →  [VM 1: full clone, branch-a checked out]
Cloud Chat B  →  [VM 2: full clone, branch-b checked out]
Cloud Chat C  →  [VM 3: full clone, branch-c checked out]
```

You never worry about switching branches because each chat has its own machine.

### Worktrees = The Local Equivalent

Worktrees give you the same "multiple independent workspaces" pattern on your local
machine, **without** duplicating the entire repo:

```
Terminal 1 + Claude  →  ../project-factorial/    (feature-factorial branch)
Terminal 2 + Claude  →  ../project-fix-divide/   (fix-divide branch)
Terminal 3 + Claude  →  ../my-project/           (main branch)
```

The advantage over full clones: worktrees **share the `.git` history**, so they're
lightweight and instant to create.

### Comparison Table

| | One dir + branches | Worktrees | Claude.ai web |
|---|---|---|---|
| Branches checked out at once | 1 | Many | Many |
| How to switch tasks | `git stash` + `checkout` | `cd` to another folder | Open another chat |
| Parallel Claude sessions? | No | Yes | Yes |
| Disk cost | Minimal | Small (shared `.git`) | N/A (cloud VMs) |
| Setup required | Nothing | `git worktree add` | Automatic |

---

## Quickstart: Session Workflow

### Starting a Session

Run these steps at the **beginning** of a work session to set up a clean environment:

```bash
# 1. Navigate to your main repo
cd /path/to/my-project

# 2. Make sure main is up to date
git checkout main
git pull

# 3. Check if you have any leftover worktrees from last time
git worktree list

# 4. If there are stale worktrees you're done with, clean them up
#    (see "Ending a Session" below for details)

# 5. Plan your tasks — decide what you'll work on in parallel
#    Open Claude in your main repo for planning:
claude
#    Use plan mode to break work into independent subtasks

# 6. Create a worktree for each independent task
git worktree add ../project-task-a -b task-a
git worktree add ../project-task-b -b task-b

# 7. Open a terminal + Claude session in each worktree
#    Terminal 1:
cd ../project-task-a && claude
#    Terminal 2:
cd ../project-task-b && claude
```

### Ending a Session

Run these steps at the **end** of a work session to keep everything clean:

```bash
# 1. In each worktree, make sure all work is committed
#    (Claude should have been committing as it works, but double-check)
cd ../project-task-a
git status   # should be clean
cd ../project-task-b
git status   # should be clean

# 2. Go back to your main repo
cd /path/to/my-project

# 3. Merge completed branches (or push them for PRs)
git merge task-a        # merge locally, OR:
gh pr create --head task-a --title "Add feature A"  # create a PR instead

git merge task-b
gh pr create --head task-b --title "Fix bug B"

# 4. Remove worktrees you're done with
git worktree remove ../project-task-a
git worktree remove ../project-task-b

# 5. Verify cleanup
git worktree list       # should only show your main repo

# 6. Delete merged branches
git branch -d task-a
git branch -d task-b

# 7. Push to remote
git push
```

### If You're Pausing (Not Done Yet)

If you're stopping for the day but tasks aren't finished:

```bash
# Just make sure everything is committed in each worktree
cd ../project-task-a && git status  # commit any uncommitted work
cd ../project-task-b && git status  # commit any uncommitted work

# Leave the worktrees in place — pick up where you left off tomorrow
# When you resume, just cd into the worktree and start Claude again
```

---

## Creating and Using Worktrees

### Basic Creation

```bash
# From your main repo directory:
# Creates a new directory AND a new branch in one command
git worktree add ../project-feature-name -b feature-name
```

- `../project-feature-name` — the directory path (sibling to your main repo)
- `-b feature-name` — creates a new branch starting from your current commit

### Naming Convention

Use a consistent pattern so worktrees are easy to find:

```
../project-description
```

For example:
```bash
git worktree add ../calculator-add-factorial -b add-factorial
git worktree add ../calculator-fix-divide -b fix-divide
git worktree add ../calculator-add-tests -b add-tests
```

This puts them all as siblings of your main repo, easy to spot with `ls ..`.

### Running Claude in Each Worktree

Open a separate terminal for each worktree:

```bash
# Terminal 1
cd ../calculator-add-factorial
claude
# Give Claude its task: "Add a factorial function to calculator.py with tests"

# Terminal 2
cd ../calculator-fix-divide
claude
# Give Claude its task: "Fix the divide function to handle division by zero"
```

Each Claude session operates independently, in its own directory, on its own branch.

---

## Handling Dependencies Between Tasks

Not all tasks are fully independent. Here's how to handle each type of dependency.

### 1. Sequential Dependencies (Task B needs Task A's code)

**Example**: Task A adds a `factorial()` function, Task B writes tests that call `factorial()`.

**Strategy**: Stagger the work — don't parallelize things with a strict ordering.

```bash
# Start task A first
git worktree add ../project-feature-a -b feature-a
cd ../project-feature-a && claude
# ... let Claude finish ...

# Merge A into main, THEN branch B from the updated main
cd /path/to/my-project
git merge feature-a
git worktree add ../project-feature-b -b feature-b
cd ../project-feature-b && claude
```

### 2. Shared File Edits (both tasks touch the same file)

**Example**: Task A adds `factorial()` to `calculator.py`, Task B adds `fibonacci()` to
the same file.

**This usually works fine.** Git can merge changes to the same file as long as they
touch different lines. Conflicts only happen when both tasks edit the *same lines*.

If you know there will be conflicts:

```bash
# Option A: Do those tasks sequentially instead

# Option B: Merge one, then rebase the other
git merge feature-a
git rebase main feature-b    # resolve conflicts here
git checkout main
git merge feature-b
```

### 3. Shared Infrastructure (both tasks need a common change)

**Example**: Both tasks need a new utility module or a new dependency.

**Strategy**: Do the shared piece first on main, then branch.

```bash
# Step 1: Make the shared change on main
# (add the utility module, install the dependency, etc.)

# Step 2: THEN create worktrees — both start from updated main
git worktree add ../project-feature-a -b feature-a
git worktree add ../project-feature-b -b feature-b
```

### 4. Late-Discovered Dependencies (realized mid-task)

Sometimes you're halfway through Task B and realize it needs something from Task A.

```bash
# Option A: Cherry-pick specific commits from feature-a into feature-b
cd ../project-feature-b
git cherry-pick <commit-hash-from-feature-a>

# Option B: Pause feature-b, finish feature-a, merge to main, rebase
cd /path/to/my-project
git merge feature-a
cd ../project-feature-b
git rebase main
```

### Thinking in Dependency Graphs

When planning, sort subtasks into a dependency graph:

```
         ┌── B (add tests)        ← depends on A
A (core) ┤
         └── C (add docs)         ← depends on A

D (unrelated refactor)            ← fully independent
```

- **A** runs first (everything depends on it)
- **B and C** run in parallel after A merges (they depend on A, not each other)
- **D** runs in parallel with everything (no dependencies)

**The key insight**: worktrees let you parallelize the **independent branches** of the
dependency graph. Dependent tasks still run sequentially.

---

## The Plan + Execute Pattern (Pattern D)

This is where worktrees reach their full potential with Claude Code.

### Step 1: Plan in Your Main Repo

```bash
cd /path/to/my-project
claude
```

Use plan mode to break a big task into independent subtasks. Ask Claude to identify
dependencies. You should end up with something like:

```
Task 1: Add factorial() function           [no dependencies]
Task 2: Add fibonacci() function           [no dependencies]
Task 3: Fix divide() zero-handling         [no dependencies]
Task 4: Write tests for all new functions  [depends on 1, 2, 3]
```

### Step 2: Create Worktrees for Independent Tasks

```bash
git worktree add ../project-factorial -b add-factorial
git worktree add ../project-fibonacci -b add-fibonacci
git worktree add ../project-fix-divide -b fix-divide
```

### Step 3: Execute in Parallel

Open three terminals, each with its own Claude session:

```bash
# Terminal 1
cd ../project-factorial && claude
# "Add a factorial function to calculator.py"

# Terminal 2
cd ../project-fibonacci && claude
# "Add a fibonacci function to calculator.py"

# Terminal 3
cd ../project-fix-divide && claude
# "Fix divide() to handle division by zero"
```

### Step 4: Merge and Continue

```bash
cd /path/to/my-project
git merge add-factorial
git merge add-fibonacci
git merge fix-divide

# Now branch for the dependent task
git worktree add ../project-add-tests -b add-tests
cd ../project-add-tests && claude
# "Write tests for factorial, fibonacci, and the fixed divide function"
```

### Step 5: Clean Up

```bash
cd /path/to/my-project
git merge add-tests
git worktree remove ../project-factorial
git worktree remove ../project-fibonacci
git worktree remove ../project-fix-divide
git worktree remove ../project-add-tests
git branch -d add-factorial add-fibonacci fix-divide add-tests
```

---

## Command Reference

| Command | What it does |
|---------|-------------|
| `git worktree add <path> -b <branch>` | Create a new worktree on a new branch |
| `git worktree list` | Show all active worktrees and their branches |
| `git worktree remove <path>` | Remove a worktree (working directory must be clean) |
| `git worktree prune` | Clean up references to worktrees that were manually deleted |
| `git branch -d <branch>` | Delete a branch after merging (cleanup step) |
| `git cherry-pick <hash>` | Copy a specific commit into the current branch |
| `git rebase main` | Replay current branch's commits on top of updated main |

---

## Tips and Best Practices

- **Plan before you parallelize.** Use plan mode in your main repo to break work into
  subtasks and identify dependencies. This prevents wasted effort from merge conflicts
  or tasks that needed to be sequential.

- **Keep worktrees as siblings.** Use `../project-description` so all worktrees live next
  to your main repo. Easy to find with `ls ..`.

- **Always use `-b` when creating worktrees.** This ensures each worktree has its own
  branch. Without it, you'd be in a detached HEAD state.

- **CLAUDE.md carries over.** Since worktrees share the repo's files, your project
  `CLAUDE.md` is available in every worktree. Claude knows your preferences everywhere.

- **Parallelize only independent tasks.** If Task B needs code from Task A, don't run
  them in parallel. The merge conflicts and confusion aren't worth it.

- **Clean up when you're done.** Run `git worktree list` regularly. Remove finished
  worktrees with `git worktree remove` and delete merged branches with `git branch -d`.
  Leftover worktrees clutter your disk and can cause confusion.

- **Commit before removing.** `git worktree remove` will refuse if there are uncommitted
  changes. This is a safety net — don't force-remove unless you're sure.

- **Use `git worktree prune`** if you manually deleted a worktree directory (e.g., with
  `rm -rf`). This cleans up git's internal references to the now-missing directory.

- **Three is a good number.** Running 2-4 parallel worktrees is the sweet spot. More than
  that and it becomes hard to keep track of what's happening in each session.
