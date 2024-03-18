import subprocess
import re
from typing import Optional

def get_first_hop_ip() -> Optional[str]:
    # run traceroute to a common address like google
    result = subprocess.run(["traceroute", "-m", "1", "-w", "1","8.8.8.8"], timeout=2,
                            stdout=subprocess.PIPE, text=True, stderr=subprocess.DEVNULL)

    # use regular expression to find IP addresses
    ips = re.findall(r'\d+\.\d+\.\d+\.\d+', result.stdout)

    # return the first IP address found, which is the first hop
    return ips[0] if ips else None
