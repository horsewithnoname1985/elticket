# - This class defines selenium helper methods

from selenium.webdriver.firefox import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import time
import logging
from elticket import helper_config


# Required for Chrome only:
# Checks if a field element is in focus in order to send input text to the
# correct field
def retry_element_is_focused(driver: webdriver.WebDriver, element):
    i = 0
    config = helper_config.get_config()
    wait_until_confirm_selection = config.getfloat(config.sections()[1],
                                                   'wait_until_confirm_selection')

    while not element == driver.switch_to.active_element:
        element.click()
        time.sleep(wait_until_confirm_selection + i)
        i += 0.1


def fill_in_element(driver: webdriver.WebDriver, by: By, locator, content,
                    confirm=False):
    config = helper_config.get_config()
    wait_until_confirm_selection = config.getfloat(config.sections()[1],
                                                   'wait_until_confirm_selection')

    # from selenium.webdriver.support.wait import WebDriverWait
    try:
        if retry_element_is_visible(driver, by, locator):
            WebDriverWait(driver, 10).until(
                ec.element_to_be_clickable((by, locator)))
            element = driver.find_element_by_id(locator)
            if retry_element_can_be_filled(driver, By.ID, locator, content):
                if confirm:
                    time.sleep(wait_until_confirm_selection)
                    element.send_keys(Keys.RETURN)
                logging.info("Entered information in %s" % str(locator))

    except NoSuchElementException:
        logging.error("Cannot find the element %s" % str(locator))
    except StaleElementReferenceException:
        logging.error("Element %s is not available" % str(locator))


def retry_element_is_visible(driver: webdriver.WebDriver, by: By, locator):
    result = False
    attempts = 1
    try:
        while attempts < 3 and result is False:
            element = WebDriverWait(driver, 20).until(
                ec.presence_of_element_located((by, locator)))
            if element is not False:
                result = True
            attempts += 1
    except NoSuchElementException and NoSuchElementException:
        pass
    return result


def retry_element_can_be_filled(driver: webdriver.WebDriver, by: By, locator,
                                content):
    """
    :param driver: Driver for the browser
    :type driver: webdriver
    :param by: Locator type for the element
    :type by: selenium.webdriver.common.by.By
    :param locator: Element value for the locator type
    :type locator: str
    :param content: Content to write into the element
    :type content: str
    :return: Return the outcome of the action
    :rtype: bool
    """
    result = False
    attempts = 1
    while attempts < 3 and result is False:
        try:
            element = driver.find_element(by, locator)
            # element.click()
            element.send_keys(Keys.DELETE)
            element.send_keys(content)
            # element.clear()
            result = True
        except StaleElementReferenceException:
            pass
        time.sleep(0.5)
        attempts += 1
    return result


def retry_find_and_click(element: WebElement):
    result = False
    attempts = 1
    while attempts < 3 and result is False:
        try:
            element.click()
            result = True
        except StaleElementReferenceException:
            pass
        attempts += 1
        time.sleep(0.5)
    return result


def switch_to_iframe(driver: webdriver.WebDriver, iframe_id) -> None:
    retry_element_is_visible(driver, By.ID, iframe_id)

    try:
        driver.switch_to.frame(driver.find_element_by_id(iframe_id))
    except NoSuchElementException:
        logging.error("Cannot find the specified iFrame")
    finally:
        return None


def exit_iframe(driver: webdriver.WebDriver):
    driver.switch_to.default_content()


def wait_until_firefox_is_closed(driver: webdriver.WebDriver) -> None:
    browser_is_open = True
    while browser_is_open:
        try:
            driver.get_window_size()
            time.sleep(1)
        except WebDriverException:
            browser_is_open = False


class PageIsFullyLoaded(object):
    def __init__(self):
        pass

    def __call__(self, driver):
        try:
            status = driver.execute_script("return document.readyState")
            return status == "complete"
        except WebDriverException as e:
            raise e


def retry_current_page_is_fully_loaded(driver: webdriver.WebDriver) -> None:
    WebDriverWait(driver, 20).until(PageIsFullyLoaded())




