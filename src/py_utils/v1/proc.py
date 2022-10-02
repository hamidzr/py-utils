import subprocess
import typing as t


def exits_with(code: int, cmd: t.List[str]) -> bool:
    try:
        cp = subprocess.run(cmd, check=True)
        return cp.returncode == code
    except subprocess.CalledProcessError as e:
        return e.returncode == code
