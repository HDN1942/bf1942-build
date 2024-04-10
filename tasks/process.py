from invoke import task
import tasks.sound as sound
from .sync import sync_dirs

PROCESSOR_CHECKS = [
    sound.should_process
]

PROCESSORS = [
    sound.process
]

def should_process(target):
    for check in PROCESSOR_CHECKS:
        if check(target):
            return True

    return False

@task
def process_files(c):
    for target in [t for t in c.build.targets if not t.up_to_date and should_process(t)]:
        sync_dirs(target.work_path, target.process_path)

        for processor in PROCESSORS:
            processor(c, target)

        target.processed = True
