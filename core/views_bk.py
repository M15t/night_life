#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.core.exceptions import PermissionDenied


from .forms import *
from .models import *
from .utils import FS
from .functions import *

TEMPLATE_PATH = 'night_life/'


def index(request, code=None):
    video = []
    videos = []
    raw_url = ''
    error = False
    status = ''

    MY_ID = 'trees1411@yahoo.com'
    MY_PWD = 'hidesomeone1'
    account = FS(email=MY_ID, password=MY_PWD)

    if code:
        dump_video = get_object_or_404(Video, file_code=code)

        result, status = check_url_media_file_valid(dump_video.file_url)

        if not result:
            video = save_extracted_link_file(account, dump_video.fs_url)
        else:
            video = dump_video

        if video.folder:
            videos = Video.objects.filter(folder__pk=video.folder.pk)

    if request.POST:
        raw_url = request.POST.get('raw_url', '')

        # check url exist in our system
        if not is_exist_in_system(raw_url):
            if is_file(raw_url):
                save_extracted_link_file(account, raw_url)
                # threads = []
                # t = save_extracted_link_file_thread(account, raw_url, video_folder=None)
                # threads.append(t)
                # t.start()
                #
                # for t in threads:
                #     t.join()
            else:
                save_extracted_link_folder(account, raw_url)

        if is_file(raw_url):
            video = Video.objects.get(fs_url=raw_url)
        else:
            videos = Video.objects.filter(folder__fs_url=raw_url)
            video = videos[0]

        return redirect('core_views_save_and_watch', code=video.file_code)

    params = {
        'raw_url': raw_url,
        'video': video,
        'videos': videos,
        'error': error,
        'status': status,
    }

    return render(request, TEMPLATE_PATH + 'index.html', params)


def play(request, code=None):
    MY_ID = 'trees1411@yahoo.com'
    MY_PWD = 'hidesomeone1'
    account = FS(email=MY_ID, password=MY_PWD)

    fshare_prefix = 'https://www.fshare.vn/file/'

    link = account.get_media_link(code)

    try:
        video = Video.objects.get(file_code=code)
    except Exception as e:
        video = save_extracted_link_file(account, fshare_prefix + code)

    video.file_url = link
    video.save()

    params = {
        'link': link,
    }
    return render(request, TEMPLATE_PATH + "play.html", params)


def list(request):
    videos = Video.objects.all()
    params = {
        'videos': videos,
    }
    return render(request, TEMPLATE_PATH + "list.html", params)


def test(request):
    return HttpResponse('testing')