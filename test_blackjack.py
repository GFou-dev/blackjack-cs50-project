import pytest
from blackjack import Table, result_message, get_playername, BUST_THRESHOLD


@pytest.fixture
def table():
    return Table()


def test_score_number_cards(table):
    assert table.compute_score([("S", "7"), ("H", "8")]) == 15
    assert table.compute_score([("S", "K"), ("H", "Q")]) == 20
    assert table.compute_score([("S", "A"), ("H", "9")]) == 20
    assert table.compute_score([("S", "A"), ("H", "9"), ("C", "5")]) == 15
    assert table.compute_score([("S", "A"), ("H", "A")]) == 12
    assert table.compute_score([("S", "A"), ("H", "K")]) == BUST_THRESHOLD
    assert table.compute_score([("S", "K"), ("H", "Q"), ("C", "5")]) == 25
    assert table.compute_score([]) == 0


def test_deal_cards(table):
    initial_size = len(table.deck)
    table.deal_cards(2, table.p_cards)
    assert len(table.deck) == initial_size - 2
    assert len(table.p_cards) == 2


def test_deck_reset(table):
    table.deal_cards(5, table.p_cards)
    table.deal_cards(3, table.h_cards)
    table.deck_reset()
    assert len(table.deck) == 52
    assert table.p_cards == []
    assert table.h_cards == []


def test_result_message_1():
    assert "Alice" in result_message("Alice")


def test_result_message_2():
    msg = result_message("Alice", busted=True)
    assert "Bust" in msg
    assert "Alice" in msg


def test_get_playername_1(monkeypatch):
    monkeypatch.setattr("sys.argv", ["blackjack.py", "Cat"])
    assert get_playername() == "Cat"


def test_get_playername_2(monkeypatch):
    monkeypatch.setattr("sys.argv", ["blackjack.py"])
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert get_playername() == "Guest"


def test_get_playername_3(monkeypatch):
    monkeypatch.setattr("sys.argv", ["blackjack.py"])
    monkeypatch.setattr("builtins.input", lambda _: "Dog")
    assert get_playername() == "Dog"