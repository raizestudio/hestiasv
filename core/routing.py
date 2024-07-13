from django.urls import re_path

from core.consumers import ChatConsumer, CoreConsumer

websocket_urlpatterns = [
    re_path(r"ws/core", CoreConsumer.as_asgi()),
    re_path(r"ws/chat", ChatConsumer.as_asgi()),
]
