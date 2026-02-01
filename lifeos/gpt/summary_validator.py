def validate_summary(summary: str, entity: dict) -> None:
    name = entity.get("name", "")
    entity_type = entity.get("type", "")

    if not isinstance(summary, str):
        raise ValueError("Summary must be a string.")

    length = len(summary)
    if length < 20 or length > 300:
        raise ValueError("Summary must be between 20 and 300 characters.")

    if name not in summary:
        raise ValueError("Summary must mention the entity name.")

    if entity_type not in summary:
        raise ValueError("Summary must mention the entity type.")

    if any(token in summary for token in ["[", "]", "http", "*", "_", "`"]):
        raise ValueError("Summary must not contain markdown or links.")

    if "might" in summary or "could" in summary:
        raise ValueError("Summary must not speculate.")

    if not summary[0].isupper() or not summary.endswith("."):
        raise ValueError("Summary must be a plain English declarative sentence.")
