import allure_commons
import pytest
from appium.options.android import UiAutomator2Options
from selene import browser, support
import os
from dotenv import load_dotenv

from selenium import webdriver

@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()

@pytest.fixture(scope='function', autouse=True)
def mobile_management():
    user_name = os.getenv("bs_userName")
    access_key = os.getenv("bs_accessKey")
    options = UiAutomator2Options().load_capabilities({
        # Specify device and os_version for testing
        # "platformName": "android",
        "platformVersion": "9.0",
        "deviceName": "Google Pixel 3",

        # Set URL of the application under test
        "app": "bs://sample.app",

        # Set other BrowserStack capabilities
        'bstack:options': {
            "projectName": "First Python project",
            "buildName": "browserstack-build-2",
            "sessionName": "BStack first_test",

            # Set your access credentials
            "userName": f"{user_name}",
            "accessKey": f"{access_key}"
        }
    })

    # browser.config.driver = webdriver.Remote("http://hub.browserstack.com/wd/hub", options=options)
    browser.config.driver_remote_url = 'http://hub.browserstack.com/wd/hub'
    browser.config.driver_options = options

    browser.config.timeout = float(os.getenv('timeout', '10.0'))

    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )

    yield

    browser.quit()