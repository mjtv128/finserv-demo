from .devin_client import create_session, wait_for_session


# Expected structured response from Devin
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
                    "risk_level": {"type": "string"},
                    "scope": {"type": "string"},
                    "reason": {"type": "string"}
                },
                "required": [
                    "issue_number",
                    "difficulty",
                    "risk_level",
                    "scope",
                    "reason"
                ]
            }
        }
    },
    "required": ["results"]
}


def build_batch_prompt(issues):
    issue_sections = []

    for issue in issues:
        issue_sections.append(
            f"""
Issue #{issue["number"]}

Title:
{issue["title"]}

Description:
{issue.get("body") or "No description provided."}
"""
        )

    issues_block = "\n\n---\n\n".join(issue_sections)

    return f"""
You are assisting with engineering triage for a financial services repository.

For each issue, classify:

- difficulty: estimated implementation complexity (easy, medium, hard, unsure)
- risk_level: potential impact if the change is incorrect (low, medium, high, unsure)
- scope: expected change surface area (single-file, few-files, multi-module, architectural)
- reason: short explanation for your decision

Respond with strict JSON in this format:

{{
  "results": [
    {{
      "issue_number": number,
      "difficulty": "easy | medium | hard | unsure",
      "risk_level": "low | medium | high | unsure",
      "scope": "single-file | few-files | multi-module | architectural",
      "reason": "brief explanation"
    }}
  ]
}}

Issues:

{issues_block}
"""


def classify_batch(issues):
    prompt = build_batch_prompt(issues)
    session_id = create_session(prompt, BATCH_SCHEMA)
    response = wait_for_session(session_id)
    return response.get("results", [])