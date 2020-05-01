"""
Local Activity Command line Tool
=================================
Script that can be run at the command line to execute Garcon activities locally

Run `./local_activity_cli.py --help` for a full list of option
"""

import argparse
import importlib
import json
import logging
import os
import sys
import time

from unittest import mock

from garcon.contrib import util_activity


def list_activities(flow):
    """Find all activities associated with a flow.

    Args:
        flow (module): garcon flow module

    Return:
        str: All valid activity names for a flow
    """

    activity_names_list = util_activity.find_activity_names(flow)

    output = 'Activity names include:'
    for name in activity_names_list:
        output += '\n{}'.format(name)

    return output


def run_activity(flow, context, activity_name):
    """Locally run an activity for a flow with a given context

    Args:
        flow (module): garcon flow module
        context (dict): The flow context
        activity_name (str): name of activity (likely  in the format of
            <flow_name>_<activity_name>)

    Return:
        str: If activity was executed, the context result returned by that
            activity. If not a warning message that the activity was not found
    """

    workflow_activity = util_activity.find_activity(flow, activity_name)
    if not workflow_activity:
        return "Activity name '{}' not found".format(activity_name)

    # monkeypatch heartbeat since we're not connected to aws
    workflow_activity.heartbeat = mock.Mock()

    start = time.time()
    result = workflow_activity.execute_activity(context)
    end = time.time()

    # make context result readable
    result = json.dumps(
        result, sort_keys=True, indent=4, separators=(',', ': '))

    output = (
        'Activity {} executed in {} seconds\n'
        'Heartbeat was called {} times\n'
        'Context Result: {}').format(
            activity_name,
            end - start,
            workflow_activity.heartbeat.call_count,
            result)
    return output


def main(*args):
    """Arg parser method for local activity cli.
    """

    parser = argparse.ArgumentParser(description='Garcon local activity util')
    parser.add_argument(
        'flow', help='flow module [make sure it is in class path]')
    parser.add_argument(
        '-c', '--class', help='Name of the Flow class',
        dest='flow_class', required=False)
    parser.add_argument(
        '-i', '--info', help='set logging to info', action='store_true')
    parser.add_argument(
        '-d', '--debug', help='set logging to debug', action='store_true')

    subparsers = parser.add_subparsers(help='local garcon command', dest='cmd')

    # subparser for list activities cmd
    subparsers.add_parser('list', help='list activities')

    # subparser for run activity cmd
    parser_run = subparsers.add_parser('run', help='run activity')
    parser_run.add_argument(
        'activity', help='Activity to run (<flow_name>_<activity_name>)')
    parser_run.add_argument(
        '-c', '--context', help='initial context [json string]')
    parser_run.add_argument(
        '-cf', '--context-file', help='initial context [json file]')

    # parse cl args (allows easy unit testing)
    args = parser.parse_args(args) if args else parser.parse_args()

    # respect most verbose level of logging set
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    elif args.info:
        logging.basicConfig(level=logging.INFO)

    # patch aws keys so that the flow actvities can
    # instantiate swf.ActivityWorker
    if not os.environ.get('AWS_ACCESS_KEY_ID'):
        os.environ['AWS_ACCESS_KEY_ID'] = ''
    if not os.environ.get('AWS_SECRET_ACCESS_KEY'):
        os.environ['AWS_SECRET_ACCESS_KEY'] = ''

    # import the flow module
    flow = importlib.import_module('{}'.format(args.flow))

    # if flow class is passed, load that (otherwise is a legacy flow module)
    if args.flow_class:
        flow_class_obj = getattr(flow, args.flow_class)
        flow = flow_class_obj()

    if args.cmd == 'run':
        args.context = args.context or '{}'
        args.context = json.loads(args.context)
        # file wins if both params passed
        if args.context_file:
            with open(args.context_file) as context_file:
                args.context = json.load(context_file)
        args.activity = args.activity or '{}'
        output = run_activity(flow, args.context, args.activity)
    elif args.cmd == 'list':
        output = list_activities(flow)
    else:
        sys.exit('Bad Command')

    print(output)


if __name__ == '__main__':
    main()
