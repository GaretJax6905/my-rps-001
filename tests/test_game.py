"""RPS-001 rule checks: nine literal outcomes and one real request/result."""

# pytest injects fixtures by their function names; descriptive test names act
# as the test documentation. Keep all other Pylint diagnostics enabled.
# pylint: disable=redefined-outer-name,missing-function-docstring

import pytest

import app as web
from game import determine_winner


@pytest.fixture
def client():
    web.app.config.update(TESTING=True)
    return web.app.test_client()


@pytest.mark.unit
@pytest.mark.parametrize(
    ("player", "computer", "expected"),
    [
        ("rock", "rock", "tie"),
        ("rock", "paper", "lose"),
        ("rock", "scissors", "win"),
        ("paper", "rock", "win"),
        ("paper", "paper", "tie"),
        ("paper", "scissors", "lose"),
        ("scissors", "rock", "lose"),
        ("scissors", "paper", "win"),
        ("scissors", "scissors", "tie"),
    ],
)
def test_determine_winner_from_player_perspective(player, computer, expected):
    assert determine_winner(player, computer) == expected


@pytest.mark.integration
def test_submitted_round_uses_real_rules(client, monkeypatch):
    # Fix only the computer's random choice; the real rule function still runs.
    monkeypatch.setattr(web.random, "choice", lambda _moves: "paper")
    response = client.post("/", data={"move": "rock"})
    page = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "You chose" in page and "Computer chose" in page
    assert "Rock" in page and "Paper" in page
    assert 'data-outcome="lose"' in page
    assert "Computer wins" in page
    assert "game rules not built yet" not in page
