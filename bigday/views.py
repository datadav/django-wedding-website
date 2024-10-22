from django.shortcuts import render


def informations(request):
    return render(request, 'informations.html')


def fr_informations(request):
    return render(request, 'fr/informations.html')
