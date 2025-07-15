
from prefect import get_run_logger
from tiled.client import from_profile
from pathlib import Path

def create_folders(uid, beamline_acronym='opls'):
    logger = get_run_logger()
    tiled_client = from_profile("nsls2")
    run = tiled_client[beamline_acronym]["raw"][uid]
    logger.info(f"Creating project folders for {run.start['uid']} if not exist.")

    cycle_id, data_session = run.start['cycle'], run.start['data_session']
    if project_name := run.start.get('project_name'):
        dir_names = [
            "GISAXS_data",
            "GISAXS_analysis",
            "GID_data",
            "GID_analysis",
            "XRR_data",
            "XRR_analysis",
            "XRF_data",
            "XRF_analysis",
            "PseudoXRR",
            "PseudoXRR/gixos",
            "PseudoXRR/p100kA",
            "PseudoXRR/processed",
            "XRR_analysis/data",
            "XRR_analysis/data2",
            "XRR_analysis/data3",
            "XRR_analysis/q_plots",
            "XRR_analysis/checks_plots",
            "XRR_analysis/summaries",
            "Jupyter_notebooks",
            "GIWAXS_data",
            "GIWAXS_analysis",
            # "kibron"  # Uncomment if needed
            # "scan_plots"  # Uncomment if needed
        ]

        root_dir = Path(f"/nsls2/data/smi/proposals/{cycle_id}/{data_session}/projects/{project_name}")
        for dir_name in dir_names:
            (root_dir / dir_name).mkdir(parents=True, exist_ok=True)
        logger.info(f"Finished creating folders for project {project_name}")

    else:
        logger.warning("No project name found in run start data. Skipping folder creation.")
