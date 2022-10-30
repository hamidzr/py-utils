import subprocess
import typing as t
import threading


def exits_with(code: int, cmd: t.List[str]) -> bool:
    try:
        cp = subprocess.run(cmd, check=True)
        return cp.returncode == code
    except subprocess.CalledProcessError as e:
        return e.returncode == code


# debounce decorator with args and kwargs in miliseconds
def debounce(wait: int):
    def decorator(fn):
        def debounced(*args, **kwargs):
            def call_it():
                fn(*args, **kwargs)

            try:
                debounced.t.cancel()
            except AttributeError:
                pass
            debounced.t = threading.Timer(wait / 1000, call_it)
            debounced.t.start()

        return debounced

    return decorator


def wrap_arg_for_shell(text: str) -> str:
    """
    wrap text in quotes and escape quotes
    """
    # use .format
    # https://stackoverflow.com/questions/35817/how-to-escape-os-system-calls-in-python
    return "'{}'".format(text.replace("'", "'\\''"))


def to_shell_arg(args: list) -> str:
    return " ".join([wrap_arg_for_shell(arg) for arg in args])
