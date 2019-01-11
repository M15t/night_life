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

MY_ID = 'trees1411@yahoo.com'
MY_PWD = 'hidesomeone1'
global account
account = FS(email=MY_ID, password=MY_PWD)


def index(request, code=None):
    global account

    video = []
    videos = []
    error = False

    if request.POST:
        raw_url = request.POST.get('raw_url', '')

        if is_file(raw_url):
            return redirect('core_views_play', code=get_media_id(raw_url))
        else:
            error = "Này không phải là file bạn eiiii"

    params = {
        'video': video,
        'videos': videos,
        'error': error
    }

    return render(request, TEMPLATE_PATH + 'index.html', params)


def play(request, code):
    global account

    video = []
    videos = []
    error = False

    try:
        if code:
            video = save_video(account, code)
        else:
            videos = Video.objects.all().order_by('-pk')
    except Exception as e:
        print e
        error = str(e)

    params = {
        'video': video,
        'videos': videos,
        'error': error
    }
    return render(request, TEMPLATE_PATH + 'index.html', params)


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
    return
