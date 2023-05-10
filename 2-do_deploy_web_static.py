#!/usr/bin/env python3
"""Compress web static package and deploy it to servers"""
from datetime import datetime
from os import path
from fabric.api import env, put, run

env.hosts = ['54.157.172.8', '100.25.182.1']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'

def do_deploy(archive_path):
    """Deploy web files to server"""
    try:
        if not path.exists(archive_path):
            return False

        # Upload archive
        put(archive_path, '/tmp/')

        # Create target directory
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        run('sudo mkdir -p /data/web_static/releases/web_static_{}/'.format(timestamp))

        # Uncompress archive and delete .tgz
        run('sudo tar -xzf /tmp/{} -C /data/web_static/releases/web_static_{}/'.format(path.basename(archive_path), timestamp))

        # Remove archive
        run('sudo rm /tmp/{}'.format(path.basename(archive_path)))

        # Move contents into host web_static
        run('sudo mv /data/web_static/releases/web_static_{}/web_static/* /data/web_static/releases/web_static_{}/'.format(timestamp, timestamp))

        # Remove extraneous web_static directory
        run('sudo rm -rf /data/web_static/releases/web_static_{}/web_static'.format(timestamp))

        # Delete pre-existing symbolic link
        run('sudo rm -rf /data/web_static/current')

        # Re-establish symbolic link
        run('sudo ln -s /data/web_static/releases/web_static_{}/ /data/web_static/current'.format(timestamp))

    except Exception as e:
        print("Exception: {}".format(str(e)))
        return False

    # Return True on success
    return True
