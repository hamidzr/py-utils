import subprocess
import pathlib
import typing as t

# print colored text
def print_colored(skk): print("\033[93m {}\033[00m" .format(skk))

Number = t.Union[int, float]


def run(command, cwd: t.Optional[pathlib.Path] = None):
    msg = command
    if cwd is not None:
        msg = f'{command} [cwd: {cwd}]'
    print_colored(msg)
    subprocess.run(command, cwd=cwd, check=True, shell=True)


def has_output(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
    return len(result.stdout) > 0


def fails(command):
    try:
        subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        return True
    return False

# read command output
def get_output(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')


# get current git hash
def get_current_hash():
    return get_output('git rev-parse HEAD')


def print_array(arr: t.Union[t.List[int], t.List[float]]):
    """
    print an array of numbers and print index indicators that line up
    """
    out = [' '.join([str(i) for i in range(len(arr))])]
    out += [' '.join([str(i) for i in arr])]
    return '\n'+'\n'.join(out)+'\n'


LINUX_DATE_FMT = '%a %b %d %H:%M:%S PDT %Y'
