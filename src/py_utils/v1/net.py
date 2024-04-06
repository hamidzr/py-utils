import re
import subprocess
from typing import Optional


def get_first_hop_ip() -> Optional[str]:
    # run traceroute to a common address like google
    result = subprocess.run(
        ["traceroute", "-m", "1", "-w", "1", "8.8.8.8"],
        timeout=2,
        stdout=subprocess.PIPE,
        text=True,
        stderr=subprocess.DEVNULL,
    )

    # use regular expression to find IP addresses
    ips = re.findall(r"\d+\.\d+\.\d+\.\d+", result.stdout)

    # return the first IP address found, which is the first hop
    return ips[0] if ips else None


def ping_server(ip_address: str, timeout: int = 1) -> Optional[float]:
    """
    Ping a server and return the time in milliseconds.
    timeout: time to wait for a response in seconds
    """
    response = subprocess.Popen(
        ["ping", "-c", "1", "-t", str(timeout), ip_address], stdout=subprocess.PIPE
    )
    output = response.communicate()[0].decode("utf-8")

    try:
        ping_time = float(output.split("time=")[1].split(" ms")[0])
    except:
        ping_time = None

    return ping_time


def can_reach_internet() -> bool:
    return ping_server("8.8.8.8", timeout=1) is not None
