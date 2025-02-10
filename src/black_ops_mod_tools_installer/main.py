import time

start_time = time.time()

from black_ops_mod_tools_installer import cli
from black_ops_mod_tools_installer.log import logger
from black_ops_mod_tools_installer.log_info import LOG_INFO
from black_ops_mod_tools_installer.file_io import SCRIPT_DIR
from black_ops_mod_tools_installer.customization import enable_vt100


def main():
    try:
        enable_vt100()
        logger.set_log_base_dir(SCRIPT_DIR)
        logger.configure_logging(LOG_INFO)
        cli.cli()
    except Exception as error_message:
        logger.log_message(str(error_message))
