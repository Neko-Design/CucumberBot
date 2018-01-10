# CukeJSON Report Library
# Reads Cucumber JSON Reports
# Written by Ewen McCahon
# Copyright (c) Ewen McCahon 2018

import json
import requests

# Main Vars
BASE_URL = 'http://neko.ac/reports/'

if __name__ == "__main__":
    print "CukeJSON Report Library"

class CukeJson:
    """
    CukeJSON
    Main Controller for Cucumber JSON Reader
    Setting the second parameter to true will ignore base url
    Setting the third parameter to true will enable quiet mode
    usage: cukejson('json_url', False, False)
    """

    def is_local_path(self, pathfragment):
        if "://" in pathfragment:
            return False
        return True

    def get_json_from_disk(self, jsonpath):
        try:
            with open(jsonpath) as data_file:
                data = json.load(data_file)
                return data
        except EnvironmentError as error:
            print "*ERROR* Couldn't read JSON from Disk"
            print str(error)
            return {"error": "Error Loading JSON"}

    def get_json_from_url(self, json_url):
        proxies = {
            "http": None,
            "https": None,
        }
        try:
            response = requests.get(json_url, proxies=proxies)
            try:
                response_json = response.json()
                return response_json
            except ValueError as error:
                print "Invalid JSON returned: " + error
                return {"error": "Invalid JSON"}
        except:
            print "ERROR: " + str(response.status_code) + " " + json_url
            return {"error": "Invalid Response: " + str(response.status_code)}

    # Init Func
    def __init__(self, json_url, full_url=False, quiet_mode=False):
        if not quiet_mode:
            print "Reading JSON: " + json_url
        if self.is_local_path(json_url):
            self.reportjson = self.get_json_from_disk(json_url)
        else:
            self.jsonpath = str("")
            if not full_url:
                self.jsonpath += str(BASE_URL)
            self.jsonpath += str(json_url)
            self.reportjson = self.get_json_from_url(self.jsonpath)

    def has_errors(self):
        if 'error' in self.reportjson:
            return True
        return False

    def get_total_scenarios(self):
        scenarios = 0
        try:
            for scenario in self.reportjson:
                scenarios += len(scenario['elements'])
        except:
            print "ERROR COUNTING SCENARIOS"
            print "========================"
            scenarios = 0
        return scenarios

    def get_passed_scenarios(self):
        passes = 0
        try:
            for scenario in self.reportjson:
                for element in scenario['elements']:
                    failed = False
                    for step in element['steps']:
                        if step['result']['status'] != "passed":
                            failed = True
                    if not failed:
                        passes = passes + 1
        except:
            print "ERROR COUNTING PASSES"
            print "====================="
        return passes

    def get_failed_scenarios(self):
        fails = 0
        try:
            fails = self.get_total_scenarios() - self.get_passed_scenarios()
        except:
            print "ERROR COUNTING FAILS"
            print "===================="
        return fails

    def get_build_status(self):
        if self.has_errors():
            return 'Errored'
        if self.get_failed_scenarios() > 0:
            return 'Failed'
        if self.get_failed_scenarios() == 0:
            return 'Passed'

    def get_json_url(self):
        return self.jsonpath