from django.shortcuts import render
from django.http import JsonResponse
from g4f.client import Client

client = Client()

def chat_view(request):
    return render(request, 'chat/chat.html')

def get_response(request):
    user_message = request.GET.get('message')
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "answer using html markup but without html, head, and other tags, just a piece of code and without ``` and dont say anything unless answer the question below: \n" + user_message}],
        web_search=False
    )
    return JsonResponse({'response': response.choices[0].message.content})
