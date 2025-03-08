from django.contrib import admin
from .models import Computador

@admin.register(Computador)
class ComputadorAdmin(admin.ModelAdmin):
    list_display = ('numero_serie', 'modelo', 'ano_fabricacao', 'tempo_garantia', 'data_vigencia_garantia')
    search_fields = ('numero_serie', 'modelo')

# Register your models here.
