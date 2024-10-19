import pynput
from pynput.keyboard import Key, KeyCode

keyboard_listener = None
mouse_listener = None
shortcut_listener = None
pressed_keys = set()
shortcut_keys = []
keyboard_locked = False
mouse_locked = False
changed = False


def parse_shortcut(shortcut_str):
    if shortcut_str is None:
        shortcut_str = "ctrl+q"
    return [
        (
            pynput.keyboard.Key.ctrl_l
            if k == "ctrl"
            else (
                pynput.keyboard.Key.shift
                if k == "shift"
                else (
                    pynput.keyboard.Key.alt_l
                    if k == "alt"
                    else pynput.keyboard.KeyCode.from_char(k)
                )
            )
        )
        for k in shortcut_str.lower().split("+")
    ]


def stop_keyboard():
    global keyboard_listener, keyboard_locked
    if keyboard_listener:
        keyboard_listener.stop()
        keyboard_listener = None
    keyboard_locked = False
    print("Keyboard unlocked.")


def start_keyboard():
    global keyboard_listener, keyboard_locked
    keyboard_listener = pynput.keyboard.Listener(suppress=True)
    keyboard_listener.start()
    keyboard_locked = True
    print("Keyboard locked.")


def stop_mouse():
    global mouse_listener, mouse_locked
    if mouse_listener:
        mouse_listener.stop()
        mouse_listener = None
    mouse_locked = False
    print("Mouse unlocked.")


def start_mouse():
    global mouse_listener, mouse_locked
    mouse_listener = pynput.mouse.Listener(suppress=True)
    mouse_listener.start()
    mouse_locked = True
    print("Mouse locked.")


def start_shortcut_listener(shortcut):
    global shortcut_listener, shortcut_keys
    if not shortcut_listener:
        shortcut_keys = parse_shortcut(shortcut)
        shortcut_listener = pynput.keyboard.Listener(
            on_press=on_press, on_release=on_release
        )
        shortcut_listener.start()
        print(f"Shortcut listener started for: {shortcut}")


def stop_shortcut_listener():
    global shortcut_listener
    if shortcut_listener:
        shortcut_listener.stop()
        shortcut_listener = None
        print("Shortcut listener stopped.")


def lock_keyboard(shortcut="ctrl+q"):
    global keyboard_locked
    if keyboard_locked:
        stop_keyboard()
    else:
        start_keyboard()
    start_shortcut_listener(shortcut)


def lock_mouse(shortcut="ctrl+q"):
    global mouse_locked
    if mouse_locked:
        stop_mouse()
    else:
        start_mouse()
    start_shortcut_listener(shortcut)


VK_MAP = {
    48: "0",
    49: "1",
    50: "2",
    51: "3",
    52: "4",
    53: "5",
    54: "6",
    55: "7",
    56: "8",
    57: "9",
}

CONTROL_CHAR_MAP = {
    "\x01": "a",
    "\x02": "b",
    "\x03": "c",
    "\x04": "d",
    "\x05": "e",
    "\x06": "f",
    "\x07": "g",
    "\x08": "h",
    "\x09": "i",
    "\x0a": "j",
    "\x0b": "k",
    "\x0c": "l",
    "\x0d": "m",
    "\x0e": "n",
    "\x0f": "o",
    "\x10": "p",
    "\x11": "q",
    "\x12": "r",
    "\x13": "s",
    "\x14": "t",
    "\x15": "u",
    "\x16": "v",
    "\x17": "w",
    "\x18": "x",
    "\x19": "y",
    "\x1a": "z",
}


def string_to_key(string):
    if string is None:
        return None
    if isinstance(string, str) and string.startswith("Key."):
        special_key_name = string[4:]
        try:
            return getattr(Key, special_key_name)
        except AttributeError:
            return None
    elif len(string) == 1:
        return KeyCode.from_char(string)
    else:
        return None


def on_press(key):
    global pressed_keys
    global changed

    readable_key = None

    if hasattr(key, "char"):
        readable_key = key.char
    elif isinstance(key, Key):
        readable_key = str(key)

    if readable_key in CONTROL_CHAR_MAP:
        readable_key = CONTROL_CHAR_MAP[readable_key]

    key_object = string_to_key(readable_key)
    if key_object is not None:
        pressed_keys.add(key_object)

    print(f"Pressed key: {key}, Readable key: {readable_key}")

    if all(
        (k in pressed_keys)
        or (isinstance(k, str) and k.startswith("\\x") and ord(k) in pressed_keys)
        for k in shortcut_keys
    ):
        print("Shortcut pressed, unlocking all...")
        stop_keyboard()
        stop_mouse()
        stop_shortcut_listener()
        pressed_keys = set()
        changed = True


def on_release(key):
    global pressed_keys
    if key in pressed_keys:
        pressed_keys.remove(key)
