import os
import threading

config_template = """
&unlock@!@ctrl+q                # Shortcut to unlock (Examples: ctrl+q, alt+s, shift+ctrl+q)
&onstart_lock_keyboard@!@false  # Lock keyboard on start (true or false)
&onstart_lock_mouse@!@false     # Lock mouse on start (true or false)
&refresh_rate@!@1500            # Check for lock every x milliseconds (integer only)
&quit_after@!@never             # Exit app after some time (never or number in milliseconds, examples: 1000, 5000, never)

# 🔴 The "Mouse lock" button is a bit buggy. When you lock only mouse, if exit shortcut has "ctrl" then you can only use a-z characters and nothing else. This is not an issue when you lock only keyboard or both.
"""


def parse(path):
    settings = {}
    with open(path, "r") as file:
        for line in file:
            line = line.split("#", 1)[0].strip()
            if line:
                key_value = line.split("@!@", 1)
                if len(key_value) == 2:
                    settings[key_value[0].lstrip("&")] = key_value[1]
    return settings


def open_config(file_name):
    def main():
        if os.path.exists(file_name):
            settings_dict = parse(file_name)
            return settings_dict
        return None

    thread = threading.Thread(target=main)
    thread.start()
    thread.join()
    return main()


def save_config(shortcut):
    config_path = "keylock.config"

    def main():
        if not os.path.exists(config_path):
            with open(config_path, "w") as file:
                file.write(config_template)

        with open(config_path, "r") as file:
            content = file.read().strip() or config_template

        lines = content.splitlines()
        updated_lines = []
        unlock_replaced = False

        for line in lines:
            if line.startswith("&unlock@!@"):
                updated_lines.append(f"&unlock@!@{shortcut}")
                unlock_replaced = True
            else:
                updated_lines.append(line)

        if not unlock_replaced:
            updated_lines.append(f"&unlock@!@{shortcut}")

        with open(config_path, "w") as file:
            file.write("\n".join(updated_lines))

    thread = threading.Thread(target=main)
    thread.start()
    thread.join()
