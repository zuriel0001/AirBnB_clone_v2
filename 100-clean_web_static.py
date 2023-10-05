#!/usr/bin/python3
# A Fabfile to deleting out-of-date archives

import os
from fabric.api import *

env.hosts = ["34.207.189.180", "54.172.84.52"]


def do_clean(number=0):
    """Defined to Delete out-of-date archives.

    Args:
        number (int): The number of archives to be kept

    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the 2 most recent archives, and on and on.
    """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
