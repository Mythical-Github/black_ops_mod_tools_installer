import os
import textwrap
from datetime import datetime
from shutil import get_terminal_size

from black_ops_mod_tools_installer.console import console
from black_ops_mod_tools_installer.log_info import LOG_INFO


class Logger():
    def __init__(
        self
    ):
        super().__init__()
        self.log_base_dir = os.path.normpath(f'{os.getcwd()}/src')
        self.log_prefix = ''


    def set_log_base_dir(self, base_dir: str):
        self.log_base_dir = base_dir


    def rename_latest_log(self, log_dir):
        latest_log_path = os.path.join(log_dir, f'{self.log_prefix}latest.log')
        if os.path.isfile(latest_log_path):
            try:
                timestamp = datetime.now().strftime('%m_%d_%Y_%H%M_%S')
                new_name = f'{self.log_prefix}{timestamp}.log'
                new_log_path = os.path.join(log_dir, new_name)

                counter = 1
                while os.path.isfile(new_log_path):
                    new_name = f'{self.log_prefix}{timestamp}_({counter}).log'
                    new_log_path = os.path.join(log_dir, new_name)
                    counter += 1

                os.rename(latest_log_path, new_log_path)

            except PermissionError as e:
                self.log_message(f"Error renaming log file: {e}")
                return


    def configure_logging(self, colors_config):
        self.log_prefix = colors_config['log_name_prefix']

        log_dir = os.path.join(self.log_base_dir, 'logs')
        os.makedirs(log_dir, exist_ok=True)

        self.rename_latest_log(log_dir)


    def log_message(self, message: str):
        color_options = LOG_INFO.get('theme_colors', {})
        default_background_color = LOG_INFO.get('background_color')
        default_background_color = f"rgb({default_background_color[0]},{default_background_color[1]},{default_background_color[2]})"

        default_text_color = LOG_INFO.get('default_color')
        default_text_color = f"rgb({default_text_color[0]},{default_text_color[1]},{default_text_color[2]})"

        terminal_width = get_terminal_size().columns
        wrapped_message = textwrap.fill(message, width=terminal_width)

        for keyword, color in color_options.items():
            if keyword in message:
                rgb_color = f"rgb({color[0]},{color[1]},{color[2]})"
                console.print(wrapped_message, style=f'{rgb_color} on {default_background_color}')
                break
        else:
            console.print(wrapped_message, style=f'{default_text_color} on {default_background_color}')

        log_dir = os.path.join(self.log_base_dir, 'logs')
        log_path = os.path.join(log_dir, f'{self.log_prefix}latest.log')

        os.makedirs(log_dir, exist_ok=True)

        if not os.path.isfile(log_path):
            try:
                with open(log_path, 'w') as log_file:
                    log_file.write("")
            except OSError as e:
                error_color = LOG_INFO.get('error_color', (255, 0, 0))
                error_color = f"rgb({error_color[0]},{error_color[1]},{error_color[2]})"
                console.print(f"Failed to create log file: {e}", style=f'{error_color} on {default_background_color}')
                return

        try:
            with open(log_path, 'a') as log_file:
                log_file.write(f"{message}\n")
        except OSError as e:
            error_color = LOG_INFO.get('error_color', (255, 0, 0))
            error_color = f"rgb({error_color[0]},{error_color[1]},{error_color[2]})"
            console.print(f"Failed to write to log file: {e}", style=f'{error_color} on {default_background_color}')


logger = Logger()
