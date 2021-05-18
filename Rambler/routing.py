import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack  # Django Authentication System
from django.core.asgi import get_asgi_application
import chat.routing
from chat.consumers import ChatRoomConsumer
from django import path, re_path
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Rambler.settings")

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path('chat/<room_id>', chatRoomConsumer)
            ])
        )
    )
   # "http": get_asgi_application(),
 #   'websocket': AuthMiddlewareStack(
   #     URLRouter(
   #         chat.routing.websocket_urlpatterns
    #    )
  #  ),
})
