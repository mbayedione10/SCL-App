from django import test
from django.test import TestCase,  Client
from django.urls import reverse
from django.urls.base import resolve
from scl.models import *
import json
from django.contrib.auth.models import User


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')

        self.user = User.objects.create_superuser(
            'foo',
            'myemail@test.com',
            'pass'
        )
        self.logged_in = self.client.login(
            username='foo',
            password='pqass'
        )


    def test_index_GET(self):

        response = self.client.get(self.index_url)
        
        if self.logged_in:    # check login success

            self.assertEquals(response.status_code,200)
            self.assertTemplateUsed(response,'scl/index.html')
            self.assertTemplateUsed(response,'scl/base.html')
            self.assertTemplateUsed(response,'scl/navigation.html')
            self.assertTemplateUsed(response,'scl/footer.html')

        else:

            self.assertEquals(response.status_code,302)
            print(response.json)
            print("check login ", self.logged_in)


