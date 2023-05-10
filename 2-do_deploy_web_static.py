#!/usr/bin/python3
# This Fabfile distributes an archive to a web server.
import os.path
from fabric.api import env, put, run

env.hosts = ["100.25.182.1", "54.157.172.8"]


def do_deploy(archive_path):
    """
    Distribute an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.

    Returns:
        True if successful, False otherwise.
    """
    if not os.path.isfile(archive_path):
        return False

    file_name = os.path.basename(archive_path)
    name = os.path.splitext(file_name)[0]

    if put(archive_path, "/tmp/{}".format(file_name)).failed:
        return False

    if run("rm -rf /data/web_static/releases/{}/".format(name)).failed:
        return False

    if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed:
        return False

    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file_name, name)).failed:
        return False

    if run("rm /tmp/{}".format(file_name)).failed:
        return False

    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed:
        return False

    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed:
        return False

    if run("rm -rf /data/web_static/current").failed:
        return False

    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed:
        return False

    return True
