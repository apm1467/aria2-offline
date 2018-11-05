import os
from os.path import (isfile, join)
import time
import redis
from flask import (Blueprint, render_template, request, send_from_directory)
from . import settings

bp = Blueprint('index', __name__)
rds = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)


@bp.route('/', methods=('GET', 'POST'))
def index():
    err = ''
    if request.method == 'POST':
        file_name = request.form['file_name']
        if request.form['submit'] == 'Set New Name':
            new_name = request.form['new_name']
            if new_name:
                rds.set(file_name, new_name)
            else:
                err = 'File name can not be empty.'
        else:
            # request.form['submit'] == 'Delete File'
            delete_file(file_name)

    disk_space = get_disk_space()
    files = get_file_list()
    return render_template('index.html', err=err, disk_space=disk_space, files=files)

@bp.route(settings.FILE_DOWNLOAD_URL + '<filename>')
def download(filename):
    return send_from_directory(join(settings.FILE_BASE_DIR), filename)


def delete_file(file_name):
    rds.delete(file_name)
    os.remove(join(settings.FILE_BASE_DIR, file_name))
    try:
        os.remove(join(settings.FILE_BASE_DIR, file_name + '.aria2'))
    except FileNotFoundError:
        pass

def get_disk_space():
    import subprocess
    _, total, used, avail, _, _ = subprocess.getoutput('df -h | grep /etc/hosts').split()
    return {'total': total, 'used': used, 'avail': avail}

def get_file_list():
    base_dir = settings.FILE_BASE_DIR
    names = [f for f in os.listdir(base_dir) if isfile(join(base_dir, f))]
    temp_names = [f for f in names if f.endswith('.aria2')]  # aria2 temp file
    file_names = [f for f in names if not f.endswith('.aria2')]
    files = []

    for name in file_names:
        path = join(base_dir, name)
        stat = os.stat(path)
        display_name = get_file_display_name(name)
        # download isn't finished if the .aria2 temp file exists
        finished = not (name + '.aria2' in temp_names)
        # give 10 sec tolerance after file creation
        if time.time() - stat.st_ctime < 10:
            finished = False

        file_name = name
        if finished:
            file_name = rename_file(name)

        files.append({
            'name': file_name,
            'display_name': display_name,
            'size': convert_bytes(stat.st_size),
            'mtime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat.st_mtime)),
            'url': settings.FILE_DOWNLOAD_URL + file_name,
            'finished': finished
        })

    return files

def get_file_display_name(file_name):
    if rds.exists(file_name):
        return rds.get(file_name)
    return file_name

def rename_file(file_name):
    if rds.exists(file_name):
        new_name = rds.get(file_name)
        base_dir = settings.FILE_BASE_DIR
        os.rename(join(base_dir, file_name), join(base_dir, new_name))
        rds.delete(file_name)
        return new_name
    return file_name

def convert_bytes(num):
    for unit in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, unit)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')
