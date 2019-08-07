"""elticket.elticket: provides entry point main()."""

__version__ = "0.2"

from elticket import jira, config as jira_cfg, browser as brwsr
import click
from elticket import helper_config, helper_selenium
from subprocess import Popen
from sys import platform, exit
from selenium.webdriver import Firefox
import logging

editor = ""
if platform == "linux":
    editor = "gedit"
if platform == "win32":
    editor = "notepad.exe"
if platform == "darwin":
    editor = "texteditor"


# TODO: Add unit and acceptance tests

def add_project_option(function):
    project_option = click.option('--project', '-p',
                                  type=click.Choice(['oms3', 'oms4', 'oms6']),
                                  required=True,
                                  help="Set project")
    return project_option(function)


def add_type_option(function):
    type_option = click.option('--type', '-t', 'issue_type',
                               type=click.Choice(['bug', 'feature',
                                                  'improvement']),
                               required=True,
                               help="Set ticket type")
    return type_option(function)


def add_project_and_type_options(function):
    return add_type_option(add_project_option(function))


def verify_jira_user(function):
    def create(*args, **kwargs):
        status = "OK"

        if config_value_is_empty(2, "user_value"):
            print("Please define a Jira username")
            print("Use 'elticket set jira_user <NAME>'")
            status = "NOK"
        if config_value_is_empty(2, "pw_value"):
            print("Please define a Jira password")
            print("Use 'elticket set jira_pw <PASSWORD>'")
            status = "NOK"

        if status == "NOK":
            exit()

        return function(*args, **kwargs)

    return create


def config_value_is_empty(section, key):
    config = helper_config.get_config()
    try:
        if config.get(config.sections()[section], key):
            return False
        else:
            return True
    except KeyError:
        pass


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("elticket " + __version__)
    ctx.exit()


@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True,
              help="Prints version")
@click.group()
def main():
    pass


@main.group()
def set():
    """Set config data"""
    pass


@main.group()
def edit():
    """Edit input data template"""


@main.command(short_help="Create a new JIRA ticket")
@click.option('--browser', '-b', 'browser_option',
              type=click.Choice(['chrome', 'firefox']),
              default='chrome',
              help="Set browser (default: chrome)")
@add_project_and_type_options
@verify_jira_user
def create(project, issue_type, browser_option):
    browser = brwsr.select_browser(browser_option)

    print(
        "Executing automatic E+L Jira ticket creator version {0} ... ".format(
            __version__))

    jira.login(browser)
    jira.check_login(browser)
    jira.open_new_ticket(browser)
    jira.fill_in_project_information(browser, project)
    jira.fill_in_type_information(browser, issue_type)

    config = helper_config.get_config()
    assignee = environment_path = description_path = ""

    if project == "oms6":
        environment_path = jira_cfg.oms6_environment_desc_filepath

        if issue_type == "bug":
            assignee = config.get(config.sections()[2],
                                  'assignee_oms6_bug_value')
            description_path = jira_cfg.oms6_bug_desc_filepath

        elif issue_type == "feature":
            assignee = config.get(config.sections()[2],
                                  'assignee_feature_value')
            description_path = jira_cfg.feature_desc_filepath

        elif issue_type == "improvement":
            assignee = config.get(config.sections()[2],
                                  'assignee_improvement_value')
            description_path = jira_cfg.improvement_desc_filepath

    elif project == "oms4":
        environment_path = jira_cfg.oms4_environment_desc_filepath

        if issue_type == "bug":
            assignee = config.get(config.sections()[2],
                                  'assignee_oms4_bug_value')
            description_path = jira_cfg.oms4_bug_desc_filepath

        elif issue_type == "feature":
            assignee = config.get(config.sections()[2],
                                  'assignee_feature_value')
            description_path = jira_cfg.feature_desc_filepath

        elif issue_type == "improvement":
            assignee = config.get(config.sections()[2],
                                  'assignee_improvement_value')
            description_path = jira_cfg.improvement_desc_filepath

    elif project == "oms3":
        environment_path = jira_cfg.oms3_environment_desc_filepath

        if issue_type == "bug":
            assignee = config.get(config.sections()[2],
                                  'assignee_oms3_bug_value')
            description_path = jira_cfg.oms3_bug_desc_filepath

        elif issue_type == "feature":
            assignee = config.get(config.sections()[2],
                                  'assignee_feature_value')
            description_path = jira_cfg.feature_desc_filepath

        elif issue_type == "improvement":
            assignee = config.get(config.sections()[2],
                                  'assignee_improvement_value')
            description_path = jira_cfg.improvement_desc_filepath

    jira.fill_in_assignee(browser, assignee)
    jira.fill_in_environment_information(browser, issue_type, environment_path)
    jira.fill_in_description(browser, description_path)
    logging.info("Creation complete")
    print("Please enter your data and submit the ticket.")
    print("Close the browser instance afterwards...")

    if isinstance(browser, Firefox):
        helper_selenium.wait_until_firefox_is_closed(browser)


