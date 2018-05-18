# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import socket
import urllib2

from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from redurl.models import TinyURL
import tinyurl


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
                print original_url
                if not original_url.startswith("http://"):
                    original_url = "http://" + str(original_url)
                print original_url
                code = urllib2.urlopen(original_url).getcode()
                if code == 200:
                    try:
                        tiny_obj = TinyURL.objects.get(givenurl=original_url)
                        tiny_obj.hitcount = tiny_obj.hitcount + 1
                        tiny_obj.save()
                        tiny_url = tiny_obj.biturl
                    except:
                        tiny_url = tinyurl.create_one(original_url)
                        tiny_object = TinyURL(givenurl=original_url, biturl=tiny_url, hitcount=1)
                        tiny_object.save()

                return Response({
                    'tiny_url': tiny_url,
                })
        except:
            return Response({
                'error': tiny_url
            })
