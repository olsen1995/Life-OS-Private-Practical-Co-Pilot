def validate_summary(summary: str, entity: dict) -> None:
    if not isinstance(summary, str):
        raise ValueError("Summary must be a string")

    summary = summary.strip()
    length = len(summary)

    if length < 20:
        raise ValueError("Summary is too short (< 20 characters)")
    if length > 300:
        raise ValueError("Summary is too long (> 300 characters)")

    name = entity.get("name", "").lower()
    type_ = entity.get("type", "").lower()
    text = summary.lower()

    if name not in text:
        raise ValueError(f"Summary must mention entity name: {name}")
    if type_ not in text:
        raise ValueError(f"Summary must mention entity type: {type_}")

    if any(symbol in summary for symbol in ["**", "*", "[", "]", "`", "http", "<", ">"]):
        raise ValueError("Summary contains disallowed formatting or links")

    if "external" in text or "future" in text:
        raise ValueError("Summary contains speculative or external references")
