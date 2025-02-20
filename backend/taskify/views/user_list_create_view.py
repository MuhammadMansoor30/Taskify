from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from taskify.models import User, Role
from taskify.serializers import UserSerializer, RoleSerializer
from taskify.decorator import permission_required

class UserListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    @permission_required(['users_get'])
    def get(self, *args, **kwargs):
        users = User.objects.all()   # Fetching all the users
        user_ser = UserSerializer(users, many=True)
        response_data = user_ser.data

        for user in response_data:
            user_data = User.objects.get(id=user['id'])    # Looping through each user and fetching their roles
            roles = RoleSerializer(user_data.roles.all(), many=True).data
            for role in roles:
                role.pop('code_name')
                role.pop('permissions')
            
            user['roles'] = roles   # Adding roles to user and final response as well
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    @permission_required(['user_create'])
    def post(self, request, *args, **kwargs):
        data = request.data

        if not data.get('email') or not data.get("roles") or not data.get('password') or not data.get("cnic"):
            return Response({"Msg": "Please provide all the required fields!"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            User.objects.get(email=data.get('email'))
            return Response({"Msg": "User for the Provided Email already Exists!"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            pass

        user = User.objects.create_user(username=data.get('username'), email=data.get('email'), password=data.get('password'), cnic=data.get('cnic'), mobile_no=data.get('mobile_no'))
        
        for role_name in data.get('roles'):
            role = Role.objects.get(code_name=role_name)
            user.roles.add(role)
            user.save()
        
        user_ser = self.serializer_class(user)
        return Response({"Msg": "User Addded Successfully", "Data": user_ser.data}, status=status.HTTP_201_CREATED)
        