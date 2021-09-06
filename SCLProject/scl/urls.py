from django.urls import path
from django.conf.urls.static import static
from .views import *

urlpatterns = [

    path('', Index.as_view(), name='index'),
    # Encaissements Manuel
    path('manuel/', AjouterManuel.as_view(), name='manuel'),
    path('manuel/dashboard', ManuelDashboard.as_view(), name='manuelDashboard'),
    path('manuel/search', SearchManuelDashboard.as_view(), name='manuel-search' ),
    path('updateManuel/<int:pk>', UpdateManuel.as_view(), name='update-manuel'),

    # Resiliations
    path('resiliation/', AjouterResiliation.as_view(), name='resiliation'),
    path('resiliation/dashboard/', ResiliationDashboard.as_view(), name='resiliationDashboard' ),
    path('resiliation/search', SearchResiliationDashboard.as_view(), name='resiliation-search' ),
    path('updateResiliation/<int:pk>', UpdateResiliation.as_view(), name='update-resiliation' ),

    # Affaires
    path('affaire/',AjouterAffaire.as_view(), name='affaire'),
    path('affaire/dashboard', AffaireDashboard.as_view(), name='affaireDashboard'),
    path('affaire/search', SearchAffaireDashboard.as_view(), name='affaire-search' ),
    path('updateAffaire/<int:pk>', UpdateAffaire.as_view(), name='update-affaire'),

    # Tableau de Bord
    path('dashboard', Dashboard.as_view(), name='dashboard'),
    path('dashboard/search', SearchDashboard.as_view(), name='dashboard-search' ),



    


]
#urlpatterns += static(se)