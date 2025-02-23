from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from IA.utils import generate_qcm
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

@require_GET
def display_text(request):
    text = generate_qcm("les voiture tesla")
    return JsonResponse({'text': text})
@csrf_exempt
@require_POST
def generate_text(request):
        try:
            data = json.loads(request.body)
            prompt = data.get('prompt', '')
            if not prompt:
                return JsonResponse({'error': 'No prompt provided'}, status=400)
            text = generate_qcm(prompt)
            return JsonResponse({'result': text})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)