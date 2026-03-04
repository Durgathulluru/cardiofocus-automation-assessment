from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DevicesPage:
    def __init__(self, driver, base_url: str):
        self.driver = driver
        self.url = f"{base_url}/devices"

    def open(self):
        self.driver.get(self.url)

    def search_device(self, device_id: str, timeout: int = 15):
        wait = WebDriverWait(self.driver, timeout)

        # NOTE: update these selectors if needed
        search = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "[data-test='device-search'], input[name='deviceSearch'], input[placeholder*='Device']")
            )
        )
        search.clear()
        search.send_keys(device_id)

        wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='device-search-btn'], button[type='submit']"))
        ).click()

    def get_status(self, timeout: int = 15) -> str:
        wait = WebDriverWait(self.driver, timeout)

        # NOTE: update selector if portal differs
        status_el = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='device-status'], .device-status"))
        )
        return status_el.text.strip()