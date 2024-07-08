import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from messaging.models import ChatRoom, Message

# Defining GraphQL types for `Users`, `ChatRoom`, and `Message` models

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class ChatRoomType(DjangoObjectType):
    class Meta:
        model = ChatRoom
        fields = ("id", "name")

class MessageType(DjangoObjectType):
    class Meta:
        model = Message
        fields = ("id", "user", "chat_room", "content", "timestamp")


# Query classes to fetch data

class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    all_chat_rooms = graphene.List(ChatRoomType)
    all_messages = graphene.List(MessageType)
    chat_room_messages = graphene.List(MessageType, room_name=graphene.String(required=True))

    def resolve_all_users(root, info):
        return User.objects.all()
    
    def resolve_all_chat_rooms(root, info):
        return ChatRoom.objects.all()
    
    def resolve_all_messages(root, info):
        return Message.objects.select_related('user', 'chat_room').all()
    
    def resolve_chat_room_messages(root, info, room_name):
        try:
            room = ChatRoom.objects.get(name=room_name)
        except ChatRoom.DoesNotExist:
            return []
        return Message.objects.filter(chat_room=room).select_related('user', 'chat_room')
    
schema = graphene.Schema(query=Query)

# Mutations to create or modify data

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=False)

    def mutate(self, info, username, password, email=None):
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return CreateUser(user=user)
    
class CreateMessage(graphene.Mutation):
    message = graphene.Field(MessageType)

    class Arguments:
        username = graphene.String(required=True)
        room_name = graphene.String(required=True)
        content = graphene.String(required=True)

    def mutate(self, info, username, room_name, content):
        user = User.objects.get(username=username)
        chat_room, created = ChatRoom.objects.get_or_create(name=room_name)
        message = Message(user=user, chat_room=chat_room, content=content)
        message.save()
        return CreateMessage(message=message)
    
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_message = CreateMessage.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)