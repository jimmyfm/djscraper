from django.contrib import admin
from scraper.models import Categoria


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['codice', 'nome']
