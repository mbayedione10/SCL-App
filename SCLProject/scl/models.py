from django.db import models
from django.contrib.auth.models import User

# Create your models here.

cpt_endommage = 'Compteur endommagé'
cheque_vide = 'Chéque vide'
fraude = 'Fraude'
surcharge = 'Surcharge'

TYPE_AFFAIRES =(
    (cpt_endommage,cpt_endommage),
    (cheque_vide,cheque_vide),
    (fraude,fraude),
    (surcharge,surcharge),
)

espece = 'Espéces'
cheque = 'Chéque'

PAYMENT_MODE = (
    (espece,espece),
    (cheque,cheque),
)

class resiliation(models.Model):
    nombreMois = models.PositiveIntegerField(null=False, default=0)
    redTableau = models.BigIntegerField(blank=True, default=0)
    frais_coupure = models.IntegerField(null=False, default=0)
    frais_retard = models.IntegerField(null=False, default=0)
    tva = models.DecimalField(null=False,decimal_places=2, default=0, max_length=20,max_digits=7)
    timbre = models.DecimalField(default=0, null=True,decimal_places=2, max_length=20,max_digits=7)
    montant_ttc = models.DecimalField(null=False,decimal_places=2, default=0, max_length=50,max_digits=7)
    montant_a_payer = models.DecimalField(null=False,decimal_places=2, default=0, max_length=50,max_digits=7)
    contrat = models.CharField(unique=True, null=False, max_length=25)
    date_ajout = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    user = models.ManyToManyField(User)

    def __str__(self) -> str:
        return super().__str__()


class affaire(models.Model):
    contrat = models.CharField(null=False, max_length=25)
    libelle_affaire = models.CharField(choices=TYPE_AFFAIRES,max_length=30, null=False, default=fraude)
    description_affaire = models.TextField(max_length=100, blank=True, null=True)
    technicien = models.CharField(max_length=50, null=True, blank=True)
    montant = models.DecimalField(null=True,decimal_places=0, default=0, max_length=50,max_digits=7)
    user = models.ManyToManyField(User)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return super().__str__()

class manuel(models.Model):
    motif_reglement = models.CharField(max_length=50,null=False)
    contrat = models.CharField(null=True,blank=True, max_length=25)
    mode_payement = models.CharField(choices=PAYMENT_MODE,max_length=30, null=True, blank=True)
    village = models.CharField(max_length=50, blank=True)
    montant = models.DecimalField(null=True,decimal_places=0, default=0, max_length=50,max_digits=7)
    user = models.ManyToManyField(User)
    date_ajout = models.DateTimeField(auto_now_add=True)
    nom_client = models.CharField(max_length=50, blank=True)
    contact_client = models.CharField(max_length=20, blank=True)

    def __str__(self) -> str:
        return super().__str__()

