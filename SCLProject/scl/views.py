from datetime import date, datetime, tzinfo
from typing import ContextManager
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.
from django.views import View
from .forms import *
from django.utils import timezone
from django.db.models import Q


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

# TODO PRINT only table with information
# TODO SET TODAY's resil as default for dashboard
class ResiliationDashboard(UserPassesTestMixin,LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        resil = resiliation.objects.all()
        nombreResiliation = 0
        montantTotal = 0
        all_resiliation = []
        user_id = request.user.id
        
        if request.user.groups.filter(name='Caissier'):
            resil = resiliation.objects.filter(user = user_id)
            for name in resil:
                added_by = [user.username for user in User.objects.filter(resiliation=name)]
                montantTotal += name.montant_a_payer
                nombreResiliation += 1
                resiliation_data = {
                    'id_resiliation': name.id,
                    'date_ajout': name.date_ajout,
                    'contrat': name.contrat,
                    'montant_a_payer': name.montant_a_payer,
                    'timbre': name.timbre,
                    'montant_ttc': name.montant_ttc,
                    'tva': name.tva,
                    'caissier': added_by[0],
                }
                all_resiliation.append(resiliation_data)
        else:
            for name in resil:
                added_by = [user.username for user in User.objects.filter(resiliation=name)]
                montantTotal += name.montant_a_payer
                nombreResiliation += 1
                resiliation_data = {
                    'id_resiliation': name.id,
                    'date_ajout': name.date_ajout,
                    'contrat': name.contrat,
                    'montant_a_payer': name.montant_a_payer,
                    'timbre': name.timbre,
                    'montant_ttc': name.montant_ttc,
                    'tva': name.tva,
                    'caissier': added_by[0],
                }
                all_resiliation.append(resiliation_data)

        
        all_resiliation.sort(key=lambda item:item['date_ajout'], reverse=True)

        context = {
            'resiliation': all_resiliation,
            'nombre_resiliation': nombreResiliation,
            'montant_total': montantTotal
        }

        return render(request,'scl/resiliationDashboard.html',context)

    def test_func(self):
        return self.request.user.groups.all()


class SearchResiliationDashboard(UserPassesTestMixin,LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")
        query_date_filter = datetime.strptime(query,"%Y-%m-%d")

        resil = resiliation.objects.filter(Q(date_ajout__icontains=query))
        nombreResiliation = 0
        montantTotal = 0
        all_resiliation = []
        user_id = request.user.id
        
        if request.user.groups.filter(name='Caissier'):
            resil = resiliation.objects.filter(user = user_id, date_ajout__year = query_date_filter.year, date_ajout__month=query_date_filter.month, date_ajout__day=query_date_filter.day)
            for name in resil:
                added_by = [user.username for user in User.objects.filter(resiliation=name)]
                montantTotal += name.montant_a_payer
                nombreResiliation += 1
                resiliation_data = {
                    'id_resiliation': name.id,
                    'date_ajout': name.date_ajout,
                    'contrat': name.contrat,
                    'montant_a_payer': name.montant_a_payer,
                    'timbre': name.timbre,
                    'montant_ttc': name.montant_ttc,
                    'tva': name.tva,
                    'caissier': added_by[0],
                }
                all_resiliation.append(resiliation_data)
        else:
            for name in resil:
                added_by = [user.username for user in User.objects.filter(resiliation=name)]
                montantTotal += name.montant_a_payer
                nombreResiliation += 1
                resiliation_data = {
                    'id_resiliation': name.id,
                    'date_ajout': name.date_ajout,
                    'contrat': name.contrat,
                    'montant_a_payer': name.montant_a_payer,
                    'timbre': name.timbre,
                    'montant_ttc': name.montant_ttc,
                    'tva': name.tva,
                    'caissier': added_by[0],
                }
                all_resiliation.append(resiliation_data)

        
        all_resiliation.sort(key=lambda item:item['date_ajout'], reverse=True)

        context = {
            'resiliation': all_resiliation,
            'nombre_resiliation': nombreResiliation,
            'montant_total': montantTotal
        }

        return render(request,'scl/resiliationDashboard.html',context)

    def test_func(self):
        return self.request.user.groups.all()

class AffaireDashboard(View):
    def get(self, request, *args, **kwargs):
        aff = affaire.objects.all()
        nombreAffaire = 0
        montantTotal = 0
        all_affaire = []
        user_id = request.user.id

        if request.user.groups.filter(name='Caissier'):
            aff= affaire.objects.filter(user=user_id)
            for case in aff:
                montantTotal += case.montant
                nombreAffaire += 1
                added_by = [user.username for user in User.objects.filter(affaire=case)]
                affaire_data = {
                    'caissier': added_by[0],
                    'id_affaire': case.id,
                    'date_ajout': case.date_ajout,
                    'contrat': case.contrat,
                    'libelle': case.libelle_affaire,
                    'technicien': case.technicien,
                    'montant': case.montant,
                }
                all_affaire.append(affaire_data)
        else:
            for case in aff:
                montantTotal += case.montant
                nombreAffaire += 1
                added_by = [user.username for user in User.objects.filter(affaire=case)]
                affaire_data = {
                    'caissier': added_by[0],
                    'id_affaire': case.id,
                    'date_ajout': case.date_ajout,
                    'contrat': case.contrat,
                    'libelle': case.libelle_affaire,
                    'technicien': case.technicien,
                    'montant': case.montant,
                }
                all_affaire.append(affaire_data)

        context = {
            'montant_total': montantTotal,
            'affaire': all_affaire,
            'nombre_affaire': nombreAffaire
        }
        
        return render(request,'scl/affaireDashboard.html', context)

class SearchAffaireDashboard(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")
        query_date_filter = datetime.strptime(query,"%Y-%m-%d")

        aff = affaire.objects.filter(Q(date_ajout__icontains=query))
        nombreAffaire = 0
        montantTotal = 0
        all_affaire = []
        user_id = request.user.id

        if request.user.groups.filter(name='Caissier'):
            aff= affaire.objects.filter(user=user_id, date_ajout__year = query_date_filter.year, date_ajout__month=query_date_filter.month, date_ajout__day=query_date_filter.day)
            for case in aff:
                montantTotal += case.montant
                nombreAffaire += 1
                added_by = [user.username for user in User.objects.filter(affaire=case)]
                affaire_data = {
                    'caissier': added_by[0],
                    'id_affaire': case.id,
                    'date_ajout': case.date_ajout,
                    'contrat': case.contrat,
                    'libelle': case.libelle_affaire,
                    'technicien': case.technicien,
                    'montant': case.montant,
                }
                all_affaire.append(affaire_data)
        else:
            for case in aff:
                montantTotal += case.montant
                nombreAffaire += 1
                added_by = [user.username for user in User.objects.filter(affaire=case)]
                affaire_data = {
                    'caissier': added_by[0],
                    'id_affaire': case.id,
                    'date_ajout': case.date_ajout,
                    'contrat': case.contrat,
                    'libelle': case.libelle_affaire,
                    'technicien': case.technicien,
                    'montant': case.montant,
                }
                all_affaire.append(affaire_data)

        context = {
            'montant_total': montantTotal,
            'affaire': all_affaire,
            'nombre_affaire': nombreAffaire
        }
        
        return render(request,'scl/affaireDashboard.html', context)

class ManuelDashboard(View):
    def get(self, request, *args, **kwargs):
        encaissement = manuel.objects.all()
        nombreManuel = 0
        montantTotal = 0
        all_manuel = []
        user_id = request.user.id
        if request.user.groups.filter(name='Caissier'):
            encaissement = manuel.objects.filter(user = user_id)
            for manu in encaissement:
                added_by = [user.username for user in User.objects.filter(manuel = manu) ]
                nombreManuel +=1
                montantTotal += manu.montant
                manuel_data = {
                    'id_manuel': manu.id,
                    'date_ajout': manu.date_ajout,
                    'contrat': manu.contrat,
                    'nom_client': manu.nom_client,
                    'motif_reglement': manu.motif_reglement,
                    'mode_payement': manu.mode_payement,
                    'montant': manu.montant,
                    'caissier': added_by[0]
                }
                all_manuel.append(manuel_data)
        else:
            for manu in encaissement:
                added_by = [user.username for user in User.objects.filter(manuel = manu) ]
                nombreManuel +=1
                montantTotal += manu.montant
                manuel_data = {
                    'id_manuel': manu.id,
                    'date_ajout': manu.date_ajout,
                    'contrat': manu.contrat,
                    'nom_client': manu.nom_client,
                    'motif_reglement': manu.motif_reglement,
                    'mode_payement': manu.mode_payement,
                    'montant': manu.montant,
                    'caissier': added_by[0]
                    }
                all_manuel.append(manuel_data)
            
        context={
            'manuel': all_manuel,
            'nombre_manuel': nombreManuel,
            'montant_total': montantTotal
        }
        return render(request, 'scl/manuelDashboard.html', context)


class SearchManuelDashboard(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")
        query_date_filter = datetime.strptime(query,"%Y-%m-%d")

        encaissement = manuel.objects.filter(Q(date_ajout__icontains=query))
        nombreManuel = 0
        montantTotal = 0
        all_manuel = []
        user_id = request.user.id
        if request.user.groups.filter(name='Caissier'):
            encaissement = manuel.objects.filter(user = user_id, date_ajout__year = query_date_filter.year, date_ajout__month=query_date_filter.month, date_ajout__day=query_date_filter.day)
            for manu in encaissement:
                added_by = [user.username for user in User.objects.filter(manuel = manu) ]
                nombreManuel +=1
                montantTotal += manu.montant
                manuel_data = {
                    'id_manuel': manu.id,
                    'date_ajout': manu.date_ajout,
                    'contrat': manu.contrat,
                    'nom_client': manu.nom_client,
                    'motif_reglement': manu.motif_reglement,
                    'mode_payement': manu.mode_payement,
                    'montant': manu.montant,
                    'caissier': added_by[0]
                }
                all_manuel.append(manuel_data)
        else:
            for manu in encaissement:
                added_by = [user.username for user in User.objects.filter(manuel = manu) ]
                nombreManuel +=1
                montantTotal += manu.montant
                manuel_data = {
                    'id_manuel': manu.id,
                    'date_ajout': manu.date_ajout,
                    'contrat': manu.contrat,
                    'nom_client': manu.nom_client,
                    'motif_reglement': manu.motif_reglement,
                    'mode_payement': manu.mode_payement,
                    'montant': manu.montant,
                    'caissier': added_by[0]
                    }
                all_manuel.append(manuel_data)
            
        context={
            'manuel': all_manuel,
            'nombre_manuel': nombreManuel,
            'montant_total': montantTotal
        }
        return render(request, 'scl/manuelDashboard.html', context)