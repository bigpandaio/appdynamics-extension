#!/usr/bin/python

import sys
import json
import urllib2
import ConfigParser
import socket
import time
import os
import logging
import logging.handlers


current_dir = os.path.realpath(os.path.dirname(__file__))
CONFIG_FILE = os.path.join(current_dir, 'config.ini')
BP_BASE_URL = 'http://10.0.10.17:1337'
TIMEOUT=120

LOG_FILE = '/tmp/bigpanda.action.log'
LOG_MAX_BYTES = 2.5 * 1024 * 1024 # 2.5 MB
LOG_BACKUP_COUNT = 1 # Two files overall

# Check input
if len(sys.argv) < 14:
    print "%s: doesn't look like appdynamics health rule run, quitting" % sys.argv[0]
    sys.exit(0)

# Init logging object
log = logging.getLogger("bigpanda.appdynamics")
log.addHandler(logging.NullHandler())
log.setLevel(logging.INFO)

# Parse config file
try:
    config = ConfigParser.SafeConfigParser()
    config.read(CONFIG_FILE)
    api_token = config.get('base', 'api_token')
    app_key = config.get('base', 'app_key')
except Exception as e:
    sys.stderr.write("Failed to parse bigpanda.ini file: %s" % str(e))
    sys.exit(1)

if config.has_option('base', 'logging') and config.get('base', 'logging').lower() in ['1', 'true', 'yes']:
   log_handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=LOG_MAX_BYTES, backupCount=LOG_BACKUP_COUNT)
   log.addHandler(log_handler)

try:
    # All args are surrounded by quotes, so we need to remove them
    unquoted_args = map(lambda x: x[1:-1], sys.argv)

    # Parse args
    log.info("Parsing command line arguments")
    params = dict()

    ( params['app_name'],
      params['app_id'],
      params['pvn_alert_time'],
      params['priority'],
      params['severity'],
      params['tag'],
      params['health_rule_name'],
      params['health_rule_id'],
      params['pvn_time_period_in_minutes'],
      params['affected_entity_type'],
      params['affected_entity_name'],
      params['affected_entity_id'],
      number_of_evaluation_entities ) = unquoted_args[1:14]
      
    args_index = 14
    number_of_evaluation_entities = int(number_of_evaluation_entities)
    params['evaluation_entities'] = []
    for n in xrange(number_of_evaluation_entities):
        evaluation_entity = dict()
        evaluation_entity['evaluation_entity_type'] = unquoted_args[args_index]
        evaluation_entity['evaluation_entity_name'] = unquoted_args[args_index+1]
        evaluation_entity['evaluation_entity_id'] = unquoted_args[args_index+2]
        number_of_triggered_conditions = int(unquoted_args[args_index+3])
        args_index += 4

        evaluation_entity['triggered_conditions'] = []
        for c in xrange(number_of_triggered_conditions):
            triggered_condition = dict()
            triggered_condition['scope_type'] = unquoted_args[args_index]
            triggered_condition['scope_name'] = unquoted_args[args_index+1]
            triggered_condition['scope_id'] = unquoted_args[args_index+2]
            triggered_condition['condition_name'] = unquoted_args[args_index+3]
            triggered_condition['condition_id'] = unquoted_args[args_index+4]
            triggered_condition['operator'] = unquoted_args[args_index+5]
            triggered_condition['condition_unit_type'] = unquoted_args[args_index+6]
            if triggered_condition['condition_unit_type'].startswith('BASELINE_'):
                triggered_condition['use_default_baseline'] = unquoted_args[args_index+7].lower() == 'true' and True or False
                if not triggered_condition['use_default_baseline']:
                    triggered_condition['baseline_name'] = unquoted_args[args_index+8]
                    triggered_condition['baseline_id'] = unquoted_args[args_index+9]
                    args_index += 10
                else:
                    args_index += 8
            else:
                args_index += 7
            triggered_condition['threshold_value'] = unquoted_args[args_index]
            triggered_condition['observed_value'] = unquoted_args[args_index+1]
            args_index += 2

            evaluation_entity['triggered_conditions'].append(triggered_condition)

        params['evaluation_entities'].append(evaluation_entity)

    params['summary_message'] = unquoted_args[args_index]
    params['incident_id'] = unquoted_args[args_index+1]
    params['deep_link_url'] = unquoted_args[args_index+2]
    params['event_type'] = unquoted_args[args_index+3]

    # Prepare and send HTTP request
    data = json.dumps(params)
    headers = { "Content-Type": "application/json", "Authorization": "Bearer " + api_token }
    url = '%s/data/integrations/appdynamics?app_key=%s' % (BP_BASE_URL, app_key)
    log.info("Sending request")
    log.debug("Request url is: %s", url)
    log.debug("Request data is: %s", data)
    request = urllib2.Request(url=url, headers=headers, data=data)
    socket.setdefaulttimeout(TIMEOUT)
    urllib2.urlopen(request)
except:
    log.exception("Error while running script")
