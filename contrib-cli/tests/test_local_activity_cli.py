"""
Unit tests for the local activity cli script
"""


from unittest.mock import MagicMock, patch


from garcon.contrib import local_activity_cli
from garcon.contrib import util_activity


def test_list_activities(monkeypatch):
    """Test that we list the activities names associated with a flow"""

    monkeypatch.setattr(
        util_activity, 'find_activity_names', MagicMock(
            return_value=['a', 'b', 'c']))

    output = local_activity_cli.list_activities(MagicMock())
    expected_output = ('Activity names include:\n'
                       'a\n'
                       'b\n'
                       'c')

    assert output == expected_output


def test_run_activity_not_called(monkeypatch):
    """Tests that the run_activity method is not called when the activity name
    is not found in the flow
    """

    workflow_activity_mock = MagicMock(return_value=None)
    monkeypatch.setattr(util_activity, 'find_activity', workflow_activity_mock)
    local_activity_cli.run_activity(
        MagicMock(), '{"context": "test"}', 'activity_name')

    assert workflow_activity_mock.execute_activity.call_count == 0


def test_run_activity_called(monkeypatch):
    """Tests that the run_activity method is called when the activity name
    is found in the flow
    """

    workflow_activity_mock = MagicMock()
    workflow_activity_mock.execute_activity.return_value = '{"c": "t"}'

    monkeypatch.setattr(
        util_activity, 'find_activity', MagicMock(
            return_value=workflow_activity_mock))

    local_activity_cli.run_activity(
        MagicMock(), '{"context": "test"}', 'activity_name')

    assert workflow_activity_mock.execute_activity.call_count == 1


@patch('importlib.import_module')
def test_garcon_local_activity_list(mock, monkeypatch):
    """Test cli 'list' command works"""

    monkeypatch.setattr(local_activity_cli, 'list_activities', MagicMock())
    local_activity_cli.main('test_flow_module', 'list')
    assert local_activity_cli.list_activities.called


@patch('importlib.import_module')
def test_garcon_local_activity_run(mock, monkeypatch):
    """Test cli 'run' command works"""

    monkeypatch.setattr(local_activity_cli, 'run_activity', MagicMock())
    local_activity_cli.main('test_flow_module', 'run', 'activity')
    assert local_activity_cli.run_activity.called
