from django import test
from django.test import TestCase,  Client
from django.urls import reverse
from scl.models import *
import json
from django.contrib.auth.models import Group, User


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')

        # Manuel
        self.ajouter_manuel = reverse('manuel')
        self.search_manuel = reverse('manuel-search')
        self.update_manuel = reverse('update-manuel', args='1')

        # Affaire
        self.ajouter_affaire = reverse('affaire')
        self.search_affaire= reverse('affaire-search')
        self.update_affaire= reverse('update-affaire',args='1')

        # Resiliation
        self.ajouter_resiliation = reverse('resiliation')
        self.search_resiliation = reverse('resiliation-search')
        self.update_resiliation = reverse('update-resiliation',args='1')


        #create permissions group
        group_name = "Admin"
        self.group = Group(name=group_name)
        self.group.save()
        # Create a new user
        self.user = User.objects.create_superuser(
            username = 'foo',
            email = 'myemail@test.com',
            password = 'pass',
        )
        # Add group on new user created
        self.user.groups.add(self.group)
        self.user.save()
        
        self.logged_in = self.client.login(
            username='foo',
            password='pass'
        )


    def test_index_GET(self):

        response = self.client.get(self.index_url)
        
        if self.logged_in:    # check login success

            self.assertEqual(response.status_code, 200, u'user in group should have access')
            self.assertTemplateUsed(response,'scl/index.html')
            self.assertTemplateUsed(response,'scl/base.html')
            self.assertTemplateUsed(response,'scl/navigation.html')
            self.assertTemplateUsed(response,'scl/footer.html')

        else:

            self.assertEquals(response.status_code,302)
            print(response.json)
            print("check login ", self.logged_in)



    #Manuel
    def test_ajouter_manuel_urls(self):
        response = self.client.get(self.ajouter_manuel)
        
        if self.logged_in:    # check login success

            self.assertEquals(response.status_code,200)
            self.assertTemplateUsed(response,'scl/manuel.html')
            self.assertTemplateUsed(response,'scl/base.html')
            self.assertTemplateUsed(response,'scl/navigation.html')
            self.assertTemplateUsed(response,'scl/footer.html')

        else:

            self.assertEquals(response.status_code,302)
            print(response.json)
            print("check login ", self.logged_in)