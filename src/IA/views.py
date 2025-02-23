from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from utils import generate_qcm
@require_GET
def display_text(request):
    text = generate_qcm()
    return JsonResponse({'text': text})