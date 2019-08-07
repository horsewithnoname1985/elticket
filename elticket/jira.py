from elticket.helper_selenium import *
from elticket.elements import elements_jira
from selenium.webdriver.firefox import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import logging
from selenium.common.exceptions import WebDriverException

logging.basicConfig(level=logging.INFO,
                    format=" %(asctime)s - %(levelname)s - %(message)s")


def login(browser: webdriver.WebDriver):
    """
    The login(driver) function is used to login into JIRA

    :param browser: instance of a selenium.webdriver() object
    :return: No return value
    """
    from elticket import helper_config
    config = helper_config.get_config()
    have_dns = config.getboolean(config.sections()[0], 'have_dns')
    homepage_url_no_dns = config.get(config.sections()[0],
                                     'homepage_url_no_dns')
    homepage_url = config.get(config.sections()[0], 'homepage_url')
    login_user = config.get(config.sections()[2], 'user_value')
    login_pw = config.get(config.sections()[2], 'pw_value')

    if have_dns:
        browser.get(homepage_url)
    else:
        browser.get(homepage_url_no_dns)

    fld_user = browser.find_element_by_id(elements_jira.fld_login_user_id)
    fld_user.click()
    retry_element_is_focused(browser, fld_user)
    fld_user.send_keys(login_user)

    fld_pw = browser.find_element_by_id(elements_jira.fld_login_pw_id)
    fld_pw.click()
    retry_element_is_focused(browser, fld_pw)
    fld_pw.send_keys(login_pw)

    btn_login = browser.find_element_by_id(elements_jira.btn_login_id)
    btn_login.click()


def check_login(browser: webdriver.WebDriver):
    """
    The check_login(driver) function is used to verify, whether the first try
    to log-in to JIRA has been successful. If not, this function retries to
    login until successful

    :param browser: instance of a selenium.webdriver() object
    :return: No return value
    """

    waitelement = WebDriverWait(browser, 1)

    for i in range(1, 60, 1):
        try:
            waitelement.until(EC.presence_of_element_located(
                (By.ID, elements_jira.btn_dropdown_project_id)))
            logging.info("Login was successful")
            return
        except WebDriverException:
            pass
        try:
            waitelement.until(EC.presence_of_element_located(
                (By.ID, elements_jira.fld_login_failed)))
            logging.info("Login was unsuccessful. Retrying...")
            login(browser)
        except WebDriverException:
            pass

    logging.error("Login not successful")


def open_new_ticket(browser: webdriver.WebDriver):
    """
    The open_new_ticket(browser) function opens a new ticket without any
    further specifications
    :param browser: instance of a selenium.webdriver() object
    :return: No return value
    """
    try:
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(
                (By.ID, elements_jira.btn_newissue_id)))
        WebDriverWait(browser, 20).until(
            EC.visibility_of_element_located(
                (By.ID, elements_jira.section_dashboard_id))
        )
        time.sleep(0.5)
    finally:
        bt_create = browser.find_element_by_id(elements_jira.btn_newissue_id)
        bt_create.click()
        logging.info("Creating new issue ticket ...")


def fill_in_project_information(browser: webdriver.WebDriver, project):
    """
    The fill_in_project_information(browser, project) functions fills in the
    project info into the designated field
    :param browser: instance of a selenium.webdriver() object
    :param project: String input value for the 'project' field
    :return: No return value
    """

    fill_in_element(browser, By.ID, elements_jira.fld_projectname_id, project,
                    confirm=True)
    time.sleep(1)


def fill_in_type_information(browser: webdriver.WebDriver, issue_type):
    """
    The fill_in_type_information(browser, issue_type) method inserts the ticket
    type information into the designated field
    :param browser: instance of a selenium.webdriver() object
    :param issue_type: String input value for the 'type' field

    :return: No return value
    """

    fill_in_element(browser, By.ID, elements_jira.fld_issuetype_id, issue_type,
                    confirm=True)
    time.sleep(1)


