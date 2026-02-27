from .devin_client import create_session, wait_for_session


BATCH_SCHEMA = {
    "type": "object",
    "properties": {
        "results": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "issue_number": {"type": "number"},
                    "difficulty": {"type": "string"},
                    "automation_category": {"type": "string"},
                    "risk_level": {"type": "string"},
                    "reason": {"type": "string"}
                },
                "required": [
                    "issue_number",
                    "difficulty",
                    "automation_category",
                    "risk_level",
                    "reason"
                ]
            }
        }
    },
    "required": ["results"]
}


def build_batch_prompt(issues):
    formatted = []

    for issue in issues:
        formatted.append(
            f"""
Issue #{issue["number"]}

Title:
{issue["title"]}

Description:
{issue.get("body") or ""}
"""
        )

    joined = "\n\n---\n\n".join(formatted)

    return f"""
You are an AI engineering triage assistant.

Classify EACH issue below.

Return STRICT JSON in this format:

{{
  "results": [
    {{
      "issue_number": number,
      "difficulty": "easy | medium | hard | unsure",
      "automation_category": "safe | review-needed",
      "risk_level": "low | medium | high",
      "reason": "short explanation"
    }}
  ]
}}

Issues:

{joined}
"""


def classify_batch(issues):
    prompt = build_batch_prompt(issues)
    session_id = create_session(prompt, BATCH_SCHEMA)
    result = wait_for_session(session_id)
    return result.get("results", [])