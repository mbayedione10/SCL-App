from django.urls import path
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('manuel/', AjouterManuel.as_view(), name='manuel'),

]
#urlpatterns += static(se)