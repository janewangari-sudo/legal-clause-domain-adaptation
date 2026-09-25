"""Frozen study constants shared by validation and reproduction utilities."""

RANDOM_SEED = 42
UNKNOWN_LABEL = "Unknown"

FROZEN_LABELS = (
    "Parties",
    "License Grant",
    "Cap On Liability",
    "Audit Rights",
    "Anti-Assignment",
    "Insurance",
    "Document Name",
    "Agreement Date",
    "Governing Law",
    "Expiration Date",
    "Effective Date",
    "Post-Termination Services",
    "Revenue/Profit Sharing",
    "Minimum Commitment",
    "Exclusivity",
    "Rofr/Rofo/Rofn",
    "Ip Ownership Assignment",
    "Non-Transferable License",
    "Non-Compete",
    "Termination For Convenience",
)

EXPECTED_SPLIT_SIZES = {"train": 8257, "validation": 833, "test": 1850}
EXPECTED_GROUP_COUNTS = {"train": 193, "validation": 35, "test": 57}
REQUIRED_COLUMNS = frozenset({"clause_text", "clause_type", "contract_title"})
