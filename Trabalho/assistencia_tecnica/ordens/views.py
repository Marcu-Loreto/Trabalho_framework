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
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import openai

def suporte_automatico(request):
    if request.method == 'POST':
        pergunta = request.POST.get('pergunta', '')

        # Configure a chave de API
        openai.api_key = settings.OPENAI_API_KEY

        try:
            # Usando a nova sintaxe openai>=1.0.0
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um assistente de suporte de TI."},
                    {"role": "user", "content": pergunta}
                ],
                max_tokens=150,
                temperature=0.7
            )
            resposta_llm = response.choices[0].message["content"]
            return JsonResponse({"resposta": resposta_llm})
        
        except Exception as e:
            return JsonResponse({"erro": f"Falha na chamada OpenAI: {str(e)}"}, status=500)

    return JsonResponse({"info": "Use o método POST para enviar a pergunta."})
