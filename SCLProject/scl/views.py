from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from .forms import *
from django.utils.timezone import datetime


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

    
    def post(self,request, *args, **kwargs):
        form = AffaireForm(request.POST)
        if 'save' in request.POST:

            if form.is_valid():
                #Save form and add user and date
                newAffaire =form.save()
                newAffaire.date_ajout= datetime.now()
                list_id = []
                user_id= request.user.id
                list_id.append(user_id)
                newAffaire.user.add(*list_id)

                newAffaire.save()
                

            return redirect('index')