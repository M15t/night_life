#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import json
import math
import string

from hyper import HTTPConnection
import requests

from .models import FSConfig

PING_URL = 'https://www.fshare.vn/file/QSIXWEZKM26E'


class FSAPI:
    """
    API Interface of Fshare.vn
    """

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.token = ""
        self.s = requests.Session()
        self.s.headers['User-Agent'] = 'okhttp/3.6.0'

    def login(self):
        config, _ = FSConfig.objects.get_or_create(
            app_key="dMnqMMZMUnN5YpvKENaEhdQQ5jxDqddt")

        self.token = config.token
        cookie = config.cookie
        self.s.cookies.set('session_id', cookie)

        data = {
            'user_email': self.email,
            'password': self.password,
            'app_key': config.app_key,
        }

        # call a test
        r = self.s.post(
            'https://api.fshare.vn/api/fileops/get',
            json={
                'token': self.token,
                'url': PING_URL,
            }
        )

        if r.status_code != 200:
            url = "https://api.fshare.vn/api/user/login"

            payload = "{\n\t\"user_email\" : \"+ self.email +\",\n\t\"password\":\t\"Tmrisdoomday!2\",\n\t\"app_key\" : \"dMnqMMZMUnN5YpvKENaEhdQQ5jxDqddt\"\n}"
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'checkAPI-UT42RX',
                'Cookie': 'session_id=he6iiesop1ht3q2val4u74edor'
            }

            response = requests.request(
                "POST", url, headers=headers, data=payload)

            login_data = response.json()

            config.token = login_data['token']
            config.cookie = login_data['session_id']
            config.save()

            self.token = config.token
            cookie = config.cookie
            self.s.cookies.set('session_id', cookie)

        return data

    def profile(self):
        r = self.s.get('https://api.fshare.vn/api/user/get')
        return r.json()

    def check_valid(self, url):
        url = url.strip()
        if not url.startswith('https://www.fshare.vn/'):
            raise Exception("Must be Fshare url")
        return url

    def download(self, url, password=None):
        url = self.check_valid(url)
        payload = {
            'token': self.token,
            'url': url
        }
        if password:
            payload['password'] = password

        r = self.s.post(
            'https://api.fshare.vn/api/session/download',
            json=payload
        )

        if r.status_code == 403:
            raise Exception("Password invalid")

        if r.status_code != 200:
            raise Exception("Link is dead")

        data = r.json()
        link = data['location']
        return link

    def get_folder_urls(self, url, page=0, limit=60):
        url = self.check_valid(url)
        r = self.s.post(
            'https://api.fshare.vn/api/fileops/getFolderList',
            json={
                'token': self.token,
                'url': url,
                'dirOnly': 0,
                'pageIndex': page,
                'limit': limit
            }
        )
        data = r.json()
        return data

    def get_home_folders(self):
        r = self.s.get(
            'https://api.fshare.vn/api/fileops/list?pageIndex=0&dirOnly=0&limit=60')
        return r.json()

    def get_file_info(self, url):
        url = self.check_valid(url)
        r = self.s.post(
            'https://api.fshare.vn/api/fileops/get',
            json={
                'token': self.token,
                'url': url,
            }
        )
        print "response ======== ", r
        return r.json()

    def upload(self, local_path, remote_path, secured=1):
        import os
        import io
        import ntpath
        import unidecode
        file_name = ntpath.basename(local_path)

        def format_filename(s):
            valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
            filename = ''.join(c for c in s if c in valid_chars)
            return filename
        file_name = format_filename(unidecode.unidecode(file_name))
        file_size = str(os.path.getsize(local_path))
        try:
            data = io.open(local_path, 'rb', buffering=25000000)
        except FileNotFoundError:
            raise Exception('File does not exist!')

        r = self.s.post(
            'https://api.fshare.vn/api/session/upload',
            json={
                'token': self.token,
                'name': file_name,
                'path': remote_path,
                'secured': 1,
                'size': file_size
            }
        )
        # print(self.token, local_path, remote_path)
        # print(r.json())

        location = r.json()['location']

        # OPTIONS for chunk upload configuration
        max_chunk_size = 25000000
        chunk_total = math.ceil(int(file_size)/max_chunk_size)

        for i in range(chunk_total):
            chunk_number = i + 1
            sent = last_index = i * max_chunk_size
            remaining = int(file_size) - sent
            if remaining < max_chunk_size:
                current_chunk = remaining
            else:
                current_chunk = max_chunk_size

            next_index = last_index + current_chunk

            chunk_params = {
                'flowChunkNumber': chunk_number,
                'flowChunkSize': max_chunk_size,
                'flowCurrentChunkSize': current_chunk,
                'flowTotalSize': file_size,
                'flowIdentifier': '{0}-{1}'.format(current_chunk, file_name),
                'flowFilename': file_name,
                'flowRelativePath': file_name,
                'flowTotalChunks': chunk_total
            }

            res = self.s.options(location, params=chunk_params)
            # POST upload data
            headers = {
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Content-Range': 'bytes {0}-{1}/{2}'.format(
                    last_index,
                    next_index - 1,
                    file_size),
                'DNT': '1',
                'Connection': 'keep-alive'
            }
            res = self.s.post(location,
                              params=chunk_params,
                              headers=headers,
                              data=data.read(max_chunk_size))
            try:
                if res.json():
                    return res.json()
                pass
            except Exception:
                pass
        data.close()
