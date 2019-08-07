from Jira.elements import elements_weasel as wbm_cfg

from selenium.webdriver.firefox import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import Select

import pyautogui
import time
import logging


def login(browser: webdriver.WebDriver):
    browser.set_page_load_timeout(5)
    try:
        browser.get(wbm_cfg.homepage_url)
    except WebDriverException:
        browser.refresh()
    finally:
        pyautogui.typewrite(wbm_cfg.login_user_value)
        pyautogui.typewrite("\t")
        pyautogui.typewrite(wbm_cfg.login_pw_value)
        pyautogui.typewrite("\n")
        logging.info("Login executed")
        wait_for_page(browser, wbm_cfg.homepage_url,
                      wbm_cfg.main_page_attr_xpath)


def go_to_page(browser: webdriver.WebDriver, url, test_element_xpath):
    if browser.current_url != url:
        browser.set_page_load_timeout(3)
        try:
            browser.get(url)
        except TimeoutException:
            try:
                browser.set_page_load_timeout(10)
                browser.get(url)
            except TimeoutException:
                logging.error("The URL " + url + " is unreachable")
                browser.close()

    wait_for_page(browser, url, test_element_xpath)


def wait_for_page(browser: webdriver.WebDriver, url, test_element_xpath):
    try:
        wait_element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, test_element_xpath)))
    except TimeoutException:
        logging.error(str(url) + " could not be successfully loaded")

    finally:
        if "iframe" in test_element_xpath:
            browser.switch_to.frame(
                browser.find_element_by_xpath(test_element_xpath))
            logging.info("Selected iFrame")

        return

        # TODO: Add cases for all known weasel websites, if an iframe exists and must be switched to


def get_config(browser: webdriver.WebDriver):
    go_to_page(browser, wbm_cfg.recoverysite_url,
               wbm_cfg.iframe_recovery_xpath)

    bt_dwnl_conf = browser.find_element_by_name(wbm_cfg.btn_name_downl_conf)
    bt_dwnl_conf.click()

    time.sleep(2)
    pyautogui.typewrite("\n")
    logging.info("Config file download is started")
    browser.switch_to.default_content()


def get_middleware_log(browser: webdriver.WebDriver):
    go_to_page(browser, wbm_cfg.logsite_url, wbm_cfg.iframe_logs_xpath)

    dd_view_log = Select(
        browser.find_element_by_tag_name(wbm_cfg.btn_dropdown_logview_name))
    try:
        dd_view_log.select_by_value(wbm_cfg.filename_middleware_log)
        logging.info("Selected middleware log file")
    except NoSuchElementException:
        logging.error(str(dd_view_log) + " - No such dropdown element found")

    bt_dwnl_log = browser.find_element_by_name(
        wbm_cfg.btn_download_logfile_name)
    bt_dwnl_log.click()
    time.sleep(2)
    pyautogui.press("down")
    pyautogui.typewrite("\n")
    browser.switch_to.default_content()


def get_backend_log(browser: webdriver.WebDriver):
    go_to_page(browser, wbm_cfg.logsite_url, wbm_cfg.iframe_logs_xpath)

    dd_view_log = Select(
        browser.find_element_by_tag_name(wbm_cfg.btn_dropdown_logview_name))
    dd_view_log.select_by_value(wbm_cfg.filename_backend_log)
    bt_dwnl_log = browser.find_element_by_name(
        wbm_cfg.btn_download_logfile_name)
    bt_dwnl_log.click()
    time.sleep(2)
    pyautogui.typewrite("\n")
    browser.switch_to.default_content()


def get_report(browser: webdriver.WebDriver):
    browser.set_page_load_timeout(10)

    elv_mngmnt_drpdwn = browser.find_element_by_xpath(
        wbm_cfg.drpdwn_elvr_mngmnt_xpath)
    elv_mngmnt_drpdwn.click()
    element = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.XPATH, wbm_cfg.btn_downl_report_xpath)))
    element.click()

    time.sleep(5)
    logging.info("Report file download is started")


def get_jobs(browser: webdriver.WebDriver):
    go_to_page(browser, wbm_cfg.recoverysite_url,
               wbm_cfg.iframe_recovery_xpath)

    bt_dwnl_conf = browser.find_element_by_name(wbm_cfg.btn_name_downl_jobs)
    bt_dwnl_conf.click()

    time.sleep(2)
    pyautogui.typewrite("\n")
    logging.info("Jobs file download is started")
    browser.switch_to.default_content()
