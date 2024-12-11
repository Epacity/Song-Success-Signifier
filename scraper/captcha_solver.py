import requests
from config import *
from typing import Optional

def create_solve_task() -> (int, Optional[str]):
    endpoint = "https://api.2captcha.com/createTask"
    payload = {
        "clientKey":TWOCAP_KEY,
        "task": {
            "type": "RecaptchaV3TaskProxyless",
            "websiteURL": RECAP_ON_URL,
            "websiteKey": RECAP_KEY,
            "minScore": 0.7,
            "pageAction": RECAP_ACTION,
            "isEnterprise": True,
            "apiDomain": "www.recaptcha.net"
        }
    }
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()

        response_data = response.json()
        if "errorDescription" in response_data.keys():
            return 0, response_data["errorDescription"]

        return response_data["taskId"], None

    except requests.HTTPError as error:
        return 0, f"Bad status code: {error.response.status_code}"

    except Exception as error:
        return 0, f"Unknown error: {error}"


def get_solve_response(task_id: int) -> (str, Optional[str]):
    endpoint = "https://api.2captcha.com/getTaskResult"
    payload = {
       "clientKey": TWOCAP_KEY,
       "taskId": task_id,
    }
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()

        response_data = response.json()
        if "errorDescription" in response_data.keys():
            return 0, response_data["errorDescription"]

        status = response_data["status"]
        if status == "ready":
            return response_data["solution"]["gRecaptchaResponse"], None

        elif status == "processing":
            return None, None

        else:
            return None, f"Unknown status: {status}"

    except requests.HTTPError as error:
        return 0, f"Bad status code: {error.response.status_code}"

    except Exception as error:
        return 0, f"Unknown error: {error}"
