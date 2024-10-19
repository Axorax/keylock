import os
import sys
import core
import threading
import tkinter as tk
from core import lock_keyboard, lock_mouse
from settings import open_config, save_config

config = open_config("keylock.config")
refresh_rate = 1500

if os.name == "nt":
    try:
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)
    except Exception as e:
        print(f"Could not set DPI awareness: {e}")


def load_asset(path):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    assets = os.path.join(base, "assets")
    return os.path.join(assets, path)


root = tk.Tk()
root.geometry("360x352")
root.configure(bg="#ffffff")
root.title("Keylock")
root.iconbitmap(load_asset("icon.ico"))

canvas = tk.Canvas(
    root,
    bg="#ffffff",
    width=360,
    height=352,
    bd=0,
    highlightthickness=0,
    relief="ridge",
)

canvas.place(x=0, y=0)

keyboard_locked_image = tk.PhotoImage(file=load_asset("keyboard_locked.png"))
keyboard_unlocked_image = tk.PhotoImage(file=load_asset("keyboard_unlocked.png"))
mouse_locked_image = tk.PhotoImage(file=load_asset("mouse_locked.png"))
mouse_unlocked_image = tk.PhotoImage(file=load_asset("mouse_unlocked.png"))

image_1 = keyboard_unlocked_image
image_1_ref = canvas.create_image(180, 17, image=image_1)

image_2 = mouse_unlocked_image
image_2_ref = canvas.create_image(180, 53, image=image_2)

image_3 = tk.PhotoImage(file=load_asset("layout.png"))
canvas.create_image(182, 184, image=image_3)


def update_keyboard():
    global image_1
    if core.keyboard_locked:
        image_1 = keyboard_locked_image
        canvas.itemconfig(image_1_ref, image=image_1)
    else:
        image_1 = keyboard_unlocked_image
        canvas.itemconfig(image_1_ref, image=image_1)


def update_mouse():
    global image_2
    if core.mouse_locked:
        image_2 = mouse_locked_image
        canvas.itemconfig(image_2_ref, image=image_2)
    else:
        image_2 = mouse_unlocked_image
        canvas.itemconfig(image_2_ref, image=image_2)


shortcut = tk.Entry(
    bd=0, bg="#f1f1f1", fg="#000000", insertbackground="#ffffff", highlightthickness=0
)

shortcut.place(x=199, y=304, width=135, height=26)

if config:
    if config.get("onstart_lock_keyboard", "").lower() == "true":
        lock_keyboard()
    if config.get("onstart_lock_mouse", "").lower() == "true":
        lock_mouse()
    if config.get("quit_after", "never").lower() != "never":
        root.after(int(config["quit_after"]), sys.exit)
    if config.get("refresh_rate", "1500").lower() != "1500":
        refresh_rate = int(config["refresh_rate"])
    shortcut.insert(0, config.get("unlock", "ctrl+q"))
else:
    shortcut.insert(0, "ctrl+q")

debounce_timer = None


def debounce():
    global debounce_timer
    if debounce_timer is not None:
        root.after_cancel(debounce_timer)
    debounce_timer = root.after(500, saving_thread)


def saving_thread():
    threading.Thread(target=lambda: save_config(shortcut.get()), daemon=True).start()


shortcut.bind("<KeyRelease>", lambda e: debounce())


def check_change():
    if core.changed:
        update_keyboard()
        update_mouse()
        core.changed = False
    root.after(refresh_rate, check_change)


threading.Thread(target=check_change, daemon=True).start()

button_1_image = tk.PhotoImage(file=load_asset("1.png"))
button_1 = tk.Button(
    image=button_1_image,
    relief="flat",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: (lock_keyboard(shortcut.get()), lock_mouse(shortcut.get())),
)
button_1.place(x=23, y=240, width=315, height=39)

button_2_image = tk.PhotoImage(file=load_asset("2.png"))
button_2 = tk.Button(
    image=button_2_image,
    relief="flat",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: (lock_keyboard(shortcut.get()), update_keyboard()),
)
button_2.place(x=24, y=176, width=144, height=39)

button_3_image = tk.PhotoImage(file=load_asset("3.png"))
button_3 = tk.Button(
    image=button_3_image,
    relief="flat",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: (lock_mouse(shortcut.get()), update_mouse()),
)
button_3.place(x=194, y=176, width=144, height=39)

root.resizable(False, False)
root.mainloop()
