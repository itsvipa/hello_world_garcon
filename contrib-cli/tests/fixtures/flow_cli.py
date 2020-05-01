import logging
import random

from garcon import activity
from garcon import runner
from garcon import task
from garcon.param import StaticParam


logger = logging.getLogger(__name__)

domain = 'dev'
name = 'workflow_sample'
create = activity.create(domain, name)


def activity_failure(context, activity):
    num = int(random.random() * 4)
    logger.info('number {}'.format(num))
    if num != 3:
        logger.info('activity_3: fails')
        raise Exception('fails')

    logger.info('activity_3: end')


@task.decorate()
def bootstrap(activity, context_test):
    logger.info('bootstrap')
    logger.info('context_test: {}'.format(context_test))
    return {'new_context': "I'm the new context"}


bootstrap1 = create(
    name='bootstrap',
    tasks=runner.Sync(
        bootstrap.fill(context_test=StaticParam('hello boostrap'))))

bootstrap2 = create(
    name='bootstrap2',
    tasks=runner.Sync(
        bootstrap.fill(context_test='context_test')))

test_activity_1 = create(
    name='activity_1',
    requires=[bootstrap],
    run=runner.Async(
        lambda context, activity: logger.info('activity_2_task_1'),
        lambda context, activity: logger.info('activity_2_task_2')))

test_activity_2 = create(
    name='activity_2',
    retry=10,
    requires=[bootstrap],
    run=runner.Sync(activity_failure))

test_activity_3 = create(
    name='activity_3',
    requires=[test_activity_1, test_activity_2],
    run=runner.Sync(
        lambda context, activity: logger.info('activity_3')))
