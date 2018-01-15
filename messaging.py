import requests

JSON_HEADER = {'Content-type': 'application/json'}

def clean_json(json_string):
    formatted_msg = str(json_string).replace(r"'", "\"")
    formatted_msg = formatted_msg.replace("$q$", "'")
    return formatted_msg

def status_check(response_object):
    status_code = response_object.status_code
    if status_code == 200:
        print "  - OK"
    elif 399 < status_code < 499:
        print "  - REQUEST ERROR: " + str(response_object.text)
    elif 499 < status_code < 599:
        print "  - SERVER ERROR: " + str(response_object.text)

def generate_cards_facts(source_dict):
    formatted_dict = []
    for (key, value) in source_dict.items():
        formatted_dict.append({
            'name': key,
            'value': value
        })
    return formatted_dict

def send_teams_message(report_container, webhook_url):
    """
    Send Teams Message
    Post Message to Teams Channel via Webhook URL
    """
    print 'Sending Teams Message: ' + webhook_url
    message_object = {
        'sections': [
            {
                'activityTitle': 'Summary Report for ' + report_container['test_suite_name'],
                'activitySubtitle': 'Test Suite ' + report_container['result'],
                'facts': [
                    {'name': 'Tags Executed', 'value': report_container['tags']}
                ]
            },
            {
                'activityTitle': 'Results by Browser',
                'facts': generate_cards_facts(report_container['results'])
            }
        ],
        '@type': 'MessageCard',
        'summary': 'Summary Report For Jbwere Automated Testing: Error'
    }
    teams_msg = requests.post(webhook_url, headers=JSON_HEADER,
                              data=clean_json(message_object))
    status_check(teams_msg)

def send_slack_message(report_container, webhook_url):
    """
    Send Slack Message
    Post Message to Slack Channel via Webhook URL
    """
    # TODO: Implement Slack Messages
    print 'Sending Slack Message: ' + webhook_url