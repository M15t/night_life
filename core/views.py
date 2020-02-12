#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.core.exceptions import PermissionDenied


from .forms import *
from .models import *
from .utils import FSAPI
from .functions import *

TEMPLATE_PATH = 'night_life/'

MY_ID = 'trees1411@yahoo.com'
MY_PWD = 'H!d3someone!2'
global account
account = FSAPI(email=MY_ID, password=MY_PWD)


def index(request):

    # if request.POST:
    #     raw_url = request.POST.get('raw_url', '')

    #     if is_file(raw_url):
    #         return redirect('core_views_play', code=get_media_id(raw_url))
    #     else:
    #         error = "Này không phải là file bạn eiiii"

    params = {}

    return render(request, TEMPLATE_PATH + 'index.html', params)


def get(request):
    global account

    video = []
    videos = []
    error_string = False
    raw_url = request.POST.get("raw_url", "")

    if request.POST:
        if is_file(raw_url):
            code = get_media_id(raw_url)
        else:
            error_string = "Not valid Fshare link"

        video = save_video(account, code)

    params = {
        'video': video,
        'code': video.file_code,
        'error_string': error_string
    }
    return render(request, TEMPLATE_PATH + 'play.html', params)


def play(request, code):
    global account

    video = []
    error_string = False
    try:
        video = Video.objects.get(file_code=code)
    except:
        error_string = "No data found"

    params = {
        'video': video,
        'error_string': error_string
    }
    return render(request, TEMPLATE_PATH + 'play.html', params)


def list(request):
    videos = Video.objects.all().order_by('-created_at')
    params = {
        'videos': videos,
    }
    return render(request, TEMPLATE_PATH + "list.html", params)


def remove(request, video_id):
    video = Video.objects.get(pk=video_id)
    video.delete()

    return redirect('core_views_list')


def test(request):
    mine = FSAPI(email=MY_ID, password=MY_PWD)
    mine.login()
    resp = mine.get_folder_urls("https://www.fshare.vn/folder/AT2HY4EGQ1P5")

    for d in resp:
        if d['mimetype'] != "text/plain":
            new_video = Video(fs_url=d['furl'], file_name=d['name'], file_code=d['linkcode'], file_url=mine.download(d['furl']), file_size=humanbytes(d['size']), file_type=d['mimetype'])
            new_video.save()


    # fs_url = "https://www.fshare.vn/file/QZKINH4VRWXR"
    # new_video = Video(fs_url=fs_url, file_code=get_media_id(fs_url), file_url=mine.download(fs_url))
    # new_video.save()
    # print "===", mine.download(fs_url)
    # print "===", mine.profile()
    # print "===", mine.get_file_info("https://www.fshare.vn/file/32RFHTIR3TK3")
    return
