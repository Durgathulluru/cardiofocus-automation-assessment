from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver, base_url: str):
        self.driver = driver
        self.url = f"{base_url}/login"

    def open(self):
        self.driver.get(self.url)

    def login(self, username: str, password: str, timeout: int = 15):
        wait = WebDriverWait(self.driver, timeout)

        # NOTE: These are common selectors. If the portal uses different ones,
        # update them here.
        wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

        # Post-login verification - update selector if needed.
        wait.until(
            EC.any_of(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "a[href*='devices']")),
                EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='nav-devices']")),
            )
        )