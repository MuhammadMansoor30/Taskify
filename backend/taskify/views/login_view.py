from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from taskify.serializers import UserSerializer

class LoginView(APIView):
    authentication_classes = ()
    permission_classes = []
    
    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email, password=password)
        if not user:
            return Response({'msg': "Invalid Credentials"}, status=status.HTTP_404_NOT_FOUND)
        
        print("HEre")
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        user_ser = UserSerializer(user)

        response = Response({
            "Msg": "Login Success",
            "User": user_ser.data
        }, status=status.HTTP_200_OK)
        
        response.set_cookie('access_token', access_token, httponly=False, secure=False)
        response.set_cookie('refresh_token', str(refresh), httponly=False, secure=False)

        return response
        