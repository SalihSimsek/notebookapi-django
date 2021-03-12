from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .serializers import AccountSerializer,ChangePasswordSerializer,RegistrationSerializer
from account.models import Account
from django.contrib.auth.models import User

@api_view(['POST',])
@permission_classes([])
@authentication_classes([])
def registration_view(request):
    if request.method == 'POST':
        data = {}
        email = request.data.get('email','0').lower()
        if validate_email(email) != None:
            data['error_message'] = 'That email is already in use'
            data['response'] = 'Error'
            return Response(data, status = status.HTTP_400_BAD_REQUEST)
        username = request.data.get('username','0').lower()
        if validate_username(username) != None:
            data['error_message'] = 'That username is already use'
            data['response'] = 'Error'
            return Response(data, status = status.HTTP_400_BAD_REQUEST)
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'Succesfully registered new user'
            data['email'] = account.email
            data['username'] = account.username
            data['pk'] = account.pk
            return Response(data,status=status.HTTP_200_OK)
        data = serializer.errors
        return Response(data,status=status.HTTP_400_BAD_REQUEST)

def validate_email(email):
    account = None
    try:
        account = Account.objects.get(email=email)
    except Account.DoesNotExist:
        return None
    if account != None:
        return email

def validate_username(username):
    account = None
    try:
        account = Account.objects.get(username=username)
    except Account.DoesNotExist:
        return None
    if account != None:
        return username

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def account_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = AccountSerializer(account)
        return Response(serializer.data)

@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def update_account(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = AccountSerializer(account,data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = 'Account update success'
            return Response(data=data)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

class ObtainAuthTokenView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self,request):
        context = {}

        username = request.POST.get('username')
        password = request.POST.get('password')
        account = authenticate(username=username ,password = password)
        if account:
            try:
                token = Token.objects.get(user=account)
            except Token.DoesNotExist:
                token = Token.objects.create(user=account)
            context['response'] = 'Succesfully Authenticated'
            context['pk'] = account.pk
            context['username'] = username.lower()
            context['token'] = token.key
            return Response(context,status = status.HTTP_200_OK)
        else:
            context['response'] = 'Error'
            context['error_message'] = 'Invalid Credentials'
            return Response(context,status = status.HTTP_401_UNAUTHORIZED)


class Logout(APIView):
    def get(self,request,format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = Account
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self,queryset=None):
        obj = self.request.user
        return obj
    
    def update(self,request,*args,**kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({'old_password':['Wrong Password']},status = status.HTTP_400_BAD_REQUEST)
            
            new_password = serializer.data.get('new_password')
            confirm_new_password = serializer.data.get('confirm_new_password')
            if new_password != confirm_new_password:
                return Response({'new_password':['new password must match']},status = status.HTTP_400_BAD_REQUEST)
            
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            return Response({'response':'Succesfully changed password'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)