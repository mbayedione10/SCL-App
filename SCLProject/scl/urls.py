from django.urls import path
from .views import *

urlpatterns = [

    path('', Index.as_view(), name='index'),
    # Encaissements Manuel
    path('manuel/', AjouterManuel.as_view(), name='manuel'),
    path('manuel/dashboard', SearchManuelDashboard.as_view(), name='manuel-search'),
    path('updateManuel/<int:pk>', UpdateManuel.as_view(), name='update-manuel'),

    # Resiliations
    path('resiliation/', AjouterResiliation.as_view(), name='resiliation'),
    path('resiliation/dashboard', SearchResiliationDashboard.as_view(), name='resiliation-search' ),
    path('updateResiliation/<int:pk>', UpdateResiliation.as_view(), name='update-resiliation' ),

    # Affaires
    path('affaire/',AjouterAffaire.as_view(), name='affaire'),
    path('affaire/dashboard', SearchAffaireDashboard.as_view(), name='affaire-search' ),
    path('updateAffaire/<int:pk>', UpdateAffaire.as_view(), name='update-affaire'),

    # Tableau de Bord
    path('dashboard', SearchDashboard.as_view(), name='dashboard'),

]
