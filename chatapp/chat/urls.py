from django.urls import path
from .views import chat_view, get_response

urlpatterns = [
    path('', chat_view, name='chat'),
    path('get_response/', get_response, name='get_response'),
]
