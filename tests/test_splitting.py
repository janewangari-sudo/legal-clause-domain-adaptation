import pandas as pd
import pytest

from legal_clause_adaptation.data import validate_group_separation


def frame(*groups):
    return pd.DataFrame({"contract_title": groups})


def test_group_separation_accepts_disjoint_title_groups():
    validate_group_separation(
        {
            "train": frame("A", "B"),
            "validation": frame("C"),
            "test": frame("D"),
        }
    )


def test_group_separation_rejects_cross_split_title_group():
    with pytest.raises(ValueError, match="Document-title-group overlap"):
        validate_group_separation(
            {
                "train": frame("Services Agreement"),
                "validation": frame("Licence Agreement"),
                "test": frame("Services Agreement"),
            }
        )
