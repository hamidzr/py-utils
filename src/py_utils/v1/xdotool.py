import logging
import subprocess

from py_utils.v1.bash import retry
from py_utils.v1.config import config
from py_utils.v1.proc import wrap_arg_for_shell

logger = logging.getLogger(__name__)


def get_window_id(name: str, timeout=None) -> str:
    """
    get the window id of the first window with a given name.
    waits until the window is found.
    """
    assert isinstance(name, str)

    def _get_window_id():
        return (
            subprocess.check_output(["xdotool", "search", "--name", name])
            .decode("utf-8")
            .strip()
        )

    if timeout is None:
        return _get_window_id()
    else:
        return retry(_get_window_id, timeout=timeout)


def window_name_exists(name: str) -> bool:
    try:
        get_window_id(name, timeout=None)
    except subprocess.CalledProcessError:
        return False
    return True


def window_exists(wid: str) -> bool:
    try:
        subprocess.check_output(["xdotool", "getwindowname", wid])
    except subprocess.CalledProcessError:
        return False
    return True


# different layout workaround
# reset to XTEST keyboard https://github.com/jordansissel/xdotool/issues/150#issuecomment-966198633
# LAYOUT_PREFIX = ["xdotool", "key", "--clearmodifiers", "shift", "&&"]
# https://github.com/jordansissel/xdotool/issues/43


def type_window(wid, text):
    logger.debug(f"typing {text} wid={wid}")
    cmd = ["xdotool", "type", "--clearmodifiers", "--window", wid, text]
    subprocess.call(cmd)


def key_window(wid, key):
    logger.debug(f"pressing {key} wid={wid}")
    cmd = ["xdotool", "key", "--clearmodifiers", "--window", wid, key]
    subprocess.call(cmd)


def execute_script(wid: str, script: str):
    """
    parse an input script into a series of type_window and key_window calls:
    t ihello
    k KP_Enter
    """
    script = script.strip()
    for line in script.splitlines():
        line = line.lstrip()
        if line.startswith("t "):
            type_window(wid, line[2:])
        elif line.startswith("k "):
            key_window(wid, line[2:])
        else:
            raise ValueError("unknown command: " + line)


if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=config.log_level)

    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    args = parser.parse_args()

    wid = get_window_id(args.name)
    key_window(wid, "Escape")
    execute_script(
        wid,
        """
k Escape
                   """,
    )
