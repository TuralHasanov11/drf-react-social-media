from django.urls import path
from django.contrib.auth import views as auth_views

from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    register, profile, profileUpdate, ObtainAuthTokenView, accountDetail,
    AccountList,
)


app_name='account_api'

urlpatterns = [
    path('accounts', AccountList.as_view(), name='list'), 
    path('register', register, name='register'), 
    path('login', ObtainAuthTokenView.as_view(), name='login'),
    path('profile', profile, name='profile'), 
    path('profile/update', profileUpdate, name='profile_update'), 
    path('accounts/<int:id>', accountDetail, name='detail'), 
]

