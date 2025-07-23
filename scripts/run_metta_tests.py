import subprocess
import pathlib
import sys

# ANSI color codes
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"

# Only run the single test file
single_test_file = pathlib.Path("test-pa-test.metta")

test_metta_files = [single_test_file] if single_test_file.exists() else []

if not test_metta_files:
    print(f"{YELLOW}No test file found: 'test-pa-test.metta'. Exiting.{RESET}")
    sys.exit(0)

print(f"{CYAN}{BOLD}Running test file: {single_test_file}{RESET}")

passed = 0
failed = 0

for test_file in test_metta_files:
    print(f"\n{BOLD}Running: {test_file}{RESET}")
    try:
        result = subprocess.run([
            "mettalog", str(test_file)
        ], capture_output=True, text=True, timeout=120)
        output = result.stdout + result.stderr
        # Simple pass/fail detection: look for 'Failures: 0' or 'Successes:'
        if "[LoonIt Report" in output:
            report_start = output.find("[LoonIt Report")
            report_section = output[report_start:]
            if "Failures:" in report_section:
                import re
                m = re.search(r"Failures:\s*(\d+)", report_section)
                failures = int(m.group(1)) if m else -1
                if failures == 0:
                    print(f"{GREEN}PASS{RESET}")
                    passed += 1
                else:
                    print(f"{RED}FAIL{RESET}")
                    print(report_section)
                    failed += 1
            else:
                print(f"{YELLOW}Could not determine result from report section{RESET}")
                print(report_section)
                failed += 1
        elif result.returncode == 0:
            print(f"{GREEN}PASS (no LoonIt Report, exit code 0){RESET}")
            passed += 1
        else:
            print(f"{RED}FAIL (no LoonIt Report, exit code {result.returncode}){RESET}")
            print(output)
            failed += 1
    except Exception as e:
        print(f"{RED}ERROR running {test_file}: {e}{RESET}")
        failed += 1

print(f"\n{CYAN}{BOLD}Test summary:{RESET}")
print(f"{GREEN}Passed: {passed}{RESET}")
print(f"{RED}Failed: {failed}{RESET}")
print(f"Total: {passed + failed}")

if failed > 0:
    sys.exit(1)
else:
    sys.exit(0)