"""
Money helpers.

All amounts inside this package are integer cents. Floats are only used
at the boundaries, when reading user input or printing a total.
"""


def to_cents(dollars):
    """Convert a dollar amount to whole cents, rounding to the nearest cent."""
    return int(round(dollars * 100))


def format_cents(cents):
    """Render an integer cent amount as a dollar string, e.g. 1234 -> '$12.34'."""
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return "{}${}.{:02d}".format(sign, cents // 100, cents % 100)


def distribute(total_cents, parts):
    """
    Split `total_cents` into `parts` amounts as evenly as possible.

    Cents cannot be divided, so when the total does not divide evenly the
    leftover cents are handed out one each to the earliest parts. The
    returned amounts must always add back up to `total_cents`.

    distribute(100, 3) -> [34, 33, 33]
    """
    if parts <= 0:
        raise ValueError("parts must be positive")

    base, remainder = divmod(total_cents, parts)
    amounts = [base] * parts
    for i in range(remainder - 1):
        amounts[i] += 1
    return amounts
