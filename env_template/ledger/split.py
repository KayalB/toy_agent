"""Deciding who owes what for a single expense."""

from .money import distribute


def split_evenly(total_cents, people):
    """Split one expense evenly across `people`.

    Returns a dict mapping each name to the cents they owe.
    """
    if not people:
        raise ValueError("need at least one person")

    amounts = distribute(total_cents, len(people))
    return dict(zip(people, amounts))


def split_by_shares(total_cents, shares):
    """Split one expense in proportion to weights.

    `shares` maps each name to an integer weight, so {"ana": 2, "bo": 1}
    means Ana covers twice what Bo does. Implemented by handing out one
    unit per share and adding up each person's units.
    """
    if not shares:
        raise ValueError("need at least one share")

    names = list(shares)
    units = distribute(total_cents, sum(shares.values()))

    owed = {}
    cursor = 0
    for name in names:
        count = shares[name]
        owed[name] = sum(units[cursor:cursor + count])
        cursor += count
    return owed
