#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt


from .forms import *
from .models import *
from .utils import FSAPI
from .functions import *

TEMPLATE_PATH = 'night_life/'

MY_ID = 'trees1411@yahoo.com'
MY_PWD = 'Tmrisdoomday!2'
global account
account = FSAPI(email=MY_ID, password=MY_PWD)


@csrf_exempt
def reponseSuccessJSON(request, data):
    # we allow to request JSONP here
    try:
        callback = request.GET.get("callback", "")
    except:
        callback = ""
    if (callback == ""):  # return as json normal
        return HttpResponse(json.dumps(data))
    else:  # return as jsonp
        return HttpResponse(callback + "(" + json.dumps(data) + ")")


def index(request):
    params = {}
    return render(request, TEMPLATE_PATH + 'index.html', params)


@csrf_exempt
def get(request):
    global account

    video = {}
    error_string = ""
    url = request.POST.get("url", "")

    if request.POST:
        if is_file(url) and leak_video(url):
            video = leak_video(url)
        elif is_folder(url) and leak_folder(url):
            video = leak_folder(url)[0]
        else:
            error_string = "Invalid link"

    jsondata = {
        "error_string": error_string,
        "code": video.file_code if video else "",
    }
    return reponseSuccessJSON(request, jsondata)


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
    leak_video("https://www.fshare.vn/file/TAPDJBLT4P2U")
    # leak_folder("https://www.fshare.vn/folder/JL4GOTQYBG1H")
    return HttpResponse("Testing..")
