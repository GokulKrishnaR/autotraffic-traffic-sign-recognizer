import json
import os
import uuid

import cv2
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .sign_predictor import predict_from_base64, predict_from_rgb_array


def home(request):
    context = {}
    if request.method == 'POST' and request.FILES.get('image'):
        upload_dir = settings.MEDIA_ROOT
        os.makedirs(upload_dir, exist_ok=True)
        ext = os.path.splitext(request.FILES['image'].name)[1] or '.jpg'
        filepath = os.path.join(upload_dir, f'{uuid.uuid4().hex}{ext}')
        with open(filepath, 'wb+') as dest:
            for chunk in request.FILES['image'].chunks():
                dest.write(chunk)
        img = cv2.imread(filepath)
        if img is not None:
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            result = predict_from_rgb_array(rgb)
            context['upload_prediction'] = (
                result['prediction'] or 'No sign detected (low confidence)'
            )
            if result.get('confidence') is not None:
                context['upload_confidence'] = f"{result['confidence'] * 100:.1f}"
        else:
            context['upload_prediction'] = 'Could not read image file'
        try:
            os.remove(filepath)
        except OSError:
            pass
    return render(request, 'home.html', context)


@require_POST
def predict_frame(request):
    try:
        data = json.loads(request.body)
        image_b64 = data.get('image', '')
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({'error': 'Invalid request'}, status=400)
    if not image_b64:
        return JsonResponse({'error': 'No image provided'}, status=400)
    try:
        result = predict_from_base64(image_b64)
    except FileNotFoundError:
        return JsonResponse({'error': 'Model file not found'}, status=500)
    except Exception as exc:
        return JsonResponse({'error': str(exc)}, status=500)
    if 'error' in result:
        return JsonResponse(result, status=400)
    return JsonResponse(result)
