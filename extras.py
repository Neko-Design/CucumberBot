import os

QUIET_MODE = False

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

def term(message):
    if not QUIET_MODE:
        print message

def banner():
    banner_art = [
        r"  ____                           _               ",
        r" / ___|   _  ___ _   _ _ __ ___ | |__   ___ _ __ ",
        r"| |  | | | |/ __| | | | '_ ` _ \| '_ \ / _ \ '__|",
        r"| |__| |_| | (__| |_| | | | | | | |_) |  __/ |   ",
        r" \____\__,_|\___|\__,_|_| |_| |_|_.__/ \___|_|"
    ]
    for line in banner_art:
        term(line)
    term('     CucumberBot v1.0.0 (c) Ewen McCahon')
    term('     Available under the Apache License' + "\n")