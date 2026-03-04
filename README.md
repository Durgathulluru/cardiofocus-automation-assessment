# CardioFocus Automation Assessment
**Candidate:** Sai Kumar Thulluru

---

## 1) What this repo includes
- **UI automation:** Selenium test validates login → device search → displayed device status
- **API automation:** Requests test validates `/api/devices/{device_id}` JSON response and status
- **Reporting:** Results stored in files under `reports/` (created automatically)

---

## 2) Requirements
- Python 3.10+ recommended
- Install dependencies from `requirements.txt`

---

## 3) Setup
```bash
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
# .venv\\Scripts\\activate   # Windows

pip install -r requirements.txt
```

---

## 4) Assumptions
- **Portal URL:** https://portal.cardiofocus.com
- **Login path:** `/login`
- **Devices path:** `/devices`
- **API endpoint:** `/api/devices/{device_id}`
- **API authentication:** Token (Bearer) or Basic authentication
- **UI selectors:** Best-guess defaults. If the portal uses different selectors, update:
  - `src/pages/login_page.py`
  - `src/pages/devices_page.py`

---

## 5) Configuration (Environment Variables)

### 5.1 UI settings
- `UI_BASE_URL=https://portal.cardiofocus.com`
- `UI_USERNAME=your_username`
- `UI_PASSWORD=your_password`
- `DEVICE_ID=ABC123`
- `EXPECTED_STATUS=OK`
- `HEADLESS=true` *(optional)*

### 5.2 API settings (choose one)

**Option A: Token (default)**
- `API_BASE_URL=https://portal.cardiofocus.com`
- `API_AUTH_MODE=token`
- `API_TOKEN=your_token`
- `DEVICE_ID=ABC123`
- `EXPECTED_STATUS=OK`

**Option B: Basic**
- `API_BASE_URL=https://portal.cardiofocus.com`
- `API_AUTH_MODE=basic`
- `API_BASIC_USER=your_user`
- `API_BASIC_PASS=your_password`
- `DEVICE_ID=ABC123`
- `EXPECTED_STATUS=OK`

---

## 6) Run commands

### Run UI only
```bash
python src/ui_test.py
```

### Run API only
```bash
python src/api_test.py
```

### Run both (recommended)
```bash
python src/run_all.py
```

---

## 7) Where to see outputs
When you run the scripts, the `reports/` folder is created automatically:
- **JSON report:** `reports/report.json`
- **Error log (saved on failures):** `reports/errors.log`
- **UI screenshots on failure:** `reports/screenshots/`

---

## 8) Reporting behavior (Pass/Fail + errors)
- Each step prints PASS/FAIL in the console.
- Every run appends a result block to `reports/report.json`.
- If a failure occurs, the error is saved into `reports/errors.log`.
- UI failures also capture a screenshot path into the report.

---

## 9) Approach and design decisions (brief)
- **Page Object Model:** UI locators and actions are in `src/pages/` for maintainability.
- **Explicit waits:** Uses `WebDriverWait` to reduce timing-related flakiness.
- **Secure handling:** Credentials and tokens are read from environment variables (no secrets in code/logs).
- **Robust errors:** Clear failure messages + saved error log + UI screenshot for faster debugging.
- **Scalable layout:** Shared config and reporting utilities make it easy to add more tests.

---

## Important Note
This repository includes working automation structure, but for the **real CardioFocus portal** you may need to adjust UI selectors (field names/IDs, search input, status label). The framework is designed so selector updates are isolated to:
- `src/pages/login_page.py`
- `src/pages/devices_page.py`