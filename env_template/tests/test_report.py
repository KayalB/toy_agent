from ledger.report import balances, settlement_lines

PEOPLE = ["ana", "bo", "cy"]


def test_balances_sum_to_zero():
    """Every cent someone fronts is owed back by someone, so the net is zero."""
    expenses = [
        {"payer": "ana", "amount_cents": 1000},
        {"payer": "bo", "amount_cents": 505},
    ]
    assert sum(balances(expenses, PEOPLE).values()) == 0


def test_payer_is_owed_the_rest_of_the_groups_share():
    expenses = [{"payer": "ana", "amount_cents": 1000}]
    net = balances(expenses, PEOPLE)
    assert net["ana"] == 666
    assert net["bo"] == -333
    assert net["cy"] == -333


def test_settlement_lines_are_sorted_and_formatted():
    expenses = [{"payer": "ana", "amount_cents": 900}]
    assert settlement_lines(expenses, PEOPLE) == [
        "ana is owed $6.00",
        "bo owes $3.00",
        "cy owes $3.00",
    ]
