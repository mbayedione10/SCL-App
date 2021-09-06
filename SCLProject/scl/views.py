from datetime import datetime
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
            else:
                form = ManuelForm()
                context = {
                    'form': form,
                }
                return render(request, 'scl/manuel.html', context)
    
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
            else:
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
            else:
                form = AffaireForm
                context = {
                    'form': form,
                    }
                return render(request,'scl/affaire.html', context)
                

        
    
    def test_func(self):
        return self.request.user.groups.all()

# TODO PRINT only table with information
today = datetime.today()
class ResiliationDashboard(UserPassesTestMixin,LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        resil = resiliation.objects.filter(date_ajout__year=today.year, date_ajout__month=today.month, date_ajout__day=today.day)
        nombreResiliation = 0
        montantTotal = 0
        all_resiliation = []
        user_id = request.user.id
        
        if request.user.groups.filter(name='Caissier'):
            resil = resiliation.objects.filter(user = user_id,date_ajout__year=today.year, date_ajout__month=today.month, date_ajout__day=today.day)
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
        aff = affaire.objects.filter(date_ajout__year=today.year, date_ajout__month=today.month, date_ajout__day=today.day)
        nombreAffaire = 0
        montantTotal = 0
        all_affaire = []
        user_id = request.user.id

        if request.user.groups.filter(name='Caissier'):
            aff= affaire.objects.filter(user=user_id,date_ajout__year=today.year, date_ajout__month=today.month, date_ajout__day=today.day)
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
        all_affaire.sort(key=lambda item:item['date_ajout'], reverse=True)
        context = {
            'montant_total': montantTotal,
            'affaire': all_affaire,
            'nombre_affaire': nombreAffaire
        }
        
        return render(request,'scl/affaireDashboard.html', context)
    
    def test_func(self):
        return self.request.user.groups.all()

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
        all_affaire.sort(key=lambda item:item['date_ajout'], reverse=True)
        context = {
            'montant_total': montantTotal,
            'affaire': all_affaire,
            'nombre_affaire': nombreAffaire
        }
        
        return render(request,'scl/affaireDashboard.html', context)
    
    def test_func(self):
        return self.request.user.groups.all()

class ManuelDashboard(View):
    def get(self, request, *args, **kwargs):
        encaissement = manuel.objects.filter(date_ajout__year=today.year, date_ajout__month=today.month, date_ajout__day=today.day)
        nombreManuel = 0
        montantTotal = 0
        all_manuel = []
        user_id = request.user.id
        if request.user.groups.filter(name='Caissier'):
            encaissement = manuel.objects.filter(user = user_id,date_ajout__year=today.year, date_ajout__month=today.month, date_ajout__day=today.day)
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
        all_manuel.sort(key=lambda item:item['date_ajout'], reverse=True)
        context={
            'manuel': all_manuel,
            'nombre_manuel': nombreManuel,
            'montant_total': montantTotal
        }
        return render(request, 'scl/manuelDashboard.html', context)

    def test_func(self):
        return self.request.user.groups.all()


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
        all_manuel.sort(key=lambda item:item['date_ajout'], reverse=True)
        context={
            'manuel': all_manuel,
            'nombre_manuel': nombreManuel,
            'montant_total': montantTotal
        }
        return render(request, 'scl/manuelDashboard.html', context)

    def test_func(self):
        return self.request.user.groups.all()


class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        montants = []
        montant_resiliation = 0
        montant_affaire = 0
        montant_manuel = 0

        user_id = [user.id for user in User.objects.all()]
        
        for name in user_id:
            user = User.objects.get(id=name)
            if user.groups.filter(name='Caissier'):
                encaissement = manuel.objects.filter(user = name,date_ajout__year=today.year, date_ajout__month=today.month, date_ajout__day=today.day)
                aff = affaire.objects.filter(user = name,date_ajout__year=today.year, date_ajout__month=today.month, date_ajout__day=today.day)
                resil = resiliation.objects.filter(user = name,date_ajout__year=today.year, date_ajout__month=today.month, date_ajout__day=today.day)

                for manu in encaissement:
                    montant_manuel += manu.montant
                for cancel in resil:
                    montant_resiliation += cancel.montant_a_payer
                for case in aff:
                    montant_affaire += case.montant
                global_user = {
                    'nom': user,
                    'montant_manuel': montant_manuel,
                    'montant_resiliation': montant_resiliation,
                    'montant_affaire': montant_affaire
                }

                montants.append(global_user)
                montant_manuel=0
                montant_resiliation=0
                montant_affaire=0
        context={
            'montants': montants,
        }

        return render (request, 'scl/dashboard.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='Admin')

class SearchDashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")
        query_date_filter = datetime.strptime(query,"%Y-%m-%d")

        montants = []
        montant_resiliation = 0
        montant_affaire = 0
        montant_manuel = 0

        user_id = [user.id for user in User.objects.all()]
        
        for name in user_id:
            user = User.objects.get(id=name)
            if user.groups.filter(name='Caissier'):
                encaissement = manuel.objects.filter(user = name, date_ajout__year = query_date_filter.year, date_ajout__month=query_date_filter.month, date_ajout__day=query_date_filter.day)
                aff = affaire.objects.filter(user = name, date_ajout__year = query_date_filter.year, date_ajout__month=query_date_filter.month, date_ajout__day=query_date_filter.day)
                resil = resiliation.objects.filter(user = name, date_ajout__year = query_date_filter.year, date_ajout__month=query_date_filter.month, date_ajout__day=query_date_filter.day)

                for manu in encaissement:
                    montant_manuel += manu.montant
                for cancel in resil:
                    montant_resiliation += cancel.montant_a_payer
                for case in aff:
                    montant_affaire += case.montant
                global_user = {
                    'nom': user,
                    'montant_manuel': montant_manuel,
                    'montant_resiliation': montant_resiliation,
                    'montant_affaire': montant_affaire
                }

                montants.append(global_user)
                montant_manuel=0
                montant_resiliation=0
                montant_affaire=0
        context={
            'montants': montants,
        }

        return render (request, 'scl/dashboard.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='Admin')


class UpdateResiliation(LoginRequiredMixin,UserPassesTestMixin,View):
    def get(self,request,pk, *args, **kwargs):
        resil = resiliation.objects.get(pk=pk)
        if request.user.groups.filter(name='Admin'):
            form=ResiliationForm(instance=resil)
            return render(request, 'scl/update-resiliation.html', {'form':form})
    def post(self, request, pk, *args, **kwargs):
        newResiliation = resiliation.objects.get(pk=pk)
        form = ResiliationForm(request.POST or None, instance = newResiliation)

        if 'update' in request.POST:
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
                newResiliation.save()
        elif 'delete' in request.POST:
            newResiliation.delete()
        
        return redirect('resiliationDashboard')


    def test_func(self):
        return self.request.user.groups.filter(name='Admin')

class UpdateAffaire(LoginRequiredMixin,UserPassesTestMixin,View):
    def get(self, request,pk, *args, **kwargs):
        aff = affaire.objects.get(pk=pk)
        form = AffaireForm(instance=aff)
        context={
            'form':form
        }
        return render(request, 'scl/update-affaire.html', context)

    def post(self, request,pk,*args,**kwargs):
        newAffaire = affaire.objects.get(pk=pk)
        form = AffaireForm(request.POST or None, instance=newAffaire)
        if 'update' in request.POST:

            if form.is_valid():
                #Save form and add user and date
                newAffaire.save()
        elif 'delete' in request.POST:
            newAffaire.delete()

        return redirect('affaireDashboard')
            
    def test_func(self):
        return self.request.user.groups.filter(name='Admin')
