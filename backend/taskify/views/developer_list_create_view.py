from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from taskify.models import Developer, Team, Manager, User, Role
from taskify.serializers import DeveloperSerializer
from taskify.decorator import permission_required

class DeveloperListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeveloperSerializer

    @permission_required(['developers_get'])
    def get(self, *args, **kwargs):
        developers = Developer.objects.all()
        developer_ser = self.serializer_class(developers, many=True)
        return Response(developer_ser.data, status=status.HTTP_200_OK)
    
    @permission_required(['developer_add'])
    def post(self, request, *args, **kwargs):
        data = request.data

        if not data.get('email') or not data.get("manager") or not data.get('password') or not data.get("cnic"):
            return Response({"Msg": "Please provide all the required fields!"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        try:
            Manager.objects.get(id=data.get("manager"))
        except Manager.DoesNotExist:
            return Response({"Msg": "Manager for the provided id does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            Team.objects.get(Q(id=data.get("team")) & Q(manager_id=data.get('manager')))
        except Team.DoesNotExist:
            return Response({"Msg": "Team For Following id and manager does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            User.objects.get(email=data.get('email'))
            return Response({"Msg": "User with this email already exists!"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            pass
        
        role = Role.objects.get(code_name='dev')

        user = User.objects.create_user(username=data.get('username'), email=data.get('email'), password=data.get('password'), cnic=data.get('cnic'), mobile_no=data.get('mobile_no'))
        user.roles.clear()
        user.roles.add(role)
        user.save()

        dev_data = {"full_name": data.get('full_name'), 
                    "experience": data.get("experience"), 
                    "skill_set": data.get("skill_set"),
                    "manager": data.get("manager"), 
                    "team": data.get("team")}

        developer_ser = self.serializer_class(data=dev_data, context={"user": user})
        if developer_ser.is_valid():
            developer_ser.save()
            return Response(developer_ser.data, status=status.HTTP_201_CREATED)
        else:
            print(developer_ser.errors)
            return Response({"Msg": "Could not add a developer some error occured!"}, status=status.HTTP_400_BAD_REQUEST)
