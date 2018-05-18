# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import socket
import urllib2
import string
import random

from math import floor

from django.shortcuts import render, redirect

from rest_framework.decorators import api_view
from rest_framework.response import Response

from redurl.models import TinyURL
from zpxtinyurl.settings import BASE_URL_, BASE_URL


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
                if not original_url.startswith("https://") and  not original_url.startswith("http://") :
                    original_url = "https://" + str(original_url)
                code = urllib2.urlopen(original_url).getcode()
                print code
                if code == 200:
                    try:
                        tiny_url = TinyURL.objects.get(givenurl=original_url).biturl
                    except Exception as e:
                        print e.message
                        try:
                            tiny_url = sevenbase(tiny_url).strip()
                            tiny_object = TinyURL(givenurl=original_url, biturl=tiny_url, hitcount=0)
                            tiny_object.save()
                        except Exception as e:
                            print e.message


                return Response({
                    'tiny_url': BASE_URL_+"/"+tiny_url,
                })
        except Exception as e:
            print e.message
            return Response({
                'error': e.message
            })

@api_view(['GET'])
def redirecturl(request, tiny_id):
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
def sevenbase(tiny_url):
    biturl = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + tiny_url) for _ in range(7))
    try:
        TinyURL.objects.get(biturl=biturl).exists()
        biturl = sevenbase(tiny_url)
    except:
        pass
    return biturl