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
        return self.request.user.is_authenticated


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
    
    def post(self, request, *args, **kwargs):
        form = ResiliationForm(request.POST)
        if 'save' in request.POST:
            if form.is_valid():
                newResiliation = form.save()
                newResiliation.redTableau = 429*newResiliation.nombre_mois
                if newResiliation.nombre_mois>0:
                    newResiliation.is_paid = True
                    newResiliation.frais_coupure = 2000
                    newResiliation.frais_retard = 500*newResiliation.nombre_mois
                    newResiliation.tva = 0.18*(newResiliation.redTableau+newResiliation.frais_coupure)
                    newResiliation.montant_ttc = newResiliation.redTableau + newResiliation.frais_coupure + newResiliation.frais_retard + newResiliation.tva
                    if newResiliation.montant_ttc > 20000:
                        newResiliation.timbre = 0.01*newResiliation.montant_ttc
                    else:
                        newResiliation.timbre = 0
                    newResiliation.montant_a_payer = newResiliation.montant_ttc + newResiliation.timbre
                newResiliation.date_ajout = timezone.datetime.now(tz=timezone.utc)
                list_id = []
                user_id = request.user.id
                list_id.append(user_id)
                newResiliation.user.add(*list_id)
                newResiliation.save()
        
        return redirect('index')

    

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


class ResiliationDashboard(View):
    def get(self, request, *args, **kwargs):

        resil = resiliation.objects.all()
        nombreResiliation = 0
        montantTotal = 0
        all_resiliation = []
        
        # if request.user.groups.filter(name='Caissier'):
        for name in resil:
            added_by = [user.username for user in User.objects.filter(resiliation=name)]
            montantTotal += name.montant_a_payer
            nombreResiliation += 1
            resiliation_date = {
                'id_resiliation': name.id,
                'date_ajout': name.date_ajout,
                'contrat': name.contrat,
                'montant_a_payer': name.montant_a_payer,
                'timbre': name.timbre,
                'montant_ttc': name.montant_ttc,
                'tva': name.tva,
                'caissier': added_by[0],
            }
            all_resiliation.append(resiliation_date)
        
        all_resiliation.sort(key=lambda item:item['date_ajout'], reverse=True)
        # print(all_resiliation)

        context = {
            'resiliation': all_resiliation,
            'nombre_resiliation': nombreResiliation,
            'montant_total': montantTotal
        }

        return render(request,'scl/resiliationDashboard.html',context)