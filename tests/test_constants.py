from legal_clause_adaptation import EXPECTED_SPLIT_SIZES, FROZEN_LABELS


def test_frozen_label_schema_is_unique_and_complete():
    assert len(FROZEN_LABELS) == 20
    assert len(set(FROZEN_LABELS)) == 20
    assert FROZEN_LABELS[0] == "Parties"
    assert FROZEN_LABELS[-1] == "Termination For Convenience"


def test_frozen_split_sizes():
    assert EXPECTED_SPLIT_SIZES == {"train": 8257, "validation": 833, "test": 1850}
