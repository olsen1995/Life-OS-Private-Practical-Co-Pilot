
def format_response(summary: str, steps: list[str], priority: str = "normal", actions: list[dict] = [], status: str = "success"):
    return {
        "status": status,
        "summary": summary,
        "chunks": steps,
        "priority": priority,
        "actions": actions
    }

def format_error(message: str):
    return {
        "status": "error",
        "summary": message,
        "chunks": [],
        "priority": "high",
        "actions": []
    }

def chunk_for_adhd(summary: str, steps: list[str], actions: list[dict] = []):
    return format_response(
        summary=summary,
        steps=[
            "✅ Step 1: TL;DR",
            f"📌 Step 2: {steps[0] if steps else 'Let’s take action!'}",
            "🧠 Step 3: We got this, keep going 💪"
        ],
        priority="high",
        actions=actions
    )
