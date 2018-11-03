import os
import time
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from . import settings


bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    disk_space = get_disk_space()
    files = get_file_list()
    return render_template('index.html', disk_space=disk_space, files=files)


def get_disk_space():
    import subprocess
    _, total, used, avail, _, _ = subprocess.getoutput('df -h | grep /usr/src/app').split()
    return {'total': total, 'used': used, 'avail': avail}

def get_file_list():
    base_dir = settings.FILE_BASE_DIR
    names = [f for f in os.listdir(base_dir) if os.path.isfile(os.path.join(base_dir, f))]
    temp_names = filter(lambda f: f.endswith('.aria2'), names) # aria2 temp file
    file_names = filter(lambda f: not f.endswith('.aria2'), names)
    files = []

    for name in file_names:
        path = os.path.join(base_dir, name)
        stat = os.stat(path)
        # download isn't finished if the .aria2 temp file exists
        finished = not (name + '.aria2' in temp_names)
        files.append({
            'name': name,
            'size': convert_bytes(stat.st_size),
            'mtime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat.st_mtime)),
            'url': path,
            'finished': finished
        })

    return files

def convert_bytes(num):
    for unit in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, unit)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')


