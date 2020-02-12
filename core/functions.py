import socket
import fcntl
import struct
import datetime
import requests
from threading import Thread
from lxml import html

from .models import Video, VideoFolder


def is_file(url):
    data = url.split('/')

    if data[3] == 'file':
        return True
    else:
        return False


def get_media_id(url):
    if url.split('/')[-1] == '':
        return url.split('/')[-2]
    else:
        return url.split('/')[-1]


def get_full_url(code):
    return 'https://www.fshare.vn/file/' + code


def is_exist_in_system(url):
    if len(VideoFolder.objects.filter(fs_url=url)) > 0 or len(Video.objects.filter(fs_url=url)) > 0:
        return True
    else:
        return False


def get_file_extension(file_path):
    try:
        return file_path[-3:].lower()
    except Exception as e:
        print 'get_file_extension', e


def check_url_media_file_valid(url_file):
    r = requests.head(str(url_file))
    if r.status_code != 200:
        return False, r.status_code
    return True, r.status_code


def extract_extension_file(account, url):
    try:
        ext = account.get_media_link(get_media_id(url))[-3:]
        return True, ext
    except Exception as e:
        print 'extract_extension_file', e
        return False, None


def save_extracted_link_folder(account, folder_url):
    video_folder = VideoFolder(fs_url=folder_url)
    video_folder.folder_name = account.get_file_name(folder_url)
    video_folder.save()

    extracted_links = account.extract_links(folder_url)

    for link in extracted_links:
        if len(Video.objects.filter(fs_url=link['file_url'])) == 0:
            save_extracted_link_file(account, link['file_url'], video_folder)

def save_extracted_link_file(account, url, video_folder=None):
    file_url = account.get_link(url)
    file_type = get_file_extension(file_url)
    file_name = account.get_file_name(url)
    file_size = account.get_file_size(url)

    video = []

    if file_type in ['mp4', 'mkv', 'avi', 'wmv']:
        videos = Video.objects.filter(fs_url=url)
        if len(videos) > 0:
            video = videos[0]
        else:
            video = Video(fs_url=url)
        video.file_name = file_name
        video.file_url = file_url
        video.file_size = file_size
        video.file_type = file_type
        video.file_code = get_media_id(url)
        if video_folder:
            video.folder = video_folder
        video.save()

    return video


class save_extracted_link_file_thread(Thread):
    def __init__(self, account, url, video_folder):
        self.account = account
        self.url = url
        self.video_folder = video_folder
        super(save_extracted_link_file_thread, self).__init__()

    def run(self):
        try:
            file_url = self.account.get_link(self.url)
            file_type = get_file_extension(file_url)
            file_name = self.account.get_file_name(self.url)
            file_size = self.account.get_file_size(self.url)

            if file_type in ['mp4', 'mkv', 'avi', 'wmv']:
                videos = Video.objects.filter(fs_url=self.url)
                if len(videos) > 0:
                    video = videos[0]
                else:
                    video = Video(fs_url=self.url)

                video = Video(fs_url=self.url)
                video.file_name = file_name
                video.file_url = file_url
                video.file_size = file_size
                video.file_type = file_type
                video.file_code = get_media_id(self.url)
                if self.video_folder:
                    video.folder = self.video_folder
                video.save()
        except Exception as e:
            print e


def save_video(account, code):
    url = get_full_url(code)
    file_url = account.get_media_link(code)
    file_type = get_file_extension(file_url)
    file_name = account.get_file_name(url)
    file_size = account.get_file_size(url)

    video = []

    if file_type in ['mp4', 'mkv', 'avi', 'wmv']:
        videos = Video.objects.filter(fs_url=url)
        if len(videos) > 0:
            video = videos[0]
        else:
            video = Video(fs_url=url)
        video.file_name = file_name
        video.file_url = file_url
        video.file_size = file_size
        video.file_type = file_type
        video.file_code = get_media_id(url)
        video.save()

    return video

def humanbytes(B):
   'Return the given bytes as a human friendly KB, MB, GB, or TB string'
   B = float(B)
   KB = float(1024)
   MB = float(KB ** 2) # 1,048,576
   GB = float(KB ** 3) # 1,073,741,824
   TB = float(KB ** 4) # 1,099,511,627,776

   if B < KB:
      return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
   elif KB <= B < MB:
      return '{0:.2f} KB'.format(B/KB)
   elif MB <= B < GB:
      return '{0:.2f} MB'.format(B/MB)
   elif GB <= B < TB:
      return '{0:.2f} GB'.format(B/GB)
   elif TB <= B:
      return '{0:.2f} TB'.format(B/TB)