import os
import requests
import time

DEVIN_API_KEY = os.environ.get("DEVIN_API_KEY")
BASE_URL = "https://api.devin.ai/v1/sessions"

HEADERS = {
    "Authorization": f"Bearer {DEVIN_API_KEY}",
    "Content-Type": "application/json"
}


def create_session(prompt, schema):
    response = requests.post(
        BASE_URL,
        headers=HEADERS,
        json={
            "prompt": prompt,
            "structured_output_schema": schema
        }
    )
    response.raise_for_status()
    return response.json()["session_id"]


# def wait_for_session(session_id, timeout=90, interval=2):
#     elapsed = 0

#     while elapsed < timeout:
#         time.sleep(interval)
#         elapsed += interval

#         response = requests.get(
#             f"{BASE_URL}/{session_id}",
#             headers=HEADERS
#         )
#         response.raise_for_status()

#         data = response.json()
#         if data.get("structured_output"):
#             return data["structured_output"]

#     raise TimeoutError("Devin session timed out.")

def wait_for_session(session_id, timeout=300, interval=5):
    elapsed = 0

    while elapsed < timeout:
        time.sleep(interval)
        elapsed += interval

        response = requests.get(
            f"{BASE_URL}/{session_id}",
            headers=HEADERS
        )
        response.raise_for_status()

        data = response.json()

        print("Status:", data.get("status_enum"))

        # 🔥 AUTHORITATIVE COMPLETION SIGNAL
        pr = data.get("pull_request")
        if pr:
            return {
                "status": "completed",
                "pr_url": pr.get("html_url")
            }

        if data.get("status_enum") == "failed":
            return {
                "status": "failed",
                "pr_url": None
            }

    raise TimeoutError("Devin session timed out.")