@edit.command(name='environment')
@add_project_option
def open_environment_template(project):
    """Opens environment template file for editing"""

    file = ""

    if project == "oms3":
        file = str(jira_cfg.oms3_environment_desc_filepath)
    elif project == "oms4":
        file = str(jira_cfg.oms4_environment_desc_filepath)
    elif project == "oms6":
        file = str(jira_cfg.oms6_environment_desc_filepath)

    Popen([editor, file])


@edit.command(name="description")
@add_project_and_type_options
def open_description_template(project, issue_type):
    """Opens description template file for editing"""

    file = ""

    if project == "oms3":
        if issue_type == "bug":
            file = str(jira_cfg.oms3_bug_desc_filepath)
        elif issue_type == "improvement":
            file = str(jira_cfg.improvement_desc_filepath)
        elif issue_type == "feature":
            file = str(jira_cfg.feature_desc_filepath)
    elif project == "oms4":
        if issue_type == "bug":
            file = str(jira_cfg.oms4_bug_desc_filepath)
        elif issue_type == "improvement":
            file = str(jira_cfg.improvement_desc_filepath)
        elif issue_type == "feature":
            file = str(jira_cfg.feature_desc_filepath)
    elif project == "oms6":
        if issue_type == "bug":
            file = str(jira_cfg.oms6_bug_desc_filepath)
        elif issue_type == "improvement":
            file = str(jira_cfg.improvement_desc_filepath)
        elif issue_type == "feature":
            file = str(jira_cfg.feature_desc_filepath)

    Popen([editor, file])


@set.command(name="assignee")
@add_project_and_type_options
@click.argument('name')
def set_assignee(project, issue_type, name):
    """Assign new default assignee for certain ticket type"""

    config = helper_config.get_config()

    if project == "oms3":
        if issue_type == "bug":
            config.set(config.sections()[2], 'assignee_oms3_bug_value', name)
        elif issue_type == "improvement":
            config.set(config.sections()[2], 'assignee_improvement_value',
                       name)
        elif issue_type == "feature":
            config.set(config.sections()[2], 'assignee_feature_value', name)
    elif project == "oms4":
        if issue_type == "bug":
            config.set(config.sections()[2], 'assignee_oms4_bug_value', name)
        elif issue_type == "improvement":
            config.set(config.sections()[2], 'assignee_improvement_value',
                       name)
        elif issue_type == "feature":
            config.set(config.sections()[2], 'assignee_feature_value', name)
    elif project == "oms6":
        if issue_type == "bug":
            config.set(config.sections()[2], 'assignee_oms6_bug_value', name)
        elif issue_type == "improvement":
            config.set(config.sections()[2], 'assignee_improvement_value',
                       name)
        elif issue_type == "feature":
            config.set(config.sections()[2], 'assignee_feature_value', name)

    helper_config.write_to_config(config, 2, )


@set.command(name="firefox_profile")
@click.argument('path')
def set_firefox_profile_path(path):
    """Set path to used Firefox profile"""
    helper_config.write_to_config(1, 'firefox_profile_dir', path)


@set.command(name="have_dns")
@click.argument('have_dns')
def set_have_dns(have_dns):
    """Set whether local PC has access to DNS server"""
    helper_config.write_to_config(0, 'have_dns', have_dns)


@set.command(name="jira_user")
@click.argument("jira_user")
def set_jira_user(jira_user):
    """Set your JIRA username"""
    helper_config.write_to_config(2, "user_value", jira_user)


@set.command(name="jira_pw")
@click.argument("jira_pw")
def set_jira_user(jira_pw):
    """Set your JIRA password"""
    helper_config.write_to_config(2, "pw_value", jira_pw)
