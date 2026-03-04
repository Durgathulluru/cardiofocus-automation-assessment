import sys
from ui_test import main as ui_main
from api_test import main as api_main

def main() -> int:
    ui_rc = ui_main()
    api_rc = api_main()
    return 0 if (ui_rc == 0 and api_rc == 0) else 1

if __name__ == "__main__":
    sys.exit(main())