from pathlib import Path
from sys import platform
from os.path import abspath, dirname


# PATHS
def get_config_base_path():
    base_path = Path()
    if platform in ("linux", "darwin"):
        return base_path.joinpath(Path.home().joinpath(".elticket"))
    if platform == "win32":
        return base_path.joinpath("c:/ProgramData/elticket")


def get_template_path():
    return get_config_base_path().joinpath("templates")


BASE_DIR = get_config_base_path()
TEMPLATE_DIR = get_template_path()

# config.ini
config_ini_filepath = Path(dirname(abspath(__file__))).joinpath("config.ini")

# oms3
oms3_bug_desc_filepath = TEMPLATE_DIR.joinpath("oms3_jira_bug_desc.txt")
oms3_environment_desc_filepath = TEMPLATE_DIR.joinpath(
    "oms3_jira_environment_desc.txt")

# oms4
oms4_bug_desc_filepath = TEMPLATE_DIR.joinpath("oms4_jira_bug_desc.txt")
oms4_environment_desc_filepath = TEMPLATE_DIR.joinpath(
    "oms4_jira_environment_desc.txt")

# oms6
oms6_bug_desc_filepath = TEMPLATE_DIR.joinpath("oms6_jira_bug_desc.txt")
oms6_environment_desc_filepath = TEMPLATE_DIR.joinpath(
    "oms6_jira_environment_desc.txt")

# all projects
improvement_desc_filepath = TEMPLATE_DIR.joinpath("jira_improvement_desc.txt")
feature_desc_filepath = TEMPLATE_DIR.joinpath(
    "jira_feature_desc.txt")
