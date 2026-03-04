import sys
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException

from config import load_ui_config
from reporter import utc_now, step, append_report, log_error, new_screenshot_path
from pages.login_page import LoginPage
from pages.devices_page import DevicesPage

def create_driver(headless: bool):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,900")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)

def main() -> int:
    cfg = load_ui_config()
    start = time.time()

    result = {
        "test_name": "UI_Device_Status_Validation",
        "timestamp_utc": utc_now(),
        "device_id": cfg.device_id,
        "expected_status": cfg.expected_status,
        "pass": False,
        "steps": [],
        "error": None,
        "screenshot": None,
        "duration_seconds": None,
    }

    if not cfg.username or not cfg.password:
        result["error"] = "Missing UI_USERNAME or UI_PASSWORD."
        append_report("ui", result)
        log_error(f"[UI] {result['error']}")
        print("[FAIL] Missing UI credentials.")
        return 1

    driver = None
    try:
        driver = create_driver(cfg.headless)
        login = LoginPage(driver, cfg.base_url)
        devices = DevicesPage(driver, cfg.base_url)

        login.open()
        step(result["steps"], "Open login page", True, f"{cfg.base_url}/login")

        login.login(cfg.username, cfg.password)
        step(result["steps"], "Login successful", True)

        devices.open()
        step(result["steps"], "Open device management page", True, f"{cfg.base_url}/devices")

        devices.search_device(cfg.device_id)
        step(result["steps"], "Search device by ID", True, cfg.device_id)

        actual = devices.get_status()
        ok = (actual == cfg.expected_status)
        step(result["steps"], "Validate device status", ok, {"actual": actual, "expected": cfg.expected_status})

        if not ok:
            raise AssertionError(f"Status mismatch: expected '{cfg.expected_status}', got '{actual}'")

        result["pass"] = True

    except (TimeoutException, WebDriverException, AssertionError) as e:
        result["error"] = str(e)
        log_error(f"[UI] {result['error']}")

        if driver:
            path = new_screenshot_path("ui_failure")
            try:
                driver.save_screenshot(path)
                result["screenshot"] = path
            except Exception:
                pass

        print(f"[FAIL] UI test failed: {e}")

    finally:
        if driver:
            driver.quit()
        result["duration_seconds"] = round(time.time() - start, 2)
        append_report("ui", result)

    return 0 if result["pass"] else 1

if __name__ == "__main__":
    sys.exit(main())