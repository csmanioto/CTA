from utils import init_logger
import config

logger = init_logger(__name__, testing_mode=config.DEBUG_MODE)

#from datetime import datetime
from pathlib import Path
from subprocess import run, PIPE
import shlex
import re


# import subprocess


def check_file_permission(file):
    my_file = Path(file)
    if not my_file.is_file():
        return None
    st = my_file.stat()
    oct_perm = oct(st.st_mode)[-4:]
    return oct_perm


def check_is_file_exist(file):
    my_file = Path(file)
    if not my_file.is_file():
        return False
    else:
        return True


def run_os_cmd(cmd, quiet=True):
    stderr = None
    stderr = None
    try:
        if not quiet:
            logger.info('command: {}'.format(cmd))

        # use shlex to keep quoted substrings
        result = run(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
        # result = run(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
        # result = subprocess.call(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()

        stdout = result.stdout.strip().decode()
        stderr = result.stderr.strip().decode()

        if stdout and not quiet:
            logger.debug(stdout)

        if stderr and not quiet:
            logger.warning(stderr)

        return result.stdout.strip()
    except Exception as e:
        error_msg = e
        if stderr:
            error_msg = "{} {}".format(e,stderr)
        logger.error("Error on execute command using OS. {}".format(error_msg))


def check_string_in_list(string, mylist):
    match = False
    for item in mylist:
        pattern = re.compile("{}".format(item), re.IGNORECASE)
        if pattern.match(string):
            match = True
    return match

def datetime_striso8601(date_time):
    # d = datetime.datetime.strptime("2017-10-13T10:53:53.000Z", "%Y-%m-%dT%H:%M:%S.000Z")
    # iso8601 = dt.strftime("%Y-%m-%dT%H:%M.000Z")
    iso8601 = date_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    return iso8601

def str_none_to_empty(string):
    if string is None:
        string = ""
    return string
