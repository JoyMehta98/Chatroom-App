# Syncronous code 
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self , data):
        print("Fetch")
        messages = Message.last_10_messages()
        # print(messages)
        # print(list(messages))
        content = {
            'command' : 'messages',
            'messages' : self.messages_to_json(messages)
        }
        # print("message content" , self.send_message(content))
        self.send_message(content)

    def new_message(self , data):
        print("new message")
        author = data['from']
        author_user = User.objects.filter(username = author)[0]
        print(author_user)
        print(data)
        message = Message.objects.create(
            author = author_user , content = data['message'])
        content = {
            'command' : 'new_message',
            'message' : self.message_to_json(message)
        }
        self.send_chat_message(content)


    def messages_to_json(self , messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        # print("Result in json list" , result[0])
        return result
    
    def message_to_json(self , message):
        return {
            'author' : message.author.username,
            'content' : message.content,
            'timestamp' : str(message.timestamp)
        } 

    commands = {
        'fetch_messages' : fetch_messages,
        'new_message' : new_message
    }


    def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self , close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self , text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self , data)

    def send_chat_message(self , message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self , message):
        # print('message in in send_message', message)
        # print('ccc', self.send(text_data=json.dumps(message)))
        self.send(text_data=json.dumps(message))

# Receive message from room group
    def chat_message(self, event):
        print('event' , event)
        message = event['message']
        # Send message to WebSocket
        return self.send(text_data=json.dumps(message))

# Asyncronous code
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name

#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))