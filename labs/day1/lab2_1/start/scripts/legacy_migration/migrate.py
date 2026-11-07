"""Deprecated one-off migration script kept for historical reference."""


def parse_legacy_csv_row(row_text: str) -> list[str]:
    """Split a comma-separated row into stripped fields."""
    return [field.strip() for field in row_text.split(",") if field.strip()]

