# core/admin.py
from django.contrib import admin
from .models import GrupoVip, Plano

@admin.register(GrupoVip)
class GrupoVipAdmin(admin.ModelAdmin):
    list_display = ('nome', 'grupo_id', 'gateway_pagamento')
    search_fields = ('nome', 'grupo_id')

@admin.register(Plano)
class PlanoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'grupo_vip', 'valor_original')
    list_filter = ('grupo_vip',)
    search_fields = ('nome', 'descricao')