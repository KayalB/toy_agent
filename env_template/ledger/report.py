"""Rolling many expenses up into a settlement report."""

from collections import defaultdict

from .money import format_cents
from .split import split_evenly


def balances(expenses, people):
    """
    Net position per person across every expense.

    Each expense is a dict with a `payer` and an `amount_cents`. The payer
    fronts the whole amount, and everyone (including the payer) owes an
    even share of it. A positive balance means the group owes that person.
    """
    net = defaultdict(int)

    for expense in expenses:
        net[expense["payer"]] += expense["amount_cents"]
        for name, owed in split_evenly(expense["amount_cents"], people).items():
            net[name] -= owed

    return dict(net)


def settlement_lines(expenses, people):
    """Human-readable summary, one line per person, sorted by name."""
    net = balances(expenses, people)
    lines = []
    for name in sorted(people):
        amount = net.get(name, 0)
        verb = "is owed" if amount > 0 else "owes"
        lines.append("{} {} {}".format(name, verb, format_cents(abs(amount))))
    return lines
