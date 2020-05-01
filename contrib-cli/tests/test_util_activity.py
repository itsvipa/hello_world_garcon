from garcon import activity
from garcon.contrib import util_activity


def test_find_activity(monkeypatch):
    """Test that we find an activity in a flow"""

    monkeypatch.setattr(activity.Activity, '__init__', lambda self: None)
    from tests.fixtures import flow_cli

    activity_1 = util_activity.find_activity(
        flow_cli, 'workflow_sample_activity_1')

    assert isinstance(activity_1, activity.Activity)
    assert activity_1.name == 'workflow_sample_activity_1'


def test_find_activity_none(monkeypatch):
    """Test that looking up a non-existent activity in a flow returns None"""

    monkeypatch.setattr(activity.Activity, '__init__', lambda self: None)
    from tests.fixtures import flow_cli

    activity_1 = util_activity.find_activity(
        flow_cli, 'non_existent_activity')

    assert activity_1 is None


def test_find_activity_names(monkeypatch):
    """Test that we list the activities names associated with a flow"""

    monkeypatch.setattr(activity.Activity, '__init__', lambda self: None)
    from tests.fixtures import flow_cli

    activity_names = util_activity.find_activity_names(flow_cli)

    assert activity_names == [
        'workflow_sample_bootstrap', 'workflow_sample_bootstrap2',
        'workflow_sample_activity_1', 'workflow_sample_activity_2',
        'workflow_sample_activity_3']
