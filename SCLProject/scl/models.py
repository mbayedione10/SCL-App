from django.db import models
from django.contrib.auth.models import User

# Create your models here.

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


