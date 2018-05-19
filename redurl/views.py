# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import string

import datetime
import requests
import urlparse

from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response

from redurl.models import TinyURL


@api_view(['POST'])
def api_root(request):
    if request.method == 'GET':
        return Response({
            'data': 'post url to get tiny url',
        })

    elif request.method == 'POST':
        tiny_url = "invalid URL"
        try:
            if request.data:
                original_url = request.data['original_url']
                if not original_url.startswith("https://") and not original_url.startswith("http://"):
                    original_url = "https://" + str(original_url)

                req = requests.get(original_url)
                if req.status_code == 200:
                    try:
                        tiny_url = TinyURL.objects.get(givenurl=original_url).biturl
                    except:
                        try:
                            tiny_url = seven_base(tiny_url).strip()
                            tiny_object = TinyURL(givenurl=original_url, biturl=tiny_url, hitcount=0)
                            tiny_object.save()
                        except Exception as e:
                            tiny_url = e.message

                return Response({
                    'tiny_url': "http://"+get_domain(request.build_absolute_uri())+"/"+tiny_url,
                })
        except Exception as e:
            return Response({
                'error': e.message
            })


@api_view(['GET'])
def redirect_url(request, tiny_id):
    try:
        tiny_obj = TinyURL.objects.get(biturl=tiny_id)
        tiny_obj.hitcount += 1
        tiny_obj.save()
        tiny_url = tiny_obj.givenurl
        return redirect(tiny_url)
    except:
        return Response({
            'error': 'invalid URL',
        })


#Recursive: Random string generator using 'random' of length 7
def seven_base(tiny_url):
    bit_url = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + tiny_url + datetime.datetime.now().strftime("%I%M%p%B%d%Y")) for _ in range(7))
    try:
        TinyURL.objects.get(biturl=bit_url).exists()
        bit_url = seven_base(tiny_url)
    except:
        pass
    return bit_url


def get_domain(url):
    return urlparse.urlparse(url).netloc