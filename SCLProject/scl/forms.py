from django.db.models import fields
from django.forms import ModelForm
from .models import *

class ManuelForm(ModelForm):
    class Meta:
        model = manuel

        exclude = ['user','date_ajout']
        fields = '__all__'