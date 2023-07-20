import sys
# decorator to handle ctrl+c in cli
def handle_ctrl_c(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print("\n\nExiting due to keyboard interrupt...")
            sys.exit(0)
    return wrapper
