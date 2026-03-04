import sys
import time
import requests

from config import load_api_config
from reporter import utc_now, append_report, log_error

def main() -> int:
    cfg = load_api_config()
    start = time.time()

    result = {
        "test_name": "API_Device_Status_Validation",
        "timestamp_utc": utc_now(),
        "device_id": cfg.device_id,
        "expected_status": cfg.expected_status,
        "pass": False,
        "http_status": None,
        "error": None,
        "duration_seconds": None,
    }

    url = f"{cfg.base_url}/api/devices/{cfg.device_id}"
    headers = {"Accept": "application/json"}
    auth = None

    if cfg.auth_mode == "token":
        if not cfg.token:
            result["error"] = "Missing API_TOKEN (token auth)."
            append_report("api", result)
            log_error(f"[API] {result['error']}")
            print("[FAIL] Missing API_TOKEN.")
            return 1
        headers["Authorization"] = f"Bearer {cfg.token}"

    elif cfg.auth_mode == "basic":
        if not cfg.basic_user or not cfg.basic_pass:
            result["error"] = "Missing API_BASIC_USER or API_BASIC_PASS (basic auth)."
            append_report("api", result)
            log_error(f"[API] {result['error']}")
            print("[FAIL] Missing basic auth credentials.")
            return 1
        auth = (cfg.basic_user, cfg.basic_pass)

    else:
        result["error"] = "Unsupported API_AUTH_MODE. Use 'token' or 'basic'."
        append_report("api", result)
        log_error(f"[API] {result['error']}")
        print("[FAIL] Unsupported auth mode.")
        return 1

    try:
        resp = requests.get(url, headers=headers, auth=auth, timeout=15)
        result["http_status"] = resp.status_code

        if resp.status_code != 200:
            raise RuntimeError(f"Unexpected HTTP status: {resp.status_code}")

        data = resp.json()
        if "status" not in data:
            raise KeyError("Missing 'status' field in JSON response.")

        actual = str(data["status"]).strip()
        if actual != cfg.expected_status:
            raise AssertionError(f"Status mismatch: expected '{cfg.expected_status}', got '{actual}'")

        result["pass"] = True
        print("[PASS] API validation succeeded.")

    except (requests.RequestException, ValueError, KeyError, AssertionError, RuntimeError) as e:
        result["error"] = str(e)
        log_error(f"[API] {result['error']}")
        print(f"[FAIL] API test failed: {e}")

    finally:
        result["duration_seconds"] = round(time.time() - start, 2)
        append_report("api", result)

    return 0 if result["pass"] else 1

if __name__ == "__main__":
    sys.exit(main())