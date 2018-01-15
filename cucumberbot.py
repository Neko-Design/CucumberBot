import os
import ast
from cukejson import CukeJson
from extras import browser_name_from_json, tag_format, publish_path, term, banner,load_config_from_file, send_webhooks, QUIET_MODE

# CucumberBot
# Written by Ewen McCahon
# Copyright (c) Ewen McCahon 2018

TEST_ASSET_PATH = os.environ['ASSET_PATH']
TEST_SUITE_NAME = os.environ['TEST_SUITE_NAME']
PUBLISH_BASE = os.environ['PUBLISH_BASE']
try:
    TAGS = os.environ['CUKE_TAGS']
except KeyError:
    TAGS = '[]'
NICE_TAGS = ast.literal_eval(TAGS)
try:
    BOT_CONFIG = os.environ['BOT_CONFIG']
except KeyError:
    BOT_CONFIG = './config.yml'
CONFIG = load_config_from_file(BOT_CONFIG)

term('Report Directory: ' + TEST_ASSET_PATH)

def reports_in_directory(report_directory):
    """
    reports_in_directory(report_directory)
    Generate a Summary for All JSON Reports in a Directory
    """
    dir_listing = os.listdir(report_directory)
    json_files = []
    for entry in dir_listing:
        report_path = os.path.join(report_directory, entry)
        if os.path.isfile(report_path):
            if '.json' in entry:
                term('Processing Report: ' + entry)
                cuke_report = CukeJson(report_path, quiet_mode=QUIET_MODE)
                json_files.append({
                    'browser_name': browser_name_from_json(report_path),
                    'report_url': PUBLISH_BASE + TEST_ASSET_PATH + publish_path(report_path),
                    'report': cuke_report,
                })
    return json_files

def generate_report():
    """
    generate_report()
    Main Function to Generate Reports
    Requires Environment Variables Listed in test.sh
    """
    cucumber_reports = reports_in_directory(TEST_ASSET_PATH)
    if len(cucumber_reports) < 1:
        return None
    report_container = {
        'test_suite_name': TEST_SUITE_NAME,
        'results': {},
        'links': {},
        'tags': tag_format(NICE_TAGS)
    }
    failed_test = False
    errored_test = False
    overall_result = 'Passed'
    for report_data in cucumber_reports:
        report = report_data['report']
        if not report.has_errors():
            scenarios = report.get_total_scenarios()
            passed = report.get_passed_scenarios()
            result_string = str(passed) + "/" + str(scenarios) + " Scenarios Passed"
            term(report_data['browser_name'] + ': ' + result_string)
            report_container['results'][report_data['browser_name']] = result_string
            report_container['links'][report_data['browser_name']] = report_data['report_url']
            if report.get_build_status() == 'Failed':
                failed_test = True
        else:
            errored_test = True
    if errored_test:
        overall_result = 'Errored'
    elif failed_test:
        overall_result = 'Failed'
    report_container['result'] = overall_result
    term(report_container)
    return report_container

if __name__ == '__main__':
    banner()
    generated_report = generate_report()
    if generated_report != None:
        send_webhooks(CONFIG['webhooks'].items(), generated_report)
    else:
        term('No Reports in Directory: ' + str(TEST_ASSET_PATH), 'ERROR')
        exit(1)
