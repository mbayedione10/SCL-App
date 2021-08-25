from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

class Index(View):
    def get(self, request):
        return render(request, 'scl/index.html')