from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from IA.utils import generate_qcm

@require_GET
def display_text(request):
    text = generate_qcm("les voiture tesla")
    return JsonResponse({'text': text})