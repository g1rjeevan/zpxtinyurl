# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from rest_framework.test import APITestCase

from redurl.views import seven_base


class APITests(APITestCase):
    def test_api_url(self):
        data = { "original_url":"www.google.com" }
        random_char = seven_base(data.get('original_url')).strip()
        self.assertLessEqual(len(random_char),7)
        resp = self.client.get("/"+random_char)
        #301 status code for redirecting
        self.assertEqual(resp.status_code, status.HTTP_301_MOVED_PERMANENTLY)
        error_data = { 'error': "invalid URL" }
        response = self.client.post('/api/short/new', data, format='json')
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data, error_data)