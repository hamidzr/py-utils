import sys
import re
import subprocess
from typing import List

# decorator to handle ctrl+c in cli
def handle_ctrl_c(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print("\n\nExiting due to keyboard interrupt...")
            sys.exit(0)
    return wrapper

def fuzzy_match(query: str, string: str) -> bool:
    """fuzzy match query as regex to string
    parse and accept query as regex if it looks like it
    """
    if query.startswith("/") and query.endswith("/"):
        query = query[1:-1]
        return bool(re.search(query, string, re.IGNORECASE))
    return query in string

def interactive_pick_text(options: List[str]) -> str:
    """interactive pick from options"""
    print("Pick one of the following options:")
    for i, option in enumerate(options):
        print(f"{i+1}. {option}")
    while True:
        try:
            choice = int(input("Enter your choice: "))
            if choice < 1 or choice > len(options):
                raise ValueError
            return options[choice-1]
        except ValueError:
            print("Invalid choice, try again...")

def interactive_pick_dmenu(options: List[str]) -> str:
    out = subprocess.run(
        ["_themenu.sh", "-p", "Select SSID"],
        input="\n".join(options),
        capture_output=True,
        text=True,
    )
    return out.stdout.strip()
