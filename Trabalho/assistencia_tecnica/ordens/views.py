from django.shortcuts import render
from django.http import JsonResponse
import requests

def index(request):
    return render(request, 'index.html')

def suporte_automatico(request):
    """
    Exemplo de chamada a uma API de LLM já treinada.
    """
    if request.method == 'POST':
        pergunta = request.POST.get('pergunta')
        
        # Exemplo genérico de chamada a uma API
        # Ajuste a URL e parâmetros para a API real
        api_url = "https://api.minha-llm.com/chat"
        payload = {
            "prompt": pergunta,
            "max_tokens": 100
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer SEU_TOKEN_DE_API"
        }
        
        response = requests.post(api_url, json=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            resposta_llm = data.get('answer', 'Sem resposta da LLM.')
            return JsonResponse({"resposta": resposta_llm})
        else:
            return JsonResponse({"erro": "Não foi possível obter resposta da LLM."}, status=400)
    
    return JsonResponse({"info": "Use o método POST para enviar a pergunta."})

# ordens/views.py
import openai
from datetime import date
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render
from .models import Computador

def suporte_automatico(request):
    if request.method == 'POST':
        pergunta = request.POST.get('pergunta', '')
        serial = request.POST.get('serial', '')

        # Configure a chave da API
        openai.api_key = settings.OPENAI_API_KEY

        # Verifica se o computador com esse número de série existe
        computador = Computador.objects.filter(numero_serie=serial).first()

        # Define se o cliente tem garantia em dia
        garantia_dia = False
        if computador:
            if computador.data_vigencia_garantia >= date.today():
                garantia_dia = True

        # Monta a mensagem de sistema (prompt) com base na garantia
        if garantia_dia:
            system_prompt = (
                "Você é um atendente de assistência técnica de computadores. "
                "O cliente possui uma máquina com garantia em dia. "
                "Forneça dicas de Nível 1 e também dicas de Nível 2. "
                "As dicas de Nível 2 podem incluir procedimentos mais avançados, "
                "diagnóstico de hardware, reinstalação de drivers, etc."
            )
        else:
            system_prompt = (
                "Você é um atendente de assistência técnica de computadores. "
                "Forneça apenas dicas de Nível 1 (básicas), pois o cliente não "
                "possui garantia em dia ou não foi localizado no sistema. "
                "Não ofereça dicas de Nível 2. "
                "As dicas de Nível 1 podem incluir: reiniciar a máquina, verificar "
                "cabos, atualizar o sistema operacional, etc."
            )

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": pergunta}
                ],
                max_tokens=300,
                temperature=0.7
            )
            resposta_llm = response.choices[0].message["content"]
            return JsonResponse({"resposta": resposta_llm})

        except Exception as e:
            return JsonResponse({"erro": f"Falha na chamada OpenAI: {str(e)}"}, status=500)

    # Se não for POST, retorna instrução
    return JsonResponse({"info": "Use o método POST para enviar a pergunta."})
