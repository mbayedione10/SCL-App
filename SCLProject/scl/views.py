from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.
from django.views import View
from .forms import *
from django.utils import timezone
from django.db.models import Q


# LoginRequiredMixin: will just make sure the user in the request is logged in
# UserPassesTestMixin: will check the request from a boolean expression we define


class Index(LoginRequiredMixin, UserPassesTestMixin, View):
    """GET request to render the HTML template index"""

    def get(self, request):
        return render(request, 'scl/index.html')

    def test_func(self):
        return self.request.user.is_authenticated


class AjouterManuel(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request):
        """
        Form for manual operations
        :param request: GET
        :return: manuel.html
        """
        form = ManuelForm()
        context = {
            'form': form,
        }
        return render(request, 'scl/manuel.html', context)

    def post(self, request):
        """
        :param request: POST
        if POST done
            :return: index.html
        else
            :return: manuel.html

        """
        form = ManuelForm(request.POST)

        if 'save' in request.POST:
            if form.is_valid():
                # Add manuel and excluded fields in form
                new_manuel = form.save()

                new_manuel.date_ajout = timezone.datetime.now(tz=timezone.utc)
                list_id = []
                user_id = request.user.id
                list_id.append(user_id)
                new_manuel.user.add(*list_id)

                new_manuel.save()

                return redirect('index')
            form = ManuelForm()
            context = {
                'form': form,
            }
            return render(request, 'scl/manuel.html', context)

    def test_func(self):
        """
        Check if request.user is in a group
        :return: True or False
        """
        return self.request.user.groups.all()


class AjouterResiliation(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request):
        """
        Form for Cancel operations
        :param request: GET
        :return: resiliation.html
        """
        form = ResiliationForm
        context = {
            'form': form,
        }
        return render(request, 'scl/resiliation.html', context)

    def post(self, request):
        """
        if form is valid, calculate other fields based on the number of months entered by operator
        :param request: POST
        if POST done
            :return: index.html
        else
            :return: resiliation.html

        """
        form = ResiliationForm(request.POST)
        if 'save' in request.POST:
            if form.is_valid():
                new_resiliation = form.save()
                new_resiliation.redTableau = 429 * new_resiliation.nombre_mois
                if new_resiliation.nombre_mois > 0:
                    new_resiliation.is_paid = True
                    new_resiliation.frais_coupure = 2000
                    new_resiliation.frais_retard = 500 * new_resiliation.nombre_mois
                    new_resiliation.tva = 0.18 * (new_resiliation.redTableau + new_resiliation.frais_coupure)
                    new_resiliation.montant_ttc = new_resiliation.redTableau + new_resiliation.frais_coupure + new_resiliation.frais_retard + new_resiliation.tva
                    if new_resiliation.montant_ttc > 20000:
                        new_resiliation.timbre = 0.01 * new_resiliation.montant_ttc
                    else:
                        new_resiliation.timbre = 0
                    new_resiliation.montant_a_payer = new_resiliation.montant_ttc + new_resiliation.timbre
                new_resiliation.date_ajout = timezone.datetime.now(tz=timezone.utc)
                list_id = []
                user_id = request.user.id
                list_id.append(user_id)
                new_resiliation.user.add(*list_id)
                new_resiliation.save()

                return redirect('index')
            form = ResiliationForm
            context = {
                'form': form,
            }
            return render(request, 'scl/resiliation.html', context)

    def test_func(self):
        """
        Check if request.user is in a group
        :return: True or False
        """
        return self.request.user.groups.all()


class AjouterAffaire(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request):
        """
        Form for 'Affaires' operations
        :param request: GET
        :return: affaire.html
        """
        form = AffaireForm
        context = {
            'form': form
        }
        return render(request, 'scl/affaire.html', context)

    def post(self, request):
        """
        if form is valid, add fields excluded in AffaireForm
        :param request: POST
        if POST done
            :return: index.html
        else
            :return: affaire.html

        """
        form = AffaireForm(request.POST)
        if 'save' in request.POST:

            if form.is_valid():
                # Save form and add user and date
                new_affaire = form.save()
                new_affaire.date_ajout = timezone.datetime.now(tz=timezone.utc)
                list_id = []
                user_id = request.user.id
                list_id.append(user_id)
                new_affaire.user.add(*list_id)

                new_affaire.save()
                return redirect('index')
            form = AffaireForm
            context = {
                'form': form,
            }
            return render(request, 'scl/affaire.html', context)

    def test_func(self):
        """
        Check if request.user is in a group
        :return: True or False
        """
        return self.request.user.groups.all()


