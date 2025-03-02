# core/views.py
import json
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .tasks import process_telegram_update

@csrf_exempt
def telegram_webhook(request, bot_token):
    if request.method == 'POST':
        try:
            update = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return HttpResponseBadRequest("JSON inválido")
        
        # Envia a atualização para o Celery
        process_telegram_update.delay(bot_token, update)
        return HttpResponse("OK")
    return HttpResponseBadRequest("Método inválido")
