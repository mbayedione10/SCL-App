from django import test
from django.http.request import HttpRequest
from django.test import TestCase,  Client
from django.urls import reverse
from scl.models import *
import json
from django.contrib.auth.models import Group, User
from django.utils import timezone

class TestViews(TestCase):
    def setUp(self):
        self.client_admin = Client()
        self.client_caissier = Client()
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
        self.group_admin = Group(name=group_name)
        group_name2 = "Caissier"
        self.group_caissier = Group(name=group_name2)
        self.group_admin.save()
        self.group_caissier.save()

        # Create a new user Admin
        self.user_admin = User.objects.create_superuser(
            username = 'foo',
            email = 'myemail@test.com',
            password = 'pass',
        )
        # Add group on new user created
        self.user_admin.groups.add(self.group_admin)
        self.user_admin.save()
        self.logged_in_admin = self.client_admin.login(
            username='foo',
            password='pass'
        )


        # Create a new user Caissier
        self.user_caissier = User.objects.create_superuser(
            username = 'foo_caissier',
            email = 'myemail_caissier@test.com',
            password = 'pass_caissier',
        )
        # Add group on new user created
        self.user_caissier.groups.add(self.group_caissier)
        self.user_caissier.save()
        self.logged_in_caissier = self.client_caissier.login(
            username='foo_caissier',
            password='pass_caissier'
        )

    def test_index_GET(self):

        response_caissier = self.client_caissier.get(self.index_url)
        response_admin = self.client_admin.get(self.index_url)
        
        if self.logged_in_admin and self.logged_in_caissier:    # check if login success and user in groups

            # Admin
            self.assertEqual(response_admin.status_code, 200, u'user in group should have access')
            self.assertTemplateUsed(response_admin,'scl/index.html')
            self.assertTemplateUsed(response_admin,'scl/base.html')
            self.assertTemplateUsed(response_admin,'scl/navigation.html')
            self.assertTemplateUsed(response_admin,'scl/footer.html')
            # Caissier
            self.assertEqual(response_caissier.status_code, 200, u'user in group should have access')
            self.assertTemplateUsed(response_caissier,'scl/index.html')
            self.assertTemplateUsed(response_caissier,'scl/base.html')
            self.assertTemplateUsed(response_caissier,'scl/navigation.html')
            self.assertTemplateUsed(response_caissier,'scl/footer.html')

        else:

            # self.assertEquals(response.status_code,302)
            print("check login admin", self.logged_in_admin)
            print(response_admin.json)
            print("admin status code", response_admin.status_code)

            print("check login caissier", self.logged_in_caissier)
            print(response_caissier.json)
            print("caissier status code",response_caissier.status_code)

    # TODO add test for POST
    def test_ajouter_manuel_POST(self):
        response = self.client_caissier.post(self.ajouter_manuel,{
                'motif_reglement': 'extension reseau',
                'mode_payement': 'Espéces',
                'montant': 100000,
                'contrat': '15425-526421',
                'village': 'dksdjf',
                'nom_client': 'sffg sdff',
                'contact_client': '771234567'
            })
        
        if self.logged_in_caissier:
            print(response.json)
            print(response.status_code)

            
        

    #Manuel
    def test_ajouter_manuel_GET(self):
        response_caissier = self.client_caissier.get(self.ajouter_manuel)
        response_admin = self.client_admin.get(self.ajouter_manuel)
        
        if self.logged_in_admin and self.logged_in_caissier:    # check login success and user in groups

            # Admin
            self.assertEqual(response_admin.status_code, 200, u'user in group should have access')
            self.assertTemplateUsed(response_admin,'scl/manuel.html')
            self.assertTemplateUsed(response_admin,'scl/base.html')
            self.assertTemplateUsed(response_admin,'scl/navigation.html')
            self.assertTemplateUsed(response_admin,'scl/footer.html')
            # Caissier
            self.assertEqual(response_caissier.status_code, 200, u'user in group should have access')
            self.assertTemplateUsed(response_caissier,'scl/manuel.html')
            self.assertTemplateUsed(response_caissier,'scl/base.html')
            self.assertTemplateUsed(response_caissier,'scl/navigation.html')
            self.assertTemplateUsed(response_caissier,'scl/footer.html')

        else:

            print("check login admin", self.logged_in_admin)
            print(response_admin.json)
            print("admin status code", response_admin.status_code)

            print("check login caissier", self.logged_in_caissier)
            print(response_caissier.json)
            print("caissier status code",response_caissier.status_code)
    
    def test_dashboard_manuel_views(self):
        response_caissier = self.client_caissier.get(self.search_manuel)
        response_admin = self.client_admin.get(self.search_manuel)
        
        if self.logged_in_admin and self.logged_in_caissier:    # check login success and user in groups

            # Admin
            self.assertEqual(response_admin.status_code, 200, u'user in group should have access')
            self.assertTemplateUsed(response_admin,'scl/manuelDashboard.html')
            self.assertTemplateUsed(response_admin,'scl/base.html')
            self.assertTemplateUsed(response_admin,'scl/navigation.html')
            self.assertTemplateUsed(response_admin,'scl/footer.html')
            # Caissier
            self.assertEqual(response_caissier.status_code, 200, u'user in group should have access')
            self.assertTemplateUsed(response_caissier,'scl/manuelDashboard.html')
            self.assertTemplateUsed(response_caissier,'scl/base.html')
            self.assertTemplateUsed(response_caissier,'scl/navigation.html')
            self.assertTemplateUsed(response_caissier,'scl/footer.html')

        else:

            print("check login admin", self.logged_in_admin)
            print(response_admin.json)
            print("admin status code", response_admin.status_code)

            print("check login caissier", self.logged_in_caissier)
            print(response_caissier.json)
            print("caissier status code",response_caissier.status_code)
"""
    def test_update_manuel_views(self):
        response_caissier = self.client_caissier.get(self.update_manuel)
        response_admin = self.client_admin.get(self.update_manuel)
        
        if self.logged_in_admin:    # check login success and user in groups

            # Admin
            self.assertEqual(response_admin.status_code, 200, u'user in group should have access')
            self.assertTemplateUsed(response_admin,'scl/update-manuel.html')
            self.assertTemplateUsed(response_admin,'scl/base.html')
            self.assertTemplateUsed(response_admin,'scl/navigation.html')
            self.assertTemplateUsed(response_admin,'scl/footer.html')
            # # Caissier
            # self.assertEqual(response_caissier.status_code, 200, u'user in group should have access')
            # self.assertTemplateUsed(response_caissier,'scl/update-manuel.html')
            # self.assertTemplateUsed(response_caissier,'scl/base.html')
            # self.assertTemplateUsed(response_caissier,'scl/navigation.html')
            # self.assertTemplateUsed(response_caissier,'scl/footer.html')

        else:

            print("check login admin", self.logged_in_admin)
            print(response_admin.json)
            print("admin status code", response_admin.status_code)

            print("check login caissier", self.logged_in_caissier)
            print(response_caissier.json)
            print("caissier status code",response_caissier.status_code)

"""
