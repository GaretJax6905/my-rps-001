# Rock, Paper, Scissors

## RPS-001: Play a round

**Purpose:** one person plays a quick round against the computer.

- Choose rock, paper, or scissors. The computer chooses one move for that round.
- Display both choices and the result: **You win!**, **Computer wins**, or **It’s a tie**.
- Choosing again starts an independent round. No score or saved history.
- Keep the supplied interface and server. Name/color changes can wait until the rules work.

### Expected results

Results are from the **player’s perspective**. `determine_winner(player, computer)` in `game.py` returns `win`, `lose`, or `tie`. Inputs are the lowercase moves below; the supplied server rejects other choices.

| Player | Computer | Expected return |
| --- | --- | --- |
| rock | rock | tie |
| rock | paper | lose |
| rock | scissors | win |
| paper | rock | win |
| paper | paper | tie |
| paper | scissors | lose |
| scissors | rock | lose |
| scissors | paper | win |
| scissors | scissors | tie |

### Agreed plan

- **Prediction:** Player rock vs computer paper → `lose`, because paper covers rock. This matches the table above.
- **Scope:** implement only `determine_winner(player, computer)` in `game.py`, returning `win`/`lose`/`tie` from the player's perspective. Keep the supplied `app.py`, template, and server. No scoring, storage, accounts, new framework, or AI API.
- **Valid losing round (positive case):** player `rock`, computer `paper` → `lose`; the page shows both choices and "Computer wins".
- **Rejected input (negative case):** a POST with move `lizard` (or no move) → HTTP 400 with "Choose Rock, Paper, or Scissors to play." The rule function is never called. This reuses the supplied tests in `tests/test_shell.py`.
- **Tests:** nine literal unit cases plus one real request/result integration test in `tests/test_game.py`; one real browser round and replay in `tests/e2e/test_round.py`. Only the computer's random choice is fixed.
- **Help received:** Claude (AI) helped draft the plan, implementation, and tests; I reviewed them, ran the checks, and played the game myself.

### Checks

Before coding, agree this small test plan with AI:

| Level | Cases and evidence |
| --- | --- |
| Unit — positive | All nine literal expected results above, including valid losses and ties. |
| Integration — positive | A submitted round uses the real rule function and displays both choices and the correct result. Fix the computer choice for the test. |
| Integration — negative | Reuse supplied missing/unsupported-move tests: HTTP 400 and a helpful explanation, without calling the rules. A crash is not the intended result. |
| E2E — positive | Add a real-browser round and replay in tests/e2e/test_round.py using the supplied live_server/page fixtures. Fix only the computer choice; use real rules and real HTTP. |

Use `unit`, `integration`, and `e2e` pytest markers. Run `.venv/bin/python check.py` for Black, Pylint, fast tests, and browser checks; then review the diff. Keep shared settings and meaningful assertions intact. The student still plays, inspects a rule and its test, and gives feedback. Browser automation does not establish every aspect of usability or application performance.

### Work record

- Issue: https://github.com/GaretJax6905/my-rps-001/issues/1
- Pull request: https://github.com/GaretJax6905/my-rps-001/pull/2
- CI run: https://github.com/GaretJax6905/my-rps-001/actions/runs/41076400287
- Implementation: [game.py](game.py) — `determine_winner` uses a `BEATS` table: equal moves tie, a move that beats the computer's wins, otherwise lose.
- Tests: [tests/test_game.py](tests/test_game.py) (9 unit cases + real request/result integration), [tests/e2e/test_round.py](tests/e2e/test_round.py) (real Chromium round + replay). Missing/invalid input reuses the supplied HTTP 400 tests in [tests/test_shell.py](tests/test_shell.py).
- Full local check (`.venv/bin/python check.py`, 2026-10-30): Black PASS, Pylint PASS, non-browser pytest PASS (23 passed), Chromium E2E PASS (6 passed). First run failed Black/Pylint for missing final newlines; fixed with `black *.py tests`, then all checks passed.
- Test explained: the unit case `("rock", "paper", "lose")` asserts that rock vs paper returns `lose`. It would catch a flipped perspective (returning the computer's result, `win`) or a backwards BEATS table.
- Played round: I chose Rock, the computer chose Paper, and the page showed "Computer wins". That is correct because paper covers rock, and it matches my prediction.
- Other rounds tried: Paper vs Rock → You win!; Scissors vs Scissors → It's a tie; Rock vs Scissors → You win!; Paper vs Scissors → Computer wins. All match the expected results table.
- Replay/keyboard: each click started a new independent round with new choices and no score. Tab moved focus between the Rock, Paper, and Scissors buttons, and Enter played a round.