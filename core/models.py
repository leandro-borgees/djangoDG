# core/models.py
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver




class GrupoVip(models.Model):
    GATEWAY_CHOICES = [
        ('mercadopago', 'Mercado Pago'),
        ('efi', 'EFI'),
        ('pushinpay', 'PushinPay'),
    ]

    # Campos principais
    nome = models.CharField('Nome do Grupo VIP', max_length=100)
    grupo_id = models.CharField('ID do Grupo no Telegram', max_length=50, unique=True)
    token_bot_conversa = models.CharField('Token do Bot de Conversa', max_length=100)
    
    # Configurações de pagamento
    gateway_pagamento = models.CharField(
        'Gateway de Pagamento',
        max_length=20,
        choices=GATEWAY_CHOICES,
        default='mercadopago'
    )
    token_gateway = models.CharField('Token do Gateway', max_length=255)

    # Mensagens automáticas
    mensagem_boas_vindas = models.TextField('Mensagem de Boas-Vindas')
    midia_boas_vindas = models.FileField(
        'Mídia de Boas-Vindas',
        upload_to='boas_vindas/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Grupo VIP'
        verbose_name_plural = 'Grupos VIP'

class Plano(models.Model):
    grupo_vip = models.ForeignKey(
        GrupoVip,
        on_delete=models.CASCADE,
        related_name='planos',
        verbose_name='Grupo VIP'
    )
    
    # Configuração do plano
    nome = models.CharField('Nome do Plano', max_length=100)
    valor_original = models.DecimalField(
        'Valor Original',
        max_digits=10,
        decimal_places=2
    )
    valor_downsell = models.DecimalField(
        'Valor de Downsell',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    valor_remarketing = models.DecimalField(
        'Valor de Remarketing',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    
    # Duração e descrição
    duracao_dias = models.PositiveIntegerField(
        'Duração (dias)',
        validators=[MinValueValidator(1), MaxValueValidator(365)]
    )
    descricao = models.TextField('Descrição do Plano')

    # Configurações de automação
    dias_antecedencia_renovacao = models.JSONField(
        'Dias Antecedência Renovação',
        default=list,
        help_text='Ex: [5, 1] para 5 e 1 dias antes'
    )
    mensagem_renovacao = models.TextField('Mensagem de Renovação')
    duracao_downsell = models.PositiveIntegerField(
        'Duração para Downsell (dias)',
        default=3,
        help_text='Dias após inatividade para enviar downsell'
    )
    mensagem_downsell = models.TextField('Mensagem de Downsell')

    def __str__(self):
        return f"{self.nome} - {self.grupo_vip.nome}"

    def save(self, *args, **kwargs):
        # Valida limite de planos
        if self.grupo_vip.planos.count() >= 10 and not self.pk:
            raise ValidationError("Limite máximo de 10 planos por grupo VIP")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'
        ordering = ['valor_original']
