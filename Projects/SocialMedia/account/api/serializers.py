from dataclasses import field
from rest_framework import serializers
from account.models import Account 

class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    
    class Meta:
        model = Account
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def save(self):
        user = Account(
            email= self.validated_data['email'],
            username = self.validated_data['username'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'Password must match!'})

        user.set_password(password)
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username','profile_image']
    
    def clean_email(self):
        email = self.validated_data['email'].lower()

        try:
            account = Account.objects.get(email=email)
        except Exception as e:
            return email

        raise serializers.ValidationError(f'Email {email} is already in use')

    def clean_username(self):
        username = self.validated_data['username']

        try:
            account = Account.objects.get(username=username)
        except Exception as e:
            return username

        raise serializers.ValidationError(f'Username {username} is already in use')


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id','email', 'username', 'profile_image', 'last_login']
