# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
# Create a JSON POST request
from rest_framework.test import APIRequestFactory
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        data = { "original_url":"www.google.com" }
        error_data = { 'error': "invalid URL" }
        response = self.client.post('', data, format='json')
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data, error_data)