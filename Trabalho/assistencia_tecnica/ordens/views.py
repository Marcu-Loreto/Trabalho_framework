from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
import openai
from datetime import date, datetime
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.shortcuts import render
from .models import Computador
import csv
from django.contrib import messages
import pandas as pd
import re

def index(request):
    return render(request, 'index.html')

# ordens/views.py

def importar_computadores(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'O arquivo enviado não é um CSV válido.')
            return redirect('importar_computadores')

        df = pd.read_csv(csv_file)

        for _, row in df.iterrows():
            try:
                computador, created = Computador.objects.update_or_create(
                    numero_serie=row['numero_serie'],
                    defaults={
                        'modelo': row['modelo'],
                        'ano_fabricacao': int(row['ano_fabricacao']),
                        'tempo_garantia': row['tempo_garantia'],
                        'data_vigencia_garantia': pd.to_datetime(row['data_vigencia_garantia']).date()
                    }
                )
            except Exception as e:
                messages.error(request, f'Erro ao importar linha: {row.to_dict()}. Erro: {e}')
                continue

        messages.success(request, 'Importação concluída com sucesso.')
        return redirect('importar_computadores')

    return render(request, 'importar_computadores.html')

def exportar_computadores(request):
    queryset = Computador.objects.all().values(
        'numero_serie', 'modelo', 'ano_fabricacao', 'tempo_garantia', 'data_vigencia_garantia'
    )
    df = pd.DataFrame(list(queryset))
    df['data_vigencia_garantia'] = df['data_vigencia_garantia'].dt.strftime('%Y-%m-%d')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="computadores.csv"'
    df.to_csv(path_or_buf=response, index=False)

    return response

import re

def suporte_automatico(request):
    if request.method == 'POST':
        mensagem = request.POST.get('pergunta', '').strip()
        openai.api_key = settings.OPENAI_API_KEY

        # Tenta extrair o número de série do texto
        serial_match = re.search(r'(SN-[\w\d-]+)', mensagem, re.IGNORECASE)
        serial = serial_match.group(1) if serial_match else None

        garantia_msg = "O cliente ainda não forneceu um número de série válido."
        computador = None

        if serial:
            computador = Computador.objects.filter(numero_serie=serial).first()
            if computador:
                if computador.data_vigencia_garantia >= date.today():
                    garantia_msg = f"O cliente informou o número de série {serial}. O computador está EM GARANTIA até {computador.data_vigencia_garantia.strftime('%d/%m/%Y')}."
                else:
                    garantia_msg = f"O cliente informou o número de série {serial}. O computador está FORA DA GARANTIA desde {computador.data_vigencia_garantia.strftime('%d/%m/%Y')}."
            else:
                garantia_msg = f"O número de série {serial} não foi encontrado no sistema."

        # System prompt com status da garantia contextualizado
        system_prompt = (
            "Você é um atendente virtual de suporte técnico e é especializado em computadores e dispositivos móveis. "
            "sua missão é ajudar o cliente a resolver problemas técnicos e fornecer informações sobre garantia do computador e forneceder detalhes sobre envio do computador para a empresa. "
            "O cliente forneceu o seguinte: numero de serie e não esta em garantia. Voce deve orienta-lo a enviar o copmputador ao escritorio da empresa para realizar uma avaliaçao e orçamento. "	
            f"{garantia_msg} "
            "Se não tiver o número de série ou se precisar de mais informações, solicite ao cliente de maneira cordial."
        )

        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": mensagem}
                ],
                max_tokens=300,
                temperature=0.7
            )
            resposta_llm = response.choices[0].message.content

            return JsonResponse({"resposta": resposta_llm})

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return JsonResponse({"erro": f"Falha na chamada OpenAI erro 500: {str(e)}"}, status=500)

    return JsonResponse({"info": "Envie sua mensagem para o assistente."})
