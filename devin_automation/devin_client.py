import os
import requests
import time

DEVIN_API_KEY = os.environ.get("DEVIN_API_KEY")
BASE_URL = "https://api.devin.ai/v1/sessions"

HEADERS = {
    "Authorization": f"Bearer {DEVIN_API_KEY}",
    "Content-Type": "application/json"
}

def create_session(prompt, schema=None):
    payload = {
        "prompt": prompt
    }

    if schema:
        payload["structured_output_schema"] = schema

    response = requests.post(
        BASE_URL,
        headers=HEADERS,
        json=payload
    )

    response.raise_for_status()
    return response.json()["session_id"]

def wait_for_session(session_id, timeout=600, interval=10):
    elapsed = 0

    while elapsed < timeout:
        time.sleep(interval)
        elapsed += interval

        response = requests.get(
            f"{BASE_URL}/{session_id}",
            headers=HEADERS
        )
        
        if response.status_code == 504:
            time.sleep(10)
            response = requests.get(
                f"{BASE_URL}/{session_id}",
                headers=HEADERS
            )
        
        response.raise_for_status()
        data = response.json()
        status = data.get("status_enum")
        print("Status:", status)

        pr = data.get("pull_request")
        if pr:
            print("PR detected:", pr)
            return {
                "status": "completed",
                "pr_url": pr.get("html_url") or pr.get("url")
            }

        if status in ["failed", "blocked"]:
            pr = data.get("pull_request")
            if pr:
                return {
                    "status": "completed", 
                    "pr_url": pr.get("html_url") or pr.get("url")
                }
            return {
                "status": status,
                "pr_url": None
            }

    raise TimeoutError("Devin session timed out.")

def wait_for_structured_output(session_id, timeout=120, interval=5):
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
        print("Classifier status:", status)

        if status in ["blocked", "finished"]:
            return data.get("structured_output")

        if status == "failed":
            return None

    raise TimeoutError("Classifier session timed out.")

def terminate_session(session_id):
    requests.delete(
        f"{BASE_URL}/{session_id}",
        headers=HEADERS
    )