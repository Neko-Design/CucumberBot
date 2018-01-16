# CucumberBot
Cucumber Report Parser and Results Notifier

## What Does It Do?
CucumberBot works with your existing [Cucumber](https://cucumber.io/) based testing framework and generates concise summaries which can then be sent out to your developers via Slack, Teams, Emails etc. enabling a faster, more transparent development pipeline.

## How Do I Use It?
Clone this repository into your build directory and configure your environment with a small number of additional variables telling CucumberBot what directories to scan, what the publishing base URL is, and what tags you executed. CucumberBot will then parse all the reports in that directory and generate a summary, and optioanlly send this as a message to your specified chat tools.

### Getting Started
You can use `test.sh` as a base to configure your environment. In your chosen build tool, set up 4 new environment variables:

| Variable Name   | Value |
|-----------------|-------|
| ASSET_PATH      | Relative Path to Test Reports. `reports/cucumber-reports/` |
| TEST_SUITE_NAME | Friendly Name for Test Suite. `Neko Automated Tests` |
| PUBLISH_BASE    | Base URL for HTML Reports (If Enabled). `https://neko.ac/reports/` |
| CUKE_TAGS       | Tags Executed, Formatted as an Array. `["@tag1", "@tag2"]`|
| BOT_CONFIG      | Optional. Path to .yml file with webhook configuartion. See sample config file in repo |

Build tools such as Jenkins and TeamCity allow you to use substitution in these paths, so that you can generate a report for every build. CI Tools enable CucumberBot to deliver maximum value. The Jenkins [HTML Publisher plugin](https://wiki.jenkins.io/display/JENKINS/HTML+Publisher+Plugin) is what I've been using in combination with CucumberBot, it works quite well.

# License
Licensed under v2.0 of the Apache License. Please read the attached license contained within the LICENSE file in this directory.
