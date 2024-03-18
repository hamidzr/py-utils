import json
import re
from typing import Any

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
    return json.dumps(d, indent=4, sort_keys=True)
