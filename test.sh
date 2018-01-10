#!/bin/bash

export ASSET_PATH='cuke-reports/reports/' # Disk Path Relative to CucumberBot Script
export TEST_SUITE_NAME='Neko Automated Tests' # Display Name for Test Suite
export PUBLISH_BASE='https://neko.ac/reports/' # Base URL for HTML Reports
export CUKE_TAGS='["@neko-tests", "@regression"]' # Tags Executed

python cucumberbot.py