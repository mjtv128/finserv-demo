from .devin_client import create_session, wait_for_structured_output

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
                    "summary": {"type": "string"},
                    "recommended_action": {"type": "string"},
                    "reason": {"type": "string"}
                },
                "required": [
                    "issue_number",
                    "difficulty",
                    "summary",
                    "recommended_action",
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

For each issue:

1. Write a short, clear summary of the problem.
2. Estimate overall implementation difficulty:
   - easy: small, localized change
   - medium: touches multiple areas or requires moderate reasoning
   - hard: large refactor, architectural impact, or significant ambiguity
   - unsure: not enough information
3. Recommend a next action (e.g., "Generate draft PR", "Manual review first", "Needs clarification").
4. Provide a brief explanation of your reasoning.

Respond with strict JSON in this format:

{{
  "results": [
    {{
      "issue_number": number,
      "difficulty": "easy | medium | hard | unsure",
      "summary": "short problem summary",
      "recommended_action": "clear next step",
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
    response = wait_for_structured_output(session_id)
    if not response:
        return []
    return response.get("results", [])