import socket
import fcntl
import struct
import datetime
import requests
from threading import Thread
from lxml import html

from .models import Video, FSConfig
from .utils import FSAPI

MY_ID = 'trees1411@yahoo.com'
MY_PWD = 'Tmrisdoomday!2'
global fs
fs = FSAPI(email=MY_ID, password=MY_PWD)


def is_file(url):
    try:
        data = url.split('/')

        if data[3] == 'file':
            return True
        else:
            return False
    except:
        return False


def is_folder(url):
    try:
        data = url.split('/')

        if data[3] == 'folder':
            return True
        else:
            return False
    except:
        return False


def humanbytes(B):
    'Return the given bytes as a human friendly KB, MB, GB, or TB string'
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2)  # 1,048,576
    GB = float(KB ** 3)  # 1,073,741,824
    TB = float(KB ** 4)  # 1,099,511,627,776

    if B < KB:
        return '{0} {1}'.format(B, 'Bytes' if 0 == B > 1 else 'Byte')
    elif KB <= B < MB:
        return '{0:.2f} KB'.format(B/KB)
    elif MB <= B < GB:
        return '{0:.2f} MB'.format(B/MB)
    elif GB <= B < TB:
        return '{0:.2f} GB'.format(B/GB)
    elif TB <= B:
        return '{0:.2f} TB'.format(B/TB)


def leak_video(url):
    fs.login()

    d = fs.get_file_info(url)

    video, created = Video.objects.get_or_create(file_code=d['linkcode'])

    if created:
        video.fs_url = url
        video.file_code = d['linkcode']
        video.file_name = d['name']
        video.file_url = fs.download(url)
        video.file_size = humanbytes(d['size'])
        video.file_type = d['mimetype']
    video.save()

    return video


def leak_folder(url):
    fs.login()

    resp = fs.get_folder_urls(url)

    print(resp)

    if len(resp) > 0:
        videos = []
        for d in resp:
            if d['mimetype'] != "text/plain":
                videos.append(leak_video(d['furl']))

    return videos
