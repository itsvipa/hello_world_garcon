import os
import traceback
import sys

from garcon import activity
from garcon import runner
from garcon import param

import tasks


HELLO_WORLD_USER = 'HELLO_WORLD_USER'


class HelloWorldFlow(object):
    def __init__(self, domain, version):
        """Create a WorkFlow flow.

        Args:
            domain (str): domain workflow runs under.
            version (str): version of the workflow (ex 1.0).
        """

        if not os.environ.get(HELLO_WORLD_USER):
            print('Please set your {} environment variable'.format(
                HELLO_WORLD_USER))
            sys.exit(1)

        # Name of the SWF WorkFlow
        self.name = 'HelloWorld{}'.format(os.environ.get(HELLO_WORLD_USER))
        self.domain = domain
        self.version = version

        self.create = activity.create(
            self.domain, self.name, version=self.version,
            on_exception=self.on_exception)

    def decider(self, schedule, context):
        """Flow decider.

        Arg:
            schedule (callable): Call the scheduler.
        """

        print('Making decision with initial context: {}'.format(context))
        activity_one = schedule(
            'hello_world_one', self.hello_world_one_activity)

        activity_two = schedule(
            'hello_world_two',
            self.hello_world_two_activity,
            requires=[activity_one])

        activity_three = schedule(
            'hello_world_three',
            self.hello_world_three_activity,
            requires=[activity_two])
        activity_four = schedule(
            'hello_world_four',
            self.hello_world_four_activity,
            requires=[activity_two])

        schedule(
            'hello_world_five',
            self.hello_world_five_activity,
            requires=[activity_three, activity_four])

    def on_exception(self, actor, exception):
        """Capture an exception that has occurred in the application.

        Without this method exceptions would silently fail in Garcon flows.

        For Worker see:
                https://github.com/xethorn/garcon/blob/bee6bd5d5afbf2d77581d235ee1d4daa88301f42/garcon/activity.py#L274-L275
        For Decider seer
                https://github.com/xethorn/garcon/blob/967db94c2c7f759b98e9a58f276628ea773d9b84/garcon/decider.py#L138-L139
                https://github.com/xethorn/garcon/blob/967db94c2c7f759b98e9a58f276628ea773d9b84/garcon/decider.py#L178-L179

        Args:
            actor (ActivityWorker, DeciderWorker): the actor that has received
                the exception.
            exception (Exception): the exception to capture.
        """

        traceback.print_exc()

    @property
    def hello_world_one_activity(self):
        return self.create(
            name='hello_world_one',
            tasks=runner.Sync(
                tasks.print_hello_task.fill(
                    namespace='activity_one_task_one',
                    workflow_id='execution.workflow_id',
                    activity_name=param.StaticParam('Activity 1'),
                    task_name=param.StaticParam('Task 1'))))

    @property
    def hello_world_two_activity(self):
        return self.create(
            name='hello_world_two',
            tasks=runner.Sync(
                tasks.print_hello_task.fill(
                    namespace='activity_two_task_one',
                    workflow_id='execution.workflow_id',
                    activity_name=param.StaticParam('Activity 2'),
                    task_name=param.StaticParam('Task 1')),
                tasks.print_hello_task.fill(
                    namespace='activity_two_task_two',
                    workflow_id='execution.workflow_id',
                    activity_name=param.StaticParam('Activity 2'),
                    task_name=param.StaticParam('Task 2'))))

    @property
    def hello_world_three_activity(self):
        return self.create(
            name='hello_world_three',
            tasks=runner.Sync(
                tasks.print_hello_task.fill(
                    namespace='activity_three_task_one',
                    workflow_id='execution.workflow_id',
                    activity_name=param.StaticParam('Activity 3'),
                    task_name=param.StaticParam('Task 1'))))

    @property
    def hello_world_four_activity(self):
        return self.create(
            name='hello_world_four',
            tasks=runner.Sync(
                tasks.print_hello_task.fill(
                    namespace='activity_four_task_one',
                    workflow_id='execution.workflow_id',
                    activity_name=param.StaticParam('Activity 4'),
                    task_name=param.StaticParam('Task 1'))))

    @property
    def hello_world_five_activity(self):
        return self.create(
            name='hello_world_five',
            tasks=runner.Async(
                tasks.print_hello_task.fill(
                    namespace='activity_five_task_one',
                    workflow_id='execution.workflow_id',
                    sleep=param.StaticParam(10),
                    activity_name=param.StaticParam('Activity 5'),
                    task_name=param.StaticParam('Task 1')),
                tasks.print_hello_task.fill(
                    namespace='activity_five_task_two',
                    workflow_id='execution.workflow_id',
                    activity_name=param.StaticParam('Activity 5'),
                    task_name=param.StaticParam('Task 2'))))
