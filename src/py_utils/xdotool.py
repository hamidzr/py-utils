import subprocess

def get_window_id(name: str) -> str:
    # pid not alway present
    vim_wid = subprocess.check_output(["xdotool", "search", "--name", name]).decode().strip()
    return vim_wid

def type_window(wid, text):
    # send keys to vim wid
    # subprocess.call(["xdotool", "windowactivate", wid])
    print("typing: " + text)
    subprocess.call(["xdotool", "type", "--window", wid, text])

def key_window(wid, key):
    print("key: " + key)
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
