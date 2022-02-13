from django.http import request
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView  
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter


from account.models import Account
from .pagination import AccountPagination
from .serializers import RegistrationSerializer, ProfileSerializer, AccountSerializer


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def register(request):

    serializer = RegistrationSerializer(data=request.data)
    
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        
        return Response({
            'email':user.email,
            'username':user.username, 
            'token':Token.objects.get(user=user).key
        })
        


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    try:
        user = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProfileSerializer(user)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def profileUpdate(request):
    try:
        user = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProfileSerializer(user, data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()
        
        return Response({'message':'Profile updated'})
    
    return Response({'message':'Failed'}, status.HTTP_400_BAD_REQUEST)


# Custom Login
class ObtainAuthTokenView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)

        if user:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            context = {
                'message':'Login Success',
                'id':user.id,
                'email':user.email,
                'token':token.key
            }
            return Response(context)
        else:
            context = {
                'message':'Invalid credentials',
            }
        
        return Response(context, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([])
def accountDetail(request, id):
    try:
        account = Account.objects.get(id=id)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = AccountSerializer(account)
    return Response(serializer.data)
    

class AccountList(ListAPIView):
    permission_classes=[]
    authentication_classes=[]
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    pagination_class = AccountPagination
    search_fields = ['username', 'email']
    filter_backends = [SearchFilter,OrderingFilter]
