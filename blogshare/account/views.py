from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section':'dashboard'})
