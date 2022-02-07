from operator import mod
from pyexpat import model
from django.db import models
from django.conf import settings
from django.utils import timezone

class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='friends')

    def __str__(self):
        return self.user.username

    def addFriend(self, account):
        if not account in self.friends.all():
            self.friends.add(account)

    def removeFriend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removedAccount):
        friendsList = self # person unfriending
        friendsList.removeFriend(removedAccount)
        opponentFriendsList = FriendList.objects.get(user=removedAccount)
        opponentFriendsList.removeFriend(self.user)

    def isMutualFriend(self, friend):
        if friend in self.friends.all():
            return True
        return False


class FriendRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver')
    is_active = models.BooleanField(blank=True, null=False, default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        receiverFriendList = FriendList.objects.get(user=self.receiver)
        if receiverFriendList:
            receiverFriendList.addFriend(self.sender)
            senderFriendList = FriendList.objects.get(user=self.sender)
            if senderFriendList:
                senderFriendList.addFriend(self.receiver)
                self.is_active=False
                self.save()
    
    def decline(self):
        self.is_active=False
        self.save()

    def cancel(self):
        self.is_active=False
        self.save()
