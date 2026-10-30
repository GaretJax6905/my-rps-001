"""RPS-001: decide one Rock, Paper, Scissors round. See SPEC.md."""

# Each move beats exactly one other move.
BEATS = {"rock": "scissors", "paper": "rock", "scissors": "paper"}


def determine_winner(player: str, computer: str) -> str:
    """Return 'win', 'lose', or 'tie' from the player's perspective.

    The supplied web page accepts only 'rock', 'paper', and 'scissors'.
    """
    if player == computer:
        return "tie"
    if BEATS[player] == computer:
        return "win"
    return "lose"
