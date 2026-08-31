# ledger

Split shared household expenses and work out who owes whom.

## Layout

- `ledger/money.py` - integer-cent arithmetic and formatting
- `ledger/split.py` - dividing a single expense among people
- `ledger/report.py` - rolling many expenses into per-person balances
- `tests/` - pytest suite

## Running the tests

    pytest
