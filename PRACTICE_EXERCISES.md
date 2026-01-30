# Cloud Session Practice Exercises

## Prerequisites

1. Push this repo to GitHub (e.g., `therealRYC/github-practice`)
2. Install the Claude GitHub app on the repo
3. Navigate into this folder in your terminal and start Claude Code

---

## Exercise 1: Basic `&` Task — Fix a Bug

Send a bug fix to the cloud and watch it work:

```
& Fix the divide function in calculator.py to handle division by zero
```

Then check progress with `/tasks`. When it finishes, review the branch and PR it created.

---

## Exercise 2: Add Missing Tests

Ask the cloud to write tests for the untested functions:

```
& Add tests for divide, power, and average in test_calculator.py
```

Use `/tasks` to monitor. When done, review the changes on GitHub.

---

## Exercise 3: Teleporting a Session

1. Send a task to the cloud:
   ```
   & Add type hints to all functions in calculator.py
   ```
2. While it's running (or after it finishes), use `/tasks` and press `t` to teleport into the session
3. Once teleported, you can continue the conversation locally — ask follow-up questions or request more changes

---

## Exercise 4: Parallel Cloud Tasks

Launch multiple tasks at once and watch them run independently:

```
& Add a factorial function to calculator.py with tests
& Add a fibonacci function to calculator.py with tests
```

Check `/tasks` to see both running simultaneously.

---

## Exercise 5: Plan Locally, Execute Remotely

1. Start a local conversation and plan out a change:
   ```
   I want to add a statistics module with mean, median, mode, and standard deviation. Let's plan it out.
   ```
2. Discuss the approach with Claude locally
3. When satisfied, send it to the cloud:
   ```
   & Create a statistics.py module with mean, median, mode, and stdev functions, plus tests in test_statistics.py
   ```

---

## Known Bugs in calculator.py (for exercises)

These are intentional — use them for practice tasks:

1. `divide()` — no zero-division handling
2. `power()` — doesn't handle negative exponents
3. `average()` — crashes on empty list
