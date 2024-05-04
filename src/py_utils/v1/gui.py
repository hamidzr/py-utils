import os


def notify_desktop(title, message):
    os.system(f"notify-send '{title}' '{message}'")
