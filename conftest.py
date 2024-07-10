import pytest
from colorama import Back, Fore, Style


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == "call":
        if result.passed:
            print(Fore.GREEN + "PASSED: " + item.name + Style.RESET_ALL)
        elif result.failed:
            print(Fore.RED + "FAILED: " + item.name + Style.RESET_ALL)
        elif result.skipped:
            print(Fore.YELLOW + "SKIPPED: " + item.name + Style.RESET_ALL)
