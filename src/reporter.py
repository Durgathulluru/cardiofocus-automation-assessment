import json
import time
from pathlib import Path

REPORT_DIR = Path("reports")
REPORT_JSON = REPORT_DIR / "report.json"
ERROR_LOG = REPORT_DIR / "errors.log"
SCREENSHOT_DIR = REPORT_DIR / "screenshots"

def _ensure_dirs():
    REPORT_DIR.mkdir(exist_ok=True)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

def utc_now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def log_console(msg: str):
    print(msg)

def log_error(msg: str):
    _ensure_dirs()
    ERROR_LOG.open("a", encoding="utf-8").write(msg + "\n")

def append_report(section: str, payload: dict):
    _ensure_dirs()
    existing = {}
    if REPORT_JSON.exists():
        try:
            existing = json.loads(REPORT_JSON.read_text(encoding="utf-8"))
        except Exception:
            existing = {}

    existing.setdefault(section, [])
    existing[section].append(payload)
    REPORT_JSON.write_text(json.dumps(existing, indent=2), encoding="utf-8")

def step(steps: list, name: str, passed: bool, detail=None):
    steps.append({"step": name, "pass": passed, "detail": detail})
    status = "PASS" if passed else "FAIL"
    log_console(f"[{status}] {name}" + (f" | {detail}" if detail else ""))

def new_screenshot_path(prefix: str) -> str:
    _ensure_dirs()
    ts = int(time.time())
    return str(SCREENSHOT_DIR / f"{prefix}_{ts}.png")