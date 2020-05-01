"""
Util for garcon.Activity helper methods

This module will be deprecated once these are added to garcon
"""

from garcon import activity


def find_activity(flow, activity_name):
    """Get activity from a flow based on that activity's name

    Args:
        flow (module): garcon flow module
        activity_name (str): name of activity (likely in the format of
            <flow_name>_<activity_name>)

    Return:
        Activity instance with matching activity_name, None if no match
    """

    workflow_activities = activity.find_workflow_activities(flow)
    for workflow_activity in workflow_activities:
        if workflow_activity.name == activity_name:
            return workflow_activity

    return None


def find_activity_names(flow):
    """Get list of all activity names for a garcon flow module

    Args:
        flow (module): garcon flow module

    Return:
        List of all activity names in the flow
    """

    activity_names = []
    workflow_activities = activity.find_workflow_activities(flow)
    for workflow_activity in workflow_activities:
        activity_names.append(workflow_activity.name)
    return activity_names
