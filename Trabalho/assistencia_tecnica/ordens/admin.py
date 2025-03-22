from django.contrib import admin
from django.urls import path
from django.utils.html import format_html
from django.shortcuts import render, redirect
from django.http import HttpResponse
from import_export.admin import ImportExportMixin
from .models import Computador
from .resources import ComputadorResource

@admin.register(Computador)
class ComputadorAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = ComputadorResource
    list_display = ('numero_serie', 'modelo', 'ano_fabricacao', 'tempo_garantia', 'data_vigencia_garantia')

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['custom_buttons'] = format_html(
            '<a class="button" href="import-csv/" style="margin-right:10px;">Import CSV</a>'
            '<a class="button" href="export-csv/" style="background-color:green; color:white;">Export CSV</a>'
        )
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.process_import_csv), name='computador-import-csv'),
            path('export-csv/', self.admin_site.admin_view(self.process_export_csv), name='computador-export-csv'),
        ]
        return custom_urls + urls

    def process_export_csv(self, request):
        dataset = self.resource_class().export()
        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="computadores.csv"'
        return response

    def process_import_csv(self, request):
        if request.method == 'POST':
            dataset = self.resource_class().get_dataset(request.FILES['csv_file'])
            self.resource_class().import_data(dataset, dry_run=False)
            self.message_user(request, 'CSV importado com sucesso!')
            return redirect('..')

        return render(request, 'admin/import_csv.html', context={})
