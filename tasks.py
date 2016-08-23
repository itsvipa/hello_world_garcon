import datetime
import time

from garcon import task


@task.decorate(timeout=60)
def print_hello_task(activity, workflow_id, activity_name, task_name, sleep):
    """Say hello!

    Args:
        activity (ActivityWorker): Garcon ActivityWorker executing the task.
        workflow_id (str): SWF workflowid executing the task.
        activity_name (str): Name identifying the activity executing the task.
        task_name (str): Name identifying the task.
        sleep (str): Optional time in seconds to sleep before starting task.

    Returns:
        dict: Context with (str) timestamp of when the task completed.
    """

    if sleep:
        time.sleep(sleep)

    message = '{workflow_id}: I am {activity_name}, {task_name}'.format(
        workflow_id=workflow_id,
        activity_name=activity_name,
        task_name=task_name)
    print(message)

    return {'hello_completed': str(datetime.datetime.now())}
