import time as ttime

from prefect import flow, task, get_run_logger
from tiled.client import from_profile

BEAMLINE_OR_ENDSTATION = "opls"


@task(retries=2, retry_delay_seconds=10)
def read_all_streams(uid, beamline_acronym=BEAMLINE_OR_ENDSTATION):
    logger = get_run_logger()
    tiled_client = from_profile("nsls2")
    run = tiled_client[beamline_acronym]["raw"][uid]
    logger.info(f"Validating uid {run.start['uid']}")
    start_time = ttime.monotonic()
    for stream in run:
        logger.info(f"{stream}:")
        stream_start_time = ttime.monotonic()
        stream_data = run[stream].read()
        stream_elapsed_time = ttime.monotonic() - stream_start_time
        logger.info(f"{stream} elapsed_time = {stream_elapsed_time}")
        logger.info(f"{stream} nbytes = {stream_data.nbytes:_}")
    elapsed_time = ttime.monotonic() - start_time
    logger.info(f"{elapsed_time = }")


@flow(log_prints=True)
def data_validation(uid):
    read_all_streams(uid, beamline_acronym=BEAMLINE_OR_ENDSTATION)
