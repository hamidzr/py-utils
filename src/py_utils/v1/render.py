import json
import re
import shutil
import subprocess
from typing import Any, Dict, Literal, Optional

SubVariables = (
    dict[str, "SubVariables"] | list["SubVariables"] | str | int | float | bool | None
)
Variables = dict[str, SubVariables]


def ensure_max_precision(num: float | int, precision: int = 1) -> int | float:
    """
    ensure digits have at most `precision` decimal places without trailing zeros
    """
    if isinstance(num, int):
        return num

    has_non_zero_decimal = re.search(r"\.0*[1-9]", str(num))
    if not has_non_zero_decimal:
        return int(num)

    num = round(num, precision)
    digits = f"{num:.{precision}f}"
    has_decimal = re.search(r"\.", digits)
    has_trailing_zeros = has_decimal and re.search(r"0+$", digits)
    if has_trailing_zeros:
        return int(num) if num.is_integer() else float(digits.rstrip("0"))
    return num


def human_readable_number(v: float | int) -> str | float | int:
    assert isinstance(v, (int, float))
    sign = "" if v >= 0 else "-"
    v = abs(v)
    digits: str | int | float = v
    if v > 3000:
        digits = str(ensure_max_precision(v / 1000, 1)) + "k"
    elif v > 100:
        digits = ensure_max_precision(v, 1)
    elif v < 1:
        digits = ensure_max_precision(v, 4)
    else:
        digits = ensure_max_precision(v, 1)

    if isinstance(digits, float) and digits.is_integer():
        digits = int(digits)

    if sign == "":
        return digits
    elif isinstance(digits, str):
        return sign + digits
    else:
        return -digits


def human_readable_dict(d: Variables) -> Variables:
    def format_value(v: SubVariables) -> SubVariables:
        if isinstance(v, (int, float)):
            return human_readable_number(v)
        elif isinstance(v, bool):
            return str(v)
        elif v is None:
            return "None"
        elif isinstance(v, dict):
            return human_readable_dict(v)
        elif isinstance(v, list):
            return [format_value(item) for item in v]
        else:  # for str and other types
            return str(v)

    return {k: format_value(v) for k, v in d.items()}


def pretty_json(d: Any) -> str:
    """
    pretty format the given data structure prepared for printing.
    """
    if isinstance(d, str):
        try:
            d = json.loads(d)
        except json.JSONDecodeError:
            pass
    if not isinstance(d, dict):
        return d
    if shutil.which("jq"):
        json_str = json.dumps(d)
        result = subprocess.run(
            ["jq", ".", "-C"], input=json_str, text=True, capture_output=True
        )
        return result.stdout
    else:
        return json.dumps(d, indent=4, sort_keys=True)


def explore_object(
    obj: object, path: str = "", depth: int = 0, visited: Optional[set] = None
) -> None:
    """recursively explore properties and methods of an object with depth limit and cycle detection"""
    if visited is None:
        visited = set()

    # avoid revisiting the same objects
    obj_id = id(obj)
    if obj_id in visited:
        return
    visited.add(obj_id)

    # print the current path except the initial call
    if path:
        print(path)

    # depth limit to avoid too deep recursion
    if depth > 10:
        return

    for attr in dir(obj):
        if attr.startswith("__"):
            continue  # skip dunder methods
        item = getattr(obj, attr)
        new_path = f"{path}/{attr}" if path else attr
        if callable(item) or not hasattr(item, "__dict__"):
            print(new_path)
        else:
            explore_object(item, new_path, depth + 1, visited)


ColorType = Literal["red", "green", "yellow", "blue", "magenta", "cyan", "white"]

colors: Dict[ColorType, str] = {
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
    "white": "\033[97m",
}


def print_colored(text: str, color: ColorType) -> None:
    # reset color to default
    reset = "\033[0m"
    # print colored text using imported colors
    print(f"{colors[color]}{text}{reset}")
