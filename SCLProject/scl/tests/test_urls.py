from django import urls
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from scl.views import *  

class TestUrls(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse('index')
        print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, Index)

    #Manuel
    def test_ajouter_manuel_url_resolves(self):
        url = reverse('manuel')
        print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, AjouterManuel)

    def test_update_manuel_url_resolves(self):
        url = reverse('update-manuel', args = '1')
        print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, UpdateManuel)

    def test_search_manuel_url_resolves(self):
        url = reverse('manuel-search')
        print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, SearchManuelDashboard)

    # Resiliations
    def test_ajouter_resiliation_url_resolves(self):
        url = reverse('resiliation')
        print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, AjouterResiliation)

    def test_update_resiliatiion_url_resolves(self):
        url = reverse('update-resiliation', args = '1')
        print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, UpdateResiliation)

    def test_search_resiliation_url_resolves(self):
        url = reverse('resiliation-search')
        print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, SearchResiliationDashboard)

    # Affaires
    def test_ajouter_affaire_url_resolves(self):
        url = reverse('affaire')
        print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, AjouterAffaire)

    def test_update_resiliatiion_url_resolves(self):
        url = reverse('update-affaire', args = '1')
        print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, UpdateAffaire)

    def test_search_affaire_url_resolves(self):
        url = reverse('affaire-search')
        print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, SearchAffaireDashboard)