def fill_in_description(browser: webdriver.WebDriver, desc_template_path):
    """
    The fill_in_desc_template(browser, desc_template_path) fills the content of
    the description text file into the designated field
    :param browser: instance of a selenium.webdriver() object
    :param desc_template_path: Path to the description input text file
    :return: No return value
    """
    try:
        browser.find_element(By.LINK_TEXT,
                             elements_jira.tab_info_link_text).click()
    except NoSuchElementException and StaleElementReferenceException:
        logging.error("'Info' tab not found")

    browser.find_element_by_link_text(
        elements_jira.btn_description_fld_text_link_text).click()
    fill_in_element(browser, By.ID, elements_jira.fld_description_id,
                    open(desc_template_path).read())


def fill_in_assignee(browser: webdriver.WebDriver, assignee: str) -> None:
    """
    The fill_in_assignee(browser, assignee, tab_assign_xpath) function fills
    the assignee text string into the designated field and confirms the
    selection in the browser
    :param browser: instance of a selenium.webdriver() object
    :param assignee: String of the assignee value
    :return: No return value
    """

    try:
        browser.find_element(By.LINK_TEXT,
                             elements_jira.tab_assign_link_text).click()

    except NoSuchElementException and StaleElementReferenceException:
        logging.error("'Assignee' tab not found")

    fill_in_element(browser, By.ID, elements_jira.fld_assigne_id, assignee,
                    confirm=True)


def fill_in_bug_environment_information(browser: webdriver.WebDriver,
                                        env_template_path: str) -> None:
    """
    :param browser: instance of a selenium.webdriver() object
    :param env_template_path: Path of the file that contains the environment
    information text
    :return: No return value
    """

    try:
        browser.find_element(By.LINK_TEXT,
                             elements_jira.tab_bug_details_link_text).click()

    except NoSuchElementException and StaleElementReferenceException:
        logging.error("'Bug Details' tab not found")

    browser.find_element_by_link_text(
        elements_jira.btn_environment_fld_text_link_text).click()

    fill_in_element(browser, By.ID, elements_jira.fld_environment_id,
                    open(env_template_path).read(), confirm=True)


def fill_in_improv_and_feature_environment_information(
        browser: webdriver.WebDriver, env_template_path: str) -> None:
    """
    :param browser: instance of a selenium.webdriver() object
    :param env_template_path: Path of the file that contains the environment
    information text
    :return: No return value
    """

    try:
        browser.find_element(By.LINK_TEXT,
                             elements_jira.tab_improvement_others_link_text).click()

    except NoSuchElementException and StaleElementReferenceException:
        logging.error("'Others' tab not found")

    browser.find_element_by_link_text(
        elements_jira.btn_environment_fld_text_link_text).click()

    with open(env_template_path, 'r') as env_template:
        fill_in_element(browser, By.ID, elements_jira.fld_environment_id,
                        env_template.read(), confirm=True)


def fill_in_environment_information(browser: webdriver.WebDriver,
                                    issue_type: str,
                                    template_path: str) -> None:
    """
    :param browser: instance of a selenium.webdriver() object
    :param template_path: Path of the file that contains the environment
    information text
    :param issue_type: Issue name
    :return: No return value
    """
    if issue_type == "bug":
        try:
            browser.find_element(By.LINK_TEXT,
                                 elements_jira.tab_bug_details_link_text).click()

        except NoSuchElementException and StaleElementReferenceException:
            logging.error("'Bug Details' tab not found")

        browser.find_element_by_link_text(
            elements_jira.btn_environment_fld_text_link_text).click()

    elif issue_type == "improvement" or "feature":
        try:
            browser.find_element(By.LINK_TEXT,
                                 elements_jira.tab_improvement_others_link_text).click()

        except NoSuchElementException and StaleElementReferenceException:
            logging.error("'Others' tab not found")

        browser.find_element_by_link_text(
            elements_jira.btn_environment_fld_text_link_text).click()

    else:
        logging.error(
            "Environment info cannot be inserted for type " + issue_type)
        pass

    with open(template_path, 'r') as env_template:
        fill_in_element(browser, By.ID, elements_jira.fld_environment_id,
                        env_template.read(), confirm=True)
