from django.urls import path

from .views import (
    AccountFriendRequestsList,
    sendFriendRequest,
    AccountFriendsList,
    removeFriend,
    updateFriendRequest,
)

app_name='friend_api'

urlpatterns = [
    path('', AccountFriendsList.as_view(), name='friends_list'),  
    path('send-request', sendFriendRequest, name='send_friend_request'),  
    path('requests', AccountFriendRequestsList.as_view(), name='friend_requests_list'),  
    path('remove', removeFriend, name='remove_friend'),  
    path('requests/<int:request_id>', updateFriendRequest, name='update_friend_request'),  
]

