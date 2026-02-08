# Claude Code Practice Exercises

## Prerequisites

1. Push this repo to GitHub (e.g., `therealRYC/github-practice`)
2. Install the Claude GitHub app on the repo (needed for cloud exercises)
3. Navigate into this folder in your terminal and start Claude Code

> **Note**: Cloud sessions (`&`) are currently experiencing issues for some users
> (see `BACKGROUND_TASKS_&_TROUBLESHOOTING.md`). Each exercise below includes a
> **local alternative** so you can practice regardless.

---

## Exercise 1: Basic Task — Fix a Bug

**Cloud version** (if `&` is working):
```
& Fix the divide function in calculator.py to handle division by zero
```
Then check progress with `/tasks`. When it finishes, review the branch and PR it created.

**Local alternative**:
```bash
git checkout -b fix-divide
claude
```
Then ask Claude:
```
Fix the divide function in calculator.py to handle division by zero.
Run the tests to verify.
```
When done, commit, push the branch, and create a PR.

---

## Exercise 2: Add Missing Tests

**Cloud version**:
```
& Add tests for divide, power, and average in test_calculator.py
```

**Local alternative**:
```bash
git checkout -b add-missing-tests
claude
```
Then ask:
```
Add tests for divide, power, and average in test_calculator.py.
Include edge cases: division by zero, negative exponents, empty lists.
Run pytest -v to verify.
```

---

## Exercise 3: Plan Mode — Think Before Acting

This exercise practices Plan Mode, which is useful regardless of local or cloud work.

1. Start Claude Code and enter Plan Mode (`Shift+Tab` twice):
   ```
   Plan how to add type hints to all functions in calculator.py.
   What edge cases should we handle?
   ```
2. Go back and forth with Claude — ask questions, push back on the approach
3. When satisfied, approve the plan and let Claude execute it
4. Ask Claude to run the tests to verify

**Cloud version** (if you want to try teleporting):
```
& Add type hints to all functions in calculator.py
```
While it's running (or after), use `/tasks` and press `t` to teleport into the session.

---

## Exercise 4: Parallel Local Sessions

Practice running multiple Claude instances simultaneously using worktrees:

```bash
# Create two worktrees
git worktree add ../practice-factorial -b add-factorial
git worktree add ../practice-fibonacci -b add-fibonacci

# Terminal 1
cd ../practice-factorial
claude
> Add a factorial function to calculator.py with tests

# Terminal 2
cd ../practice-fibonacci
claude
> Add a fibonacci function to calculator.py with tests

# Clean up when done
cd /path/to/github-practice
git worktree remove ../practice-factorial
git worktree remove ../practice-fibonacci
```

**Cloud version** (launch both at once):
```
& Add a factorial function to calculator.py with tests
& Add a fibonacci function to calculator.py with tests
```
Check `/tasks` to see both running simultaneously.

---

## Exercise 5: Plan Locally, Execute in Parallel

This combines CLI planning with parallel execution — the workflow from Pattern D
in the Workflow Guide.

1. Start a local conversation and plan out a change:
   ```
   I want to add a statistics module with mean, median, mode, and standard deviation.
   Let's plan it out.
   ```
2. Discuss the approach with Claude — iterate until you have a solid plan
3. Ask Claude to save the plan:
   ```
   Write this plan to CLAUDE.md so other sessions can follow it.
   Commit and push.
   ```
4. Execute in parallel using worktrees (or cloud sessions if available):
   ```bash
   git worktree add ../practice-stats-impl -b stats-implementation
   git worktree add ../practice-stats-tests -b stats-tests

   # Terminal 1: implement the module
   cd ../practice-stats-impl && claude
   > Implement the statistics module per the plan in CLAUDE.md

   # Terminal 2: write the tests
   cd ../practice-stats-tests && claude
   > Write tests for the statistics module per the plan in CLAUDE.md
   ```

---

## Exercise 6: Cross-Machine Memory (CLAUDE.md)

Practice the session handoff workflow:

1. Start Claude Code and do some work (any of the exercises above)
2. Before ending, ask:
   ```
   Update CLAUDE.md with what we accomplished, current status, and next steps.
   ```
3. Commit and push
4. On another machine (or after restarting Claude), pull and start a new session:
   ```bash
   git pull origin main
   claude
   > What did we accomplish in the last session?
   ```
   Claude reads `CLAUDE.md` automatically and should know the context.

---

## Known Bugs in calculator.py (for exercises)

These are intentional — use them for practice tasks:

1. `divide()` — no zero-division handling
2. `power()` — doesn't handle negative exponents
3. `average()` — crashes on empty list
