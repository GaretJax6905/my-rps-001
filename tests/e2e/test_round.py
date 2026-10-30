"""RPS-001 in a real browser: play one round, then play again."""

import pytest
from playwright.sync_api import Page, expect

import app as web

pytestmark = pytest.mark.e2e


def test_round_and_replay_in_real_browser(page: Page, live_server, monkeypatch):
    """Real clicks, real HTTP, real rules; only the computer's move is fixed."""
    monkeypatch.setattr(web.random, "choice", lambda _moves: "scissors")
    page.goto(live_server)
    expect(page.get_by_role("heading", name="Your next move?")).to_be_visible()

    page.get_by_role("button", name="Rock", exact=True).click()

    choices = page.get_by_label("This round’s choices")
    expect(choices).to_contain_text("Rock")
    expect(choices).to_contain_text("Scissors")
    expect(page.locator("[data-outcome]")).to_have_attribute("data-outcome", "win")
    expect(page.get_by_role("heading", name="You win!")).to_be_visible()

    # Play again: a new, independent round with a different result.
    page.get_by_role("button", name="Paper", exact=True).click()

    expect(choices).to_contain_text("Paper")
    expect(choices).to_contain_text("Scissors")
    expect(page.locator("[data-outcome]")).to_have_attribute("data-outcome", "lose")
    expect(page.get_by_role("heading", name="Computer wins")).to_be_visible()
    expect(page.get_by_role("status")).to_have_count(0)
