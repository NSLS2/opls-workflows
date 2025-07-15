from prefect import task, flow, get_run_logger
from prefect.task_runners import ConcurrentTaskRunner
from data_validation import data_validation
from project_folders import create_folders

@task
def log_completion():
    logger = get_run_logger()
    logger.info("Complete")

@flow(task_runner=ConcurrentTaskRunner())
def end_of_run_workflow(stop_doc):
    logger = get_run_logger()
    uid = stop_doc["run_start"]
    data_validation(uid)
    create_folders(uid)
    log_completion()

