from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from sys import platform, exit
import os
from elticket import helper_config

"""
The browser module does handle the initialization of selenium.webdriver drivers
"""


def select_browser(selected_browser):
    """
    The function creates webdriver session with the browser specified via system arguments
    :return: driver
    """

    verify_profile_path(selected_browser)
    service_log_path = ""

    if platform == "linux" or platform == "darwin":
        service_log_path = "/var/tmp/"
    if platform == "win32":
        service_log_path = "C:\\Windows\\Temp\\"

    if selected_browser in ("ff", "firefox"):
        service_log_path += "geckodriver.log"
        browser = create_firefox_driver(service_log_path)
        return browser

    elif selected_browser in "chrome":
        try:
            service_log_path += "chromedriver.log"
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option("detach", True)
            browser = create_chrome_driver(service_log_path=service_log_path,
                                           options=chrome_options)
            return browser
        except Exception as e:
            print(e)

    else:
        print("A browser needs to be specified using the '-b' option")
        exit()


def verify_profile_path(browser_type):
    if browser_type in ("ff", "firefox"):
        path = helper_config.get_config_value(1, "firefox_profile_dir")
        if path and os.path.isdir(path):
            return
        elif not path:
            print("No profile path for firefox is set.")
        else:
            print(path + " is not a valid path on this system.")

        print("Use 'elticket set firefox_profile <PATH>'")
        exit()


def create_firefox_driver(service_log_path: str):
    """
    Creates a firefox instance with a preset profile
    :return:
    """
    firefox_options = FirefoxOptions()
    firefox_options.log.level = "info"

    from elticket import helper_config

    config = helper_config.get_config()
    firefox_profile_dir = config.get(config.sections()[1],
                                     'firefox_profile_dir')

    if firefox_profile_dir:
        profile = webdriver.FirefoxProfile(
            profile_directory=firefox_profile_dir)
        profile.accept_untrusted_certs = True
        driver = webdriver.Firefox(firefox_profile=profile,
                                   options=firefox_options,
                                   service_log_path=service_log_path)
    else:
        driver = webdriver.Firefox(options=firefox_options,
                                   service_log_path=service_log_path)
    driver.implicitly_wait(10)  # function requires Firefox 53.0 or higher

    return driver


def create_chrome_driver(service_log_path, options=None):

    # add `service_args=["--verbose"]` argument to enable verbose logging
    driver = webdriver.Chrome(chrome_options=options,
                              service_log_path=service_log_path)
    driver.implicitly_wait(10)
    return driver
