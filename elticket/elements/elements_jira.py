import os
from pathlib import Path

# # DNS
# have_dns = False
#
# # Timeouts
# wait_until_confirm_selection = 0.5
#
# # URLs
# homepage_url = "https://eljira.els.local:8443/secure/Dashboard.jspa"
# homepage_url_no_dns = "https://10.1.111.27:8443/secure/Dashboard.jspa"

# Values
# user_value = "Wohletzar"
# pw_value = "ha_gre_da_1992"
# project_value = "ELSCAN OMS6"
# issuetype_bug_value = "Bug"
# issuetype_improvement_value = "Improvement"
# issuetype_feature_value = "New Feature"
# assignee_oms3_bug_value = "Andreas Fuchs"
# assignee_oms4_bug_value = "Ken Weisheit"
# assignee_oms6_bug_value = "Heiko Geissler"
# assignee_improvement_value = "Markus Bauer"
# assignee_feature_value = "Markus Bauer"

# Files
# desc_bug_file_dir = open(os.path.abspath("./templates/oms6_jira_bug_desc.txt"))
# desc_improvement_file_dir = open(os.path.abspath("./templates/jira_improvement_desc.txt"))
# desc_feature_file_dir = open(os.path.abspath("./templates/jira_feature_desc.txt"))
# environment_file_dir = open(os.path.abspath("./templates/oms6_jira_environment_desc.txt"))

# oms3_bug_desc_file_dir = open(os.path.abspath("../../templates/oms3_jira_bug_desc.txt"))
# oms3_environment_desc_file_dir = open(os.path.abspath("../../templates/oms3_jira_environment_desc.txt"))
# oms4_bug_desc_file_dir = open(os.path.abspath("../../templates/oms4_jira_bug_desc.txt"))
# oms4_environment_desc_file_dir = open(os.path.abspath("../../templates/oms4_jira_environment_desc.txt"))
# oms6_bug_desc_file_dir = open(os.path.abspath("../../templates/oms6_jira_bug_desc.txt"))
# oms6_environment_desc_file_dir = open(os.path.abspath("../../templates/oms6_jira_environment_desc.txt"))
#
# improvement_desc_file_dir = open(os.path.abspath("../../templates/jira_improvement_desc.txt"))
# feature_desc_file_dir = open(os.path.abspath("../../templates/jira_feature_desc.txt"))

# desc_bug_file_dir = open(os.path.abspath(os.getcwd() + "../../templates/oms6_jira_bug_desc.txt"))
# desc_improvement_file_dir = open(os.path.abspath(os.getcwd() + "../../templates/jira_improvement_desc.txt"))
# desc_feature_file_dir = open(os.path.abspath(os.getcwd() + "../../templates/jira_feature_desc.txt"))
# environment_file_dir = open(os.path.abspath(os.getcwd() + "../../templates/oms6_jira_environment_desc.txt"))
# desc_bug_file_dir = open("C:\\OMS6_Scripts\\common_scripts\\templates\\oms6_jira_bug_desc.txt")
# desc_improvement_file_dir = open("C:\\OMS6_Scripts\\common_scripts\\templates\\jira_improvement_desc.txt")
# desc_feature_file_dir = open("C:\\OMS6_Scripts\\common_scripts\\templates\\jira_feature_desc.txt")
# environment_file_dir = open("C:\\OMS6_Scripts\\common_scripts\\templates\\oms6_jira_environment_desc.txt")

# Elements
frm_newticket_xpath = "/html/body/div[3]/div[2]/div[1]/div/form/div[1]"
tab_info_css = "[href*='#tab-0']"
tab_info_link_text = "Info"
tab_assign_link_text = "Assign"
tab_bug_details_link_text = "Bug Details"
tab_improvement_others_link_text = "Other"
tab_improvement_assign_xpath = "/html/body/div[3]/div[2]/div[1]/div/form/div[1]/div[2]/div/ul/li[4]/a"
tab_improvement_others_xpath = "/html/body/div[3]/div[2]/div[1]/div/form/div[1]/div[2]/div/ul/li[6]/a"
tab_feature_assign_xpath = "/html/body/div[3]/div[2]/div[1]/div/form/div[1]/div[2]/div/ul/li[4]/a"
tab_feature_others_xpath = "/html/body/div[3]/div[2]/div[1]/div/form/div[1]/div[2]/div/ul/li[6]/a"
fld_login_user_id = "login-form-username"
fld_login_pw_id = "login-form-password"
fld_login_failed = "usernameerror"
fld_projectname_id = "project-field"
fld_issuetype_id = "issuetype-field"
fld_description_id = "description"
fld_assigne_id = "assignee-field"
fld_environment_id = "environment"
btn_login_id = "login"
btn_newissue_id = "create_link"
btn_dropdown_project_id = "browse_link"
btn_environment_fld_text_link_text = "Text"
btn_description_fld_text_link_text = "Text"
iframe_description_id = "mce_7_ifr"
iframe_environment_id = "mce_8_ifr"
section_dashboard_id = "dashboard-content"
