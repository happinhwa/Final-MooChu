from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from your_app.consumers import YourConsumer

application = ProtocolTypeRouter({
    # http 프로토콜을 사용할 때는 일반적인 뷰를 처리하는 라우터
    'http': get_asgi_application(),
    # 웹 소켓 프로토콜을 사용할 때는 URLRouter를 사용하여 컨슈머와 연결
    'websocket': URLRouter([
        path('ws/your_path/', YourConsumer.as_asgi()),
    ]),
})