#!/usr/bin/python3
# This Fabfile generates a .tgz archive from the contents of web_static.
import os.path
from datetime import datetime
from fabric.api import local


def do_pack():
    """
    Compress the web_static directory into a tar gzipped archive.
    """
    current_time = datetime.utcnow()
    file_name = "web_static_{}{}{}{}{}{}.tgz".format(current_time.year,
                                                     current_time.month,
                                                     current_time.day,
                                                     current_time.hour,
                                                     current_time.minute,
                                                     current_time.second)
    if not os.path.isdir("versions"):
        if local("mkdir -p versions").failed:
            return None
    if local("tar -czvf versions/{} web_static".format(file_name)).failed:
        return None
    return "versions/{}".format(file_name)
