from account.api.serializers import AccountSerializer
from rest_framework import serializers
from account.models import Account 
from friend.models import FriendRequest



class AccountFriendRequestsSerializer(serializers.ModelSerializer):
    receiver = AccountSerializer(read_only=True)
    sender = AccountSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = '__all__'


class FriendRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendRequest
        fields = '__all__'

    def create(self, validated_data):

        friendRequests = FriendRequest.objects.filter(sender=validated_data['sender'], receiver=validated_data['receiver'])

        for req in friendRequests:
            if req.is_active:
                raise serializers.ValidationError({'message':'Already sent friend request!'})

        return FriendRequest.objects.create(**validated_data)

   