#!/usr/bin/python3
"""
Script to deploy compressed file to web server
"""
from fabric.api import task, local, env, put, run
from datetime import datetime
import os

env.hosts = ["34.207.189.180", "54.172.84.52"]
# env.user = 'ubuntu'
# env.key_filename = '~/.ssh/school'


@task
def do_pack():
    """
    Create a compressed archive of the web_static directory.
        sudo fab -f 1-pack_web_static.py do_pack

    Returns:
            str: The path to the created archive file if successful
            otherwise None
    """
    formatted_dt = datetime.now().strftime('%Y%m%d%H%M%S')
    mkdir = "mkdir -p versions"
    path = "versions/web_static_{}.tgz".format(formatted_dt)
    print("Packing web_static to {}".format(path))

    if local("{} && tar -cvzf {} web_static".format(mkdir, path)).succeeded:
        return path
    return None


@task
def do_deploy(archive_path):
    """
    Deploy a compressed archive of the web_static directory to the web server

    Args:
       archive_path (str): The path to the archive file to be deployed.

    Returns:
      bool: True if the deployment is successful, False otherwise.
    """
    try:
        if not os.path.exists(archive_path):
            return False
        fn_with_ext = os.path.basename(archive_path)
        fn_no_ext, ext = os.path.splitext(fn_with_ext)
        dpath = "/data/web_static/releases/"
        put(archive_path, "/tmp/")
        run("rm -rf {}{}/".format(dpath, fn_no_ext))
        run("mkdir -p {}{}/".format(dpath, fn_no_ext))
        run("tar -xzf /tmp/{} -C {}{}/".format(fn_with_ext, dpath, fn_no_ext))
        run("rm /tmp/{}".format(fn_with_ext))
        run("mv {0}{1}/web_static/* {0}{1}/".format(dpath, fn_no_ext))
        run("rm -rf {}{}/web_static".format(dpath, fn_no_ext))
        run("rm -rf /data/web_static/current")
        run("ln -s {}{}/ /data/web_static/current".format(dpath, fn_no_ext))
        print("New version deployed!")
        return True

    except Exception:
        return False
