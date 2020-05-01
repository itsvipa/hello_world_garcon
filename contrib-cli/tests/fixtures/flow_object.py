import logging
import random

from garcon import activity
from garcon import runner
from garcon import task
from garcon.param import StaticParam


logger = logging.getLogger(__name__)


class FlowObject(object):
    def __init__(self):
        self.domain = 'dev'
        self.name = 'workflow_sample'
        self.create = activity.create(self.domain, self.name)

    def decider(self, schedule):
        pass

    @property
    def bootstrap_activity(self):
        return self.create(
            name='bootstrap',
            tasks=runner.Sync(
                bootstrap.fill(context_test=StaticParam('hello boostrap'))))

    @property
    def bootstrap2_activity(self):
        return self.create(
            name='bootstrap2',
            tasks=runner.Sync(bootstrap.fill(context_test='context_test')))

    @property
    def test_activity_1(self):
        return self.create(
            name='activity_1',
            run=runner.Async(
                lambda context, activity: logger.info('activity_2_task_1'),
                lambda context, activity: logger.info('activity_2_task_2')))

    @property
    def test_activity_2(self):
        return self.create(
            name='activity_2',
            retry=10,
            run=runner.Sync(activity_failure))

    @property
    def test_activity_3(self):
        return self.create(
            name='activity_3',
            run=runner.Sync(
                lambda context, activity: logger.info('activity_3')))


@task.decorate()
def bootstrap(activity, context_test):
    logger.info('bootstrap')
    logger.info('context_test: {}'.format(context_test))
    return {'new_context': "I'm the new context"}


def activity_failure(context, activity):
    num = int(random.random() * 4)
    logger.info('number {}'.format(num))
    if num != 3:
        logger.info('activity_3: fails')
        raise Exception('fails')
    logger.info('activity_3: end')
