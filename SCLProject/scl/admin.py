from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.resiliation)
admin.site.register(models.affaire)
admin.site.register(models.manuel)