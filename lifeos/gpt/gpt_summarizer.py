# /lifeos/gpt/gpt_summarizer.py

def summarize_entity(entity: dict) -> str:
    """
    Produce a deterministic summary for a Canon entity.
    This is a pure function with no side effects and no GPT calls.
    """
    name = entity.get("name", "Unknown")
    type_ = entity.get("type", "UnknownType")
    description = entity.get("description", "No description provided.")

    return (
        f"The canon entity '{name}' is of type '{type_}'. "
        f"It is defined as follows: {description}"
    )