# TODO PRINT only table with information
today = datetime.today()

class SearchResiliationDashboard(UserPassesTestMixin, LoginRequiredMixin, View):
    def get(self, request):
        """
        By default Table of 'Resiliation' type operations done Today
        if request.user is a 'Caissier' show his own else show all
        check if in the GET method there are "q" like q=yyyy-mm-dd
        :param request: GET
        :return: resiliationDashboard.html
        """
        query = self.request.GET.get("q")
        
        if query is None:
            resil = resiliation.objects.filter(date_ajout__year=today.year, date_ajout__month=today.month,
                                            date_ajout__day=today.day)
        else:
            resil = resiliation.objects.filter(Q(date_ajout__icontains=query))

        nombre_resiliation = 0
        montant_total = 0
        all_resiliation = []
        user_id = request.user.id

        if request.user.groups.filter(name='Caissier'):
        
            if query is None:
                resil = resiliation.objects.filter(user=user_id,date_ajout__year=today.year, date_ajout__month=today.month,
                                            date_ajout__day=today.day)
            else:
                query_date_filter = datetime.strptime(query, "%Y-%m-%d")
                resil = resiliation.objects.filter(
                    Q(date_ajout__year=query_date_filter.year) &
                    Q(date_ajout__month=query_date_filter.month) &
                    Q(date_ajout__day=query_date_filter.day) &
                    Q(user=user_id))

            for name in resil:
                added_by = [user.username for user in User.objects.filter(resiliation=name)]
                montant_total += name.montant_a_payer
                nombre_resiliation += 1
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
                montant_total += name.montant_a_payer
                nombre_resiliation += 1
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

        all_resiliation.sort(key=lambda item: item['date_ajout'], reverse=True)

        context = {
            'resiliation': all_resiliation,
            'nombre_resiliation': nombre_resiliation,
            'montant_total': montant_total
        }

        return render(request, 'scl/resiliationDashboard.html', context)

    def test_func(self):
        """
        Check if request.user is in a group
        :return: True or False
        """
        return self.request.user.groups.all()


class SearchAffaireDashboard(View):
    def get(self, request):
        """
        By defqult Table of 'Affaire' type operations done Today
        if request.user is a 'Caissier' show his own else show all
        check if in the GET method there are "q" like q=yyyy-mm-dd
        :param request: GET
        :return: affaireDashboard.html
        """
        query = self.request.GET.get("q")

        if query is None:
            aff = affaire.objects.filter(date_ajout__year=today.year, date_ajout__month=today.month,
                                            date_ajout__day=today.day)
        else:
            aff = affaire.objects.filter(Q(date_ajout__icontains=query))
            
        nombre_affaire = 0
        montant_total = 0
        all_affaire = []
        user_id = request.user.id

        if request.user.groups.filter(name='Caissier'):
            if query is None:
                aff = affaire.objects.filter(user=user_id,date_ajout__year=today.year, date_ajout__month=today.month,
                                            date_ajout__day=today.day)
            else:
                query_date_filter = datetime.strptime(query, "%Y-%m-%d")
                aff = affaire.objects.filter(
                    Q(date_ajout__year=query_date_filter.year) &
                    Q(date_ajout__month=query_date_filter.month) &
                    Q(date_ajout__day=query_date_filter.day) &
                    Q(user=user_id))

            for case in aff:
                montant_total += case.montant
                nombre_affaire += 1
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
                montant_total += case.montant
                nombre_affaire += 1
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
        all_affaire.sort(key=lambda item: item['date_ajout'], reverse=True)
        context = {
            'montant_total': montant_total,
            'affaire': all_affaire,
            'nombre_affaire': nombre_affaire
        }

        return render(request, 'scl/affaireDashboard.html', context)

    def test_func(self):
        """
        Check if request.user is in a group
        :return: True or False
        """
        return self.request.user.groups.all()


