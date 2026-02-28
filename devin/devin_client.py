import os
import requests
import time

DEVIN_API_KEY = os.environ.get("DEVIN_API_KEY")
BASE_URL = "https://api.devin.ai/v1/sessions"

HEADERS = {
    "Authorization": f"Bearer {DEVIN_API_KEY}",
    "Content-Type": "application/json"
}


# def create_session(prompt, schema=None):
  
#     response = requests.post(
#         BASE_URL,
#         headers=HEADERS,
#         json={
#             "prompt": prompt,
#             "structured_output_schema": schema
#         }
#     )
#     response.raise_for_status()
#     return response.json()["session_id"]

def create_session(prompt, schema=None):
    payload = {
        "prompt": prompt
    }

    if schema:
        payload["response_schema"] = schema

    response = requests.post(
        BASE_URL,
        headers=HEADERS,
        json=payload
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
        status = data.get("status_enum")

        print("Status:", status)

        pr = data.get("pull_request")

        # ✅ If PR exists, we are done
        if pr:
            print("PR detected:", pr)
            return {
                "status": "completed",
                "pr_url": pr.get("html_url") or pr.get("url")
            }

        # ❌ Only fail if explicitly failed
        if status in ["failed", "blocked"]:
            return {
                "status": status,
                "pr_url": None
            }

    raise TimeoutError("Devin session timed out.")