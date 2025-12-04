import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Pega o usuário da conexão
        self.user = self.scope.get("user")
        
        if self.user and self.user.is_authenticated:
            # Cada usuário tem seu próprio grupo de notificações
            self.group_name = f"notifications_{self.user.id}"
            
            # Adiciona este canal ao grupo do usuário
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            
            await self.accept()
            
            # Envia mensagem de confirmação
            await self.send(text_data=json.dumps({
                'message': 'WebSocket conectado com sucesso!',
                'tipo': 'info'
            }))
        else:
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, 'user') and self.user and self.user.is_authenticated:
            # Remove este canal do grupo
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        # Pode ser usado para receber mensagens do cliente (opcional)
        pass

    # Handler para receber notificações do channel layer
    async def send_notification(self, event):
        notification = event['notification']
        
        # Envia a notificação para o WebSocket
        await self.send(text_data=json.dumps(notification))
