import subprocess
import time

from py_utils.v1.bash import retry

def get_window_id(name: str, timeout=None) -> str:
    """
    get the window id of the first window with a given name.
    waits until the window is found.
    """
    def _get_window_id():
        return subprocess.check_output(["xdotool", "search", "--name", name]).decode("utf-8").strip()
    if timeout is None:
        return _get_window_id()
    else:
        return retry(_get_window_id, timeout=timeout)



def type_window(wid, text):
    # send keys to vim wid
    # subprocess.call(["xdotool", "windowactivate", wid])
    subprocess.call(["xdotool", "type", "--window", wid, text])

def key_window(wid, key):
    subprocess.call(["xdotool", "key", "--window", wid, key])

def execute_script(wid: str, script: str):
    """
    parse an input script into a series of type_window and key_window calls:
    t ihello
    k KP_Enter
    """
    script = script.strip()
    for line in script.splitlines():
        # line = line.strip()
        if line.startswith("t "):
            type_window(wid, line[2:])
        elif line.startswith("k "):
            key_window(wid, line[2:])
        else:
            raise ValueError("unknown command: " + line)
