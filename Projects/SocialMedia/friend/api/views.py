from django.http import request
from account.models import Account

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView 
from rest_framework.filters import SearchFilter, OrderingFilter

from friend.models import FriendList, FriendRequest
from .pagination import FriendAppPagination
from .serializers import (AccountFriendRequestsSerializer, 
                        FriendRequestSerializer,
                    )
from account.api.serializers import (AccountSerializer)


class AccountFriendsList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer
    pagination_class = FriendAppPagination
    search_fields = ['username', 'email']
    ordering_fields = ['username']
    ordering = ['username']

    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self):
        friendRequests = FriendList.objects.get(user=self.request.user)
        return friendRequests.friends.all()


class AccountFriendRequestsList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountFriendRequestsSerializer
    pagination_class = FriendAppPagination
    search_fields = ['sender__username', 'sender__email', 'receiver__username', 'receiver__email','created_at']
    ordering_fields = ['created_at']
    ordering = ['created_at']

    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self):
        isSent = self.request.GET.get('is_sent','')

        if isSent:
            return FriendRequest.objects.prefetch_related('receiver').filter(sender=self.request.user, is_active=True)
        return FriendRequest.objects.prefetch_related('sender').filter(receiver=self.request.user, is_active=True)

         
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sendFriendRequest(request):

    serializer = FriendRequestSerializer(data={'receiver':request.POST.get('receiver_id'),'sender':request.user.id})

    serializer.is_valid(raise_exception=True)
    serializer.save()
 
    return Response({'message':'Friend request has been sent', 'friend_request':serializer.data}, status.HTTP_201_CREATED)
    

    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateFriendRequest(request, request_id):

    try:
        friendRequest = FriendRequest.objects.get(id=request_id)
    except FriendRequest.DoesNotExist:
        return Response({'message':'Friend request not found'}, status.HTTP_404_NOT_FOUND)
   
    user = request.user
    operation = request.GET.get('operation','')

    if not operation or (not hasattr(friendRequest.__class__,operation)):
        return Response({'message':'Invalid operation'}, status.HTTP_400_BAD_REQUEST)
    if operation == 'accept' and friendRequest.receiver==user:
        friendRequest.accept()
    elif operation == 'decline' and friendRequest.receiver == user:
        friendRequest.decline()
    elif operation == 'cancel' and friendRequest.sender == user:
        friendRequest.cancel()
    else:
        return Response({'message':'Prohibited operation'}, status.HTTP_403_FORBIDDEN)

    return Response({'message':'Success'})
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def removeFriend(request):

    try:
        removedFriend = Account.objects.get(id=request.POST.get('receiver_id'))
    except Account.DoesNotExist:
        return Response({'message':'Failed'}, status.HTTP_404_NOT_FOUND)
   
    friendList = FriendList.objects.get(user=request.user)
    
    if friendList.unfriend(removedFriend):
        return Response({'message':'Friend has been removed'}, status.HTTP_201_CREATED)
    
    return Response({'message':'Failed'}, status.HTTP_400_BAD_REQUEST)