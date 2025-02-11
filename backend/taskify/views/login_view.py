from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from taskify.serializers import UserSerializer, RoleSerializer


class LoginView(APIView):
    authentication_classes = ()
    permission_classes = []

    def get_role_permissions(self, roles):
        permissions_list = []
        for role in roles:
            role_perm = role.permissions.all()
            for permission in role_perm:
                permissions_list.append(permission.code_name)
        
        return permissions_list

    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email, password=password)
        if not user:
            return Response({'msg': "Invalid Credentials"}, status=status.HTTP_404_NOT_FOUND)
        
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        user_ser = UserSerializer(user)

        response_data = user_ser.data
        roles =  RoleSerializer(user.roles.all(), many=True).data   # Getting the roles data using the serializer. 
        permissions = self.get_role_permissions(user.roles.all())   # Passing user.roles.all() to pas sthe Role object not the JSON serialized roles using roles defined above.

        for role in roles:
            role.pop('permissions')  
            
        response_data['roles'] = roles
        response_data['permissions'] = permissions

        response = Response({
            "Msg": "Login Success",
            "User": response_data
        }, status=status.HTTP_200_OK)
        

        response.set_cookie('access_token', access_token, httponly=False, secure=False)
        response.set_cookie('refresh_token', str(refresh), httponly=False, secure=False)

        return response
        