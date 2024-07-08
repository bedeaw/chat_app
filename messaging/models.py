from django.db import models
from django.contrib.auth.models import User

"""Creating 3 user models
User: Using Djanogo's authentication framework
ChatRoom: This model represents different chat rooms. Each chat room has a unique name.
Message: This model represents the messages sent by users. Each message is linked to a
 user and a chat room and includes content and a timestamp.
 """

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content[:20]}'