class SearchManuelDashboard(View):
    def get(self, request):
        """
        By default table of 'Manuel' type operations done Today
        if request.user is a 'Caissier' show his own else show all
        check if in the GET method there are "q" like q=yyyy-mm-dd
        :param request: GET
        :return: manuelDashboard.html
        """
        query = self.request.GET.get("q")
        if query is None:
            encaissement = manuel.objects.filter(date_ajout__year=today.year, date_ajout__month=today.month,
                                            date_ajout__day=today.day)
        else:
            encaissement = manuel.objects.filter(Q(date_ajout__icontains=query))

        nombre_manuel = 0
        montant_total = 0
        all_manuel = []
        user_id = request.user.id
        if request.user.groups.filter(name='Caissier'):
            if query is None:
                encaissement = manuel.objects.filter(user=user_id,date_ajout__year=today.year, date_ajout__month=today.month,
                                            date_ajout__day=today.day)
            else:
                query_date_filter = datetime.strptime(query, "%Y-%m-%d")
                encaissement = manuel.objects.filter(
                    Q(date_ajout__year=query_date_filter.year) &
                    Q(date_ajout__month=query_date_filter.month) &
                    Q(date_ajout__day=query_date_filter.day) &
                    Q(user=user_id))

            for manu in encaissement:
                added_by = [user.username for user in User.objects.filter(manuel=manu)]
                nombre_manuel += 1
                montant_total += manu.montant
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
                added_by = [user.username for user in User.objects.filter(manuel=manu)]
                nombre_manuel += 1
                montant_total += manu.montant
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
        all_manuel.sort(key=lambda item: item['date_ajout'], reverse=True)
        context = {
            'manuel': all_manuel,
            'nombre_manuel': nombre_manuel,
            'montant_total': montant_total
        }
        return render(request, 'scl/manuelDashboard.html', context)

    def test_func(self):
        """
        Check if request.user is in a group
        :return: True or False
        """
        return self.request.user.groups.all()

class SearchDashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request):
        """
        summarizes the total daily amount of each operator with the different operations as a heading
        check if in the GET method there are "q" like q=yyyy-mm-dd
        :param request: GET
        :return: dashboard.html
        """
        query = self.request.GET.get("q")

        montants = []
        montant_resiliation = 0
        montant_affaire = 0
        montant_manuel = 0

        user_id = [user.id for user in User.objects.all()]

        for name in user_id:
            user = User.objects.get(id=name)
            if user.groups.filter(name='Caissier'):
                if query is None:
                    encaissement = manuel.objects.filter(user=name, date_ajout__year=today.year,
                                                     date_ajout__month=today.month, date_ajout__day=today.day)
                    aff = affaire.objects.filter(user=name, date_ajout__year=today.year, date_ajout__month=today.month,
                                                date_ajout__day=today.day)
                    resil = resiliation.objects.filter(user=name, date_ajout__year=today.year,
                                                   date_ajout__month=today.month, date_ajout__day=today.day)

                else:
                    query_date_filter = datetime.strptime(query, "%Y-%m-%d")
                    encaissement = manuel.objects.filter(user=name, date_ajout__year=query_date_filter.year,
                                                        date_ajout__month=query_date_filter.month,
                                                        date_ajout__day=query_date_filter.day)
                    aff = affaire.objects.filter(user=name, date_ajout__year=query_date_filter.year,
                                                date_ajout__month=query_date_filter.month,
                                                date_ajout__day=query_date_filter.day)
                    resil = resiliation.objects.filter(user=name, date_ajout__year=query_date_filter.year,
                                                    date_ajout__month=query_date_filter.month,
                                                   date_ajout__day=query_date_filter.day)

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
                montant_manuel = 0
                montant_resiliation = 0
                montant_affaire = 0
        context = {
            'montants': montants,
        }

        return render(request, 'scl/dashboard.html', context)

    def test_func(self):
        """
        Check if request.user is in 'Admin'
        :return: True or False
        """
        return self.request.user.groups.filter(name='Admin')


