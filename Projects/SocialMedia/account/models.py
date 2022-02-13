from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from friend.models import FriendList
from rest_framework.authtoken.models import Token


class AccounthManager(BaseUserManager):
    
    def create_user(self, email, username, password=None):
        
        if not email:
            raise ValueError("Email is required")

        if not username:
            raise ValueError("Username is required")

        user = self.model(
            email=self.normalize_email(email),
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username = username,
            password = password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser= True
        user.save(using=self._db)
        return user
        

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', unique=True)
    username= models.CharField(max_length=50, unique=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image= models.URLField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    friend_list = models.OneToOneField(FriendList, null=True, blank=True, on_delete=models.SET_NULL, related_name='friend_list')

    objects = AccounthManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    PER_PAGE = 25

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def createFriendListReceiver(sender, instance, created=False, **kwargs):
    if created:
        FriendList.objects.get_or_create(user=instance)
    

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def createAuthToken(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

