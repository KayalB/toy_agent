import pytest

from ledger.money import distribute, format_cents, to_cents


def test_to_cents_rounds_to_nearest_cent():
    assert to_cents(12.34) == 1234
    assert to_cents(0.1) == 10
    assert to_cents(19.999) == 2000


def test_format_cents_pads_the_decimal():
    assert format_cents(1234) == "$12.34"
    assert format_cents(5) == "$0.05"


def test_format_cents_handles_negatives():
    assert format_cents(-250) == "-$2.50"


def test_distribute_splits_an_even_total():
    assert distribute(900, 3) == [300, 300, 300]


def test_distribute_rejects_zero_parts():
    with pytest.raises(ValueError):
        distribute(100, 0)