class UpdateResiliation(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk):
        """
        Retrieve information from an operation using its id
        :param request: GET
        :param pk: id_resiliation
        :return: update-resiliation.html
        """
        resil = resiliation.objects.get(pk=pk)
        if request.user.groups.filter(name='Admin'):
            form = ResiliationForm(instance=resil)
            return render(request, 'scl/update-resiliation.html', {'form': form})

    def post(self, request, pk):
        """
        check name in button update or delete operation by his id
        :param request: POST
        :param pk: id_resiliation
        :return: redirect to resiliationDashboard.html
        """
        new_resiliation = resiliation.objects.get(pk=pk)
        form = ResiliationForm(request.POST or None, instance=new_resiliation)

        if 'update' in request.POST:
            if form.is_valid():
                new_resiliation = form.save()
                new_resiliation.redTableau = 429 * new_resiliation.nombre_mois
                if new_resiliation.nombre_mois > 0:
                    new_resiliation.is_paid = True
                    new_resiliation.frais_coupure = 2000
                    new_resiliation.frais_retard = 500 * new_resiliation.nombre_mois
                    new_resiliation.tva = 0.18 * (new_resiliation.redTableau + new_resiliation.frais_coupure)
                    new_resiliation.montant_ttc = new_resiliation.redTableau + new_resiliation.frais_coupure + \
                                                  new_resiliation.frais_retard + new_resiliation.tva
                    if new_resiliation.montant_ttc > 20000:
                        new_resiliation.timbre = 0.01 * new_resiliation.montant_ttc
                    else:
                        new_resiliation.timbre = 0
                    new_resiliation.montant_a_payer = new_resiliation.montant_ttc + new_resiliation.timbre
                new_resiliation.save()
        elif 'delete' in request.POST:
            new_resiliation.delete()

        return redirect('resiliationDashboard')

    def test_func(self):
        """
        Check if request.user is in 'Admin'
        :return: True or False
        """
        return self.request.user.groups.filter(name='Admin')


class UpdateAffaire(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk):
        """
        Retrieve information from an operation using its id
        :param request: GET
        :param pk: id_affaire
        :return: update-affaire.html
        """
        aff = affaire.objects.get(pk=pk)
        form = AffaireForm(instance=aff)
        context = {
            'form': form
        }
        return render(request, 'scl/update-affaire.html', context)

    def post(self, request, pk):
        """
        check name in button update or delete operation by his id
        :param request: POST
        :param pk: id_affaire
        :return: redirect to affaireDashboard.html
        """
        new_affaire = affaire.objects.get(pk=pk)
        form = AffaireForm(request.POST or None, instance=new_affaire)
        if 'update' in request.POST:

            if form.is_valid():
                new_affaire.save()
        elif 'delete' in request.POST:
            new_affaire.delete()

        return redirect('affaireDashboard')

    def test_func(self):
        """
        Check if request.user is in 'Admin'
        :return: True or False
        """
        return self.request.user.groups.filter(name='Admin')


class UpdateManuel(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk):
        """
        Retrieve information from an operation using its id
        :param request: GET
        :param pk: id_manuel
        :return: update-manuel.html
        """
        manu = manuel.objects.get(pk=pk)
        form = ManuelForm(instance=manu)
        context = {
            'form': form,
        }
        return render(request, 'scl/update-manuel.html', context)

    def post(self, request, pk):
        """
        check name in button update or delete operation by his id
        :param request: POST
        :param pk: id_manuel
        :return: redirect to manuelDashboard.html
        """
        new_manuel = manuel.objects.get(pk=pk)
        form = ManuelForm(request.POST or None, instance=new_manuel)
        if 'update' in request.POST:
            if form.is_valid():
                new_manuel.save()

        elif 'delete' in request.POST:
            new_manuel.delete()

        return redirect('manuelDashboard')

    def test_func(self):
        """
        Check if request.user is in 'Admin'
        :return: True or False
        """
        return self.request.user.groups.filter(name='Admin')
