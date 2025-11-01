import sys
import os
from datetime import datetime
from typing import Any

COLORS = {
    'info': '\033[94m',      # Blue
    'debug': '\033[90m',     # Gray
    'warning': '\033[93m',   # Yellow
    'error': '\033[91m',     # Red
}


def smart_log(*args: Any, **kwargs) -> None:
    level = kwargs.get('Level', 'info').lower()
    use_timestamp = kwargs.get('timestamp', False)
    use_colors = kwargs.get('color', True)
    save_file_path = kwargs.get('save_to', None)

    message_components = [str(arg) for arg in args]
    message_content = " ".join(message_components)

    timestamp_str = ""
    if use_timestamp:
        timestamp_str = datetime.now().strftime("%H:%M:%S")
        timestamp_str += " "

    level_str = f"[{level.upper()}] "

    prefix = f"{timestamp_str}{level_str}"

    base_message = f"{prefix}{message_content}"
    file_log_message = base_message.strip()

    if use_colors and level in COLORS:
        line_color = COLORS.get(level)

        output_log_message = f"{line_color}{base_message}"
    else:
        output_log_message = base_message

    print(output_log_message)

    if save_file_path:
        directory = os.path.dirname(save_file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        with open(save_file_path, 'a') as f:
            f.write(file_log_message + '\n')
