# core/tasks.py
from celery import shared_task
import telebot
from telebot import types
from .models import GrupoVip, Plano
from django.core.exceptions import ObjectDoesNotExist
import logging

@shared_task
def process_telegram_update(bot_token, update_data):
    try:
        # Busca o GrupoVip associado ao token do bot
        grupo_vip = GrupoVip.objects.get(token_bot_conversa=bot_token)
    except ObjectDoesNotExist:
        logging.error(f"Bot com token {bot_token} não encontrado.")
        return

    # Inicializa o bot com o token fornecido
    bot = telebot.TeleBot(bot_token)
    
    # Processa a atualização: neste exemplo, lidamos apenas com o comando /start
    if 'message' in update_data:
        message = update_data['message']
        chat_id = message['chat']['id']
        text = message.get('text', '')
        if text.startswith('/start'):
            # Envia a mensagem de boas-vindas armazenada no banco
            welcome_message = grupo_vip.mensagem_boas_vindas
            bot.send_message(chat_id, welcome_message, parse_mode='Markdown')
            
            # Busca os planos cadastrados para este grupo
            planos = Plano.objects.filter(grupo_vip=grupo_vip)
            if planos.exists():
                markup = types.InlineKeyboardMarkup()
                for plano in planos:
                    # Cria o texto do botão (ex: "Plano X - R$ Y")
                    button_text = f"{plano.descricao} - R${plano.valor_original:.2f}"
                    # Usa o ID do plano para identificar a seleção no callback
                    callback_data = f"plan_{plano.id}"
                    markup.add(types.InlineKeyboardButton(button_text, callback_data=callback_data))
                
                bot.send_message(chat_id, "Escolha seu plano:", reply_markup=markup)
            else:
                bot.send_message(chat_id, "Nenhum plano disponível no momento.")
        # Outras atualizações (callbacks, etc.) podem ser processadas aqui
