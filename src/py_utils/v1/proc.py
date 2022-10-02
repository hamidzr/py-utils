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
