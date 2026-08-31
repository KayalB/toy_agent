import pytest

from ledger.split import split_by_shares, split_evenly


def test_split_evenly_across_three_people():
    assert split_evenly(1500, ["ana", "bo", "cy"]) == {"ana": 500, "bo": 500, "cy": 500}


def test_split_evenly_with_one_person_gives_them_everything():
    assert split_evenly(725, ["ana"]) == {"ana": 725}


def test_split_evenly_rejects_an_empty_group():
    with pytest.raises(ValueError):
        split_evenly(1000, [])


def test_split_by_shares_weights_the_amounts():
    assert split_by_shares(900, {"ana": 2, "bo": 1}) == {"ana": 600, "bo": 300}
