import pytest
from selenium import webdriver

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--url", action="store", default="https://example.com")
    parser.addoption("--keep-browser", action="store_true", help="Keep browser open after tests")

@pytest.fixture
def browser(request):
    browser_name = request.config.getoption("--browser")
    url = request.config.getoption("--url")
    keep_browser = request.config.getoption("--keep-browser")

    if browser_name.lower() == "chrome":
        driver = webdriver.Chrome()
    elif browser_name.lower() == "firefox":
        driver = webdriver.Firefox()
    else:
        raise Exception(f"Browser {browser_name} not supported")

    driver.maximize_window()
    driver.get(url)

    yield driver

    if not keep_browser:
        driver.quit()
