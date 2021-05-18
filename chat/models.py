from django.db import models
from django.conf import settings

class chatRoom(models.Model):
    title = models.CharField(max_length=255, unique=True, blank=False,)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, null=True)

    def __str__(self):
        return self.title
    
    def connectUser(self,user):
        userAdded = False
        if not user in self.users.all():
            self.users.add(user)
            self.save()
            userAdded = True
        elif user in self.users.all():
            userAdded = True
        return userAdded
    
    def disconnectUser(self, user):
        userRemoved = False
        if user in self.users.all():
            self.users.remove(user)
            self.save()
            userRemoved = True
        return userRemoved

    def chatGroup(self):
        return "chat-%s" % self.id
    
class chatManager(models.Manager):
    def byRoom(self,room):
        cqs = chatMessage.objects.filter(room=room).order_by('-timestamp')
    
class chatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(chatRoom, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    objects = chatManager()

    def __str__(self):
        return self.body
