import os
import traceback
import sys

from garcon import activity
from garcon import runner
from garcon import param

import tasks


HELLO_WORLD_USER = 'HELLO_WORLD_USER'


class Flow(object):
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
        self.domain = 'dev'
        self.version = '1.0'

        self.create = activity.create(
            self.domain, self.name, version=self.version,
            on_exception=self.on_exception)

    def decider(self, schedule, context):
        """Flow decider.

        Arg:
            schedule (callable): Call the scheduler.
        """

        print('Making decision with initial context: {}'.format(context))
        activity_1 = schedule(
            'hello_world_1', self.hello_world_1_activity)

        activity_2 = schedule(
            'hello_world_2',
            self.hello_world_2_activity,
            requires=[activity_1])

        activity_3 = schedule(
            'hello_world_3',
            self.hello_world_3_activity,
            requires=[activity_2])

        activity_4 = schedule(
            'hello_world_4',
            self.hello_world_4_activity,
            requires=[activity_2])

        activity_5 = schedule(
            'hello_world_5',
            self.hello_world_5_activity,
            requires=[activity_2])

        activity_6 = schedule(
            'hello_world_6',
            self.hello_world_6_activity,
            requires=[activity_4, activity_5])

        activity_7 = schedule(
            'hello_world_7',
            self.hello_world_7_activity,
            requires=[activity_3, activity_4])

        activity_8 = schedule(
            'hello_world_8',
            self.hello_world_8_activity,
            requires=[activity_3])

        activity_9 = schedule(
            'hello_world_9',
            self.hello_world_9_activity,
            requires=[activity_5])

        activity_10 = schedule(
            'hello_world_10',
            self.hello_world_10_activity,
            requires=[activity_7, activity_8])

        activity_11 = schedule(
            'hello_world_11',
            self.hello_world_11_activity,
            requires=[activity_6, activity_8])

        schedule(
            'hello_world_12',
            self.hello_world_12_activity,
            requires=[activity_9, activity_10, activity_11])

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
    def hello_world_1_activity(self):
        return self.create(
            name='hello_world_1',
            tasks=runner.Sync(
                tasks.print_hello_task.fill(
                    namespace='activity_1_task_1',
                    workflow_id='execution.workflow_id',
                    activity_name=param.StaticParam('Activity 1'),
                    task_name=param.StaticParam('Task 1'))),
            retry=5)

    @property
    def hello_world_2_activity(self):
        return self.create(
            name='hello_world_2',
            tasks=runner.Sync(
                tasks.print_hello_task.fill(
                    namespace='activity_2_task_1',
                    workflow_id='execution.workflow_id',
                    activity_name=param.StaticParam('Activity 2'),
                    task_name=param.StaticParam('Task 1')),
                tasks.print_hello_task.fill(
                    namespace='activity_2_task_2',
                    workflow_id='execution.workflow_id',
                    activity_name=param.StaticParam('Activity 2'),
                    task_name=param.StaticParam('Task 2'))),
            retry=5)

    @property
    def hello_world_3_activity(self):
        return self.create(
            name='hello_world_3',
            tasks=runner.Sync(
                tasks.print_hello_task.fill(
                    namespace='activity_3_task_1',
                    workflow_id='execution.workflow_id',
                    activity_name=param.StaticParam('Activity 3'),
                    task_name=param.StaticParam('Task 1'))),
            retry=5)

    @property
    def hello_world_4_activity(self):
        return self.create(
            name='hello_world_4',
            tasks=runner.Sync(
                tasks.print_hello_task.fill(
                    namespace='activity_4_task_1',
                    workflow_id='execution.workflow_id',
                    activity_name=param.StaticParam('Activity 4'),
                    task_name=param.StaticParam('Task 1'))),
            retry=5)

    @property
    def hello_world_5_activity(self):
        return self.create(
            name='hello_world_5',
            tasks=runner.Async(
                tasks.print_hello_task.fill(
                    namespace='activity_5_task_1',
                    workflow_id='execution.workflow_id',
                    sleep=param.StaticParam(10),
                    activity_name=param.StaticParam('Activity 5'),
                    task_name=param.StaticParam('Task 1')),
                tasks.print_hello_task.fill(
                    namespace='activity_5_task_2',
                    workflow_id='execution.workflow_id',
                    activity_name=param.StaticParam('Activity 5'),
                    task_name=param.StaticParam('Task 2'))),
            retry=5)

    @property
    def hello_world_6_activity(self):
        return self.create(
            name='hello_world_6',
            tasks=runner.Sync(
                tasks.print_hello_task.fill(
                    namespace='activity_6_task_1',
                    workflow_id='execution.workflow_id',
                    activity_name=param.StaticParam('Activity 6'),
                    task_name=param.StaticParam('Task 1'))),
            retry=5)

    @property
    def hello_world_7_activity(self):
        return self.create(
            name='hello_world_7',
            tasks=runner.Sync(
                tasks.print_hello_task.fill(
                    namespace='activity_7_task_1',
                    workflow_id='execution.workflow_id',
                    activity_name=param.StaticParam('Activity 7'),
                    task_name=param.StaticParam('Task 1')),
                tasks.print_hello_task.fill(
                    namespace='activity_7_task_2',
                    workflow_id='execution.workflow_id',
                    activity_name=param.StaticParam('Activity 7'),
                    task_name=param.StaticParam('Task 2'))),
            retry=5)

    @property
    def hello_world_8_activity(self):
        return self.create(
            name='hello_world_8',
            tasks=runner.Sync(
                tasks.print_hello_task.fill(
                    namespace='activity_8_task_1',
                    workflow_id='execution.workflow_id',
                    activity_name=param.StaticParam('Activity 8'),
                    task_name=param.StaticParam('Task 1'))),
            retry=5)

    @property
    def hello_world_9_activity(self):
        return self.create(
            name='hello_world_9',
            tasks=runner.Sync(
                tasks.print_hello_task.fill(
                    namespace='activity_9_task_1',
                    workflow_id='execution.workflow_id',
                    activity_name=param.StaticParam('Activity 9'),
                    task_name=param.StaticParam('Task 1'))),
            retry=5)

    @property
    def hello_world_10_activity(self):
        return self.create(
            name='hello_world_10',
            tasks=runner.Async(
                tasks.print_hello_task.fill(
                    namespace='activity_10_task_1',
                    workflow_id='execution.workflow_id',
                    sleep=param.StaticParam(10),
                    activity_name=param.StaticParam('Activity 10'),
                    task_name=param.StaticParam('Task 1')),
                tasks.print_hello_task.fill(
                    namespace='activity_10_task_2',
                    workflow_id='execution.workflow_id',
                    activity_name=param.StaticParam('Activity 10'),
                    task_name=param.StaticParam('Task 2'))),
            retry=5)

    @property
    def hello_world_11_activity(self):
        return self.create(
            name='hello_world_11',
            tasks=runner.Sync(
                tasks.print_hello_task.fill(
                    namespace='activity_11_task_1',
                    workflow_id='execution.workflow_id',
                    activity_name=param.StaticParam('Activity 11'),
                    task_name=param.StaticParam('Task 1'))),
            retry=5)

    @property
    def hello_world_12_activity(self):
        return self.create(
            name='hello_world_12',
            tasks=runner.Async(
                tasks.print_hello_task.fill(
                    namespace='activity_12_task_1',
                    workflow_id='execution.workflow_id',
                    sleep=param.StaticParam(10),
                    activity_name=param.StaticParam('Activity 12'),
                    task_name=param.StaticParam('Task 1')),
                tasks.print_hello_task.fill(
                    namespace='activity_12_task_2',
                    workflow_id='execution.workflow_id',
                    activity_name=param.StaticParam('Activity 12'),
                    task_name=param.StaticParam('Task 2'))),
            retry=5)
