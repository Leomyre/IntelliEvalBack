from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from IA.utils import generate_qcm
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json




@csrf_exempt
@require_POST
def generate_text(request):
        try:
            data = json.loads(request.body)
            prompt = data.get('prompt', '')
            if not prompt:
                return JsonResponse({'error': 'No prompt provided'}, status=400)
            print(prompt)
            text = generate_qcm(prompt)
            try:
                
                text = text.split('{', 1)[-1].rsplit('}', 1)[0]
                text_json = json.loads(f'{{{text}}}')
                return JsonResponse( text_json)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Generated text is not valid JSON'}, status=500)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
@csrf_exempt
@require_POST
def evaluate_response(request):
        try:
            data = json.loads(request.body)
            response = data.get('response', '')
            if not response:
                 return JsonResponse({'error': 'No response provided'}, status=400)
                
                # Placeholder for evaluation logic
                # score = evaluate(response)
            score = 0  # Replace with actual evaluation logic
                
            return JsonResponse({'score': score})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)