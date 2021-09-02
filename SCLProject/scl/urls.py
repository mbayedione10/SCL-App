from django.urls import path
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('manuel/', AjouterManuel.as_view(), name='manuel'),
    path('resiliation/', AjouterResiliation.as_view(), name='resiliation'),
    path('affaire/',AjouterAffaire.as_view(), name='affaire'),
    path('resiliation/dashboard/', ResiliationDashboard.as_view(), name='resiliationDashboard' ),
    path('resiliation/search', SearchResiliationDashboard.as_view(), name='resiliation-search' ),
    path('affaire/dashboard', AffaireDashboard.as_view(), name='affaireDashboard'),
    path('affaire/search', SearchAffaireDashboard.as_view(), name='affaire-search' ),
    path('manuel/dashboard', ManuelDashboard.as_view(), name='manuelDashboard'),
    path('manuel/search', SearchManuelDashboard.as_view(), name='manuel-search' ),

    path('dashboard', Dashboard.as_view(), name='dashboard'),
    


]
#urlpatterns += static(se)