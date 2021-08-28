from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.
from django.views import View
from .forms import *
from django.utils import timezone


class Index(LoginRequiredMixin, UserPassesTestMixin,View):
    def get(self, request):
        return render(request, 'scl/index.html')

    def test_func(self):
        return self.request.user.groups.all()


class AjouterManuel(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        form = ManuelForm()
        context = {
            'form': form,
        }
        return render(request, 'scl/manuel.html', context)

    def post(self, request, *args, **kwargs):
        form = ManuelForm(request.POST)

        if 'save' in request.POST:
            if form.is_valid():
                # Add manuel and excluded fields in form
                newManuel = form.save()

                newManuel.date_ajout = timezone.datetime.now(tz=timezone.utc)
                list_id=[]
                user_id = request.user.id
                list_id.append(user_id)
                newManuel.user.add(*list_id)

                newManuel.save()

        return redirect('index')
    
    def test_func(self):
        return self.request.user.groups.all()




class AjouterResiliation(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        form = ResiliationForm
        context = {
            'form': form,
        }
        return render(request,'scl/resiliation.html', context)

    

    def test_func(self):
        return self.request.user.groups.all()


class AjouterAffaire(LoginRequiredMixin, UserPassesTestMixin, View):
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
                newAffaire.date_ajout= timezone.datetime.now(tz=timezone.utc)
                list_id = []
                user_id= request.user.id
                list_id.append(user_id)
                newAffaire.user.add(*list_id)

                newAffaire.save()
                

        return redirect('index')
    
    def test_func(self):
        return self.request.user.groups.all()