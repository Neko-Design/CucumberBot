import os
import yaml
from messaging import send_teams_message, send_slack_message

QUIET_MODE = False

SUPPORTED_WEBHOOKS = {
    'teams': send_teams_message,
    'slack': send_slack_message
}

def load_config_from_file(config_file_path):
    global QUIET_MODE
    config_dict = {}
    try:
        with open(config_file_path, 'r') as config_file:
            config = yaml.load(config_file)
            config_dict['webhooks'] = config['webhooks']
            config_dict['quiet_mode'] = config['quiet_mode']
    except IOError:
        term('No Configuration File Present. Using Defaults', 'WARN')
        config_dict = {
            'webhooks': {
                'teams': [],
                'slack': []
            },
            'quiet_mode': False
        }
    QUIET_MODE = config_dict['quiet_mode']
    return config_dict

def browser_name_from_json(file_name):
    file_name_array = file_name.split('/')
    file_name_unsanitised = file_name_array[len(file_name_array) - 1]
    # Clean Up Display Names
    file_name_sanitised = file_name_unsanitised.replace('.json', '').replace('-', ' ').replace('_', ' ').title().replace('Os X', 'OS-X')
    # Fix MS Edge and IE Names
    file_name_sanitised = file_name_sanitised.replace('Microsoftedge', 'MS Edge').replace("14.14393", "14").replace("Internet Explorer", "IE").replace("15.15063", "15")
    file_name_sanitised = file_name_sanitised.replace('11.103', '11')
    return file_name_sanitised

def publish_path(file_name):
    file_name_array = file_name.split('/')
    file_name_unsanitised = file_name_array[len(file_name_array) - 1]
    file_name_sanitised = file_name_unsanitised.replace('.json', '')
    return file_name_sanitised + '/cucumber-report.html'

def tag_format(tags):
    tagstring = str("")
    for index, item in enumerate(tags):
        tagstring += "`" + item + "`"
        if (index + 1) < len(tags):
            tagstring += ", "
    return tagstring

def term(message, logger = 'INFO'):
    if logger == 'INFO' and not QUIET_MODE:
        print 'INFO: ' + str(message)
        return True
    if logger == 'ERROR':
        print 'ERROR: ' + str(message)
        return True
    if logger == 'WARN' and not QUIET_MODE:
        print 'WARNING: ' + str(message)
        return True
    if logger == 'BANNER':
        print str(message)
        return True
    if not QUIET_MODE:
        print str(message)

def banner():
    banner_art = [
        r"  ____                           _               ",
        r" / ___|   _  ___ _   _ _ __ ___ | |__   ___ _ __ ",
        r"| |  | | | |/ __| | | | '_ ` _ \| '_ \ / _ \ '__|",
        r"| |__| |_| | (__| |_| | | | | | | |_) |  __/ |   ",
        r" \____\__,_|\___|\__,_|_| |_| |_|_.__/ \___|_|"
    ]
    for line in banner_art:
        term(line, 'BANNER')
    term('     CucumberBot v1.0.0 (c) Ewen McCahon', 'BANNER')
    term('     Available under the Apache License' + "\n", 'BANNER')

def send_webhooks(webhooks, report_data):
    for webhook, hooks in webhooks:
        if webhook in SUPPORTED_WEBHOOKS:
            for hook in hooks:
                SUPPORTED_WEBHOOKS[webhook](report_data, hook)