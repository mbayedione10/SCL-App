from django.urls import path
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('manuel/', AjouterManuel.as_view(), name='manuel'),
    path('resiliation/', AjouterResiliation.as_view(), name='resiliation'),
    path('affaire/',AjouterAffaire.as_view(), name='affaire'),
    path('resiliation/dashboard/', ResiliationDashboard.as_view(), name='resiliationDashboard' ),
    path('resiliation/search', SearchResiliationDashboard.as_view(), name='resiliation-search' )


]
#urlpatterns += static(se)