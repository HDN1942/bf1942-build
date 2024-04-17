import logging
from invoke import task
import tasks.sound as sound
from .sync import sync_dirs

logger = logging.getLogger(__name__)

PROCESSOR_CHECKS = [
    sound.should_process
]

PROCESSORS = [
    sound.process
]

def should_process(target):
    for check in PROCESSOR_CHECKS:
        if check(target):
            logger.debug(f'{target} will be processed')
            return True

    logger.debug(f'{target} will not be processed')
    return False

@task
def process_files(c):
    if c.build.all_up_to_date:
        return

    for target in [t for t in c.build.targets if not t.up_to_date and should_process(t)]:
        logger.debug(f'{target} setup for process')
        target.setup_for_process()

        logger.debug(f'{target} start processing')

        for processor in PROCESSORS:
            processor(c, target)

        logger.debug(f'{target} end processing')

