from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated 
from taskify.models import Manager, User, Role
from taskify.serializers import ManagerSerializer, UserSerializer
from taskify.decorator import permission_required

class ManagerListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ManagerSerializer

    @permission_required(['manager_get'])
    def get(self, *args, **kwargs):
        manager = Manager.objects.all()
        serializer = self.serializer_class(manager, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @permission_required(['manager_add'])
    def post(self, request, *args, **kwargs):
        data = request.data
        full_name = data.get('full_name')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        cnic = data.get('cnic')
        mobile_no = data.get('mobile_no')
        experience = data.get('experience')
        department = data.get('department')

        if not full_name or not username or not email or not password or not cnic or not experience:
            return Response({"Msg": "Please Provide all the required fields!"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            User.objects.get(email=email)
            return Response({"Msg": "User Already Exists!"}, status=status.HTTP_409_CONFLICT)
        except User.DoesNotExist:
            pass

        role = Role.objects.get(code_name='mng')

        user = User.objects.create_user(username=username, email=email, password=password, cnic=cnic, mobile_no=mobile_no)
        user.roles.clear()
        user.roles.add(role)
        user.save()

        manager_ser = self.serializer_class(data={'full_name': full_name,'experience': experience,'department': department}, context={"user": user})
        if manager_ser.is_valid():
            manager_ser.save()
            return Response(manager_ser.data, status=status.HTTP_201_CREATED)
        
        else:
            print(manager_ser.errors)
            return Response({"Msg": "Invalid Data Passed"}, status=status.HTTP_400_BAD_REQUEST)


# Imp Point:
# We can create a user using simple Model instance like we did it with User or we can use Serializer to create user like we did with the Manager.
# The Manager can also be created like the way user is craeted but for practice purpose I have used Serializer here.
# Passing the user as a context is becuase we dont require user field in seriaalizer so it will be added explicitly using the serializer. If we had the user field then we would pass the user as data.