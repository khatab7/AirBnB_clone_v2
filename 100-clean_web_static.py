#!/usr/bin/python3

from fabric.operations import local
from fabric.operations import put
from fabric.operations import run
from fabric.api import env
from fabric.api import hosts
from fabric.api import runs_once
import fabric
from datetime import datetime
import os


@runs_once
def do_pack():
    """Pack web_static folder for future deployment"""
    filename = "versions/web_static_{}.tgz".format(
        datetime.now().strftime("%Y%m%d%H%M%S"))
    local("mkdir -p versions")
    result = local("tar -czvf {} web_static".format(filename))
    if result.failed is True:
        return None
    else:
        return filename


env.hosts = ['54.167.41.249', '54.160.234.222']


def do_deploy(archive_path):
    """Deploy given archive to web server"""
    if os.path.exists(archive_path) is False:
        return False
    filename = os.path.basename(archive_path)
    result = put(archive_path, '/tmp/{}'.format(filename))
    if result.failed is True:
        return False
    result = run("mkdir -p /data/web_static/releases/{}/"
                 .format(filename[:-4]))
    if result.failed is True:
        return False
    result = run(("tar -xzf /tmp/" +
                  "{} -C /data/web_static/releases/{}/" +
                  " --strip-components=1").format(filename, filename[:-4]))
    if result.failed is True:
        return False
    result = run("rm /tmp/{}".format(filename))
    if result.failed is True:
        return False
    result = run("rm -rf /data/web_static/current")
    if result.failed is True:
        return False
    result = run("ln -s /data/web_static/releases/"
                 "{}/ /data/web_static/current".format(filename[:-4]))
    if result.failed is True:
        return False
    print("New version deployed!")
    return True


def deploy():
    """Pack web_static and deploy it"""
    filename = do_pack()
    if filename is None:
        return False
    return do_deploy(filename)


def do_clean(number=0):
    """Clean files from current repo and servers"""
    n = int(number)
    if n == 0:
        n = 1
    files = local("ls -1t versions", capture=True)
    files_list = files.stdout.splitlines()[n:]
    for elem in files_list:
        local("rm -rf versions/{}".format(elem))
    files = run("ls -1t /data/web_static/releases")
    files_list = files.splitlines()[n:]
    for elem in files_list:
        filepath = elem
        run("rm -rf /data/web_static/releases/{}".format(filepath))
