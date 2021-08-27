from typing import ContextManager
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from .forms import *

class Index(View):
    def get(self, request):
        return render(request, 'scl/index.html')


class AjouterManuel(View):
    def get(self, request, *args, **kwargs):
        form = ManuelForm()
        context = {
            'form': form,
        }
        return render(request, 'scl/manuel.html', context)



class AjouterResiliation(View):
    def get(self, request, *args, **kwargs):
        form = ResiliationForm
        context = {
            'form': form,
        }
        return render(request,'scl/resiliation.html', context)


class AjouterAffaire(View):
    def get(self, request, *args, **kwargs):
        form = AffaireForm
        context={
            'form': form
        }
        return render(request,'scl/affaire.html',context)