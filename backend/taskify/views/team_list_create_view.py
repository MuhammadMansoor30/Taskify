from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from taskify.models import Team
from taskify.serializers import TeamSerializer
from taskify.decorator import permission_required

class TeamListCreateView(APIView):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    @permission_required(['teams_get'])
    def get(self, *args, **kwargs):
        teams = Team.objects.all()
        team_ser = self.serializer_class(teams, many=True)
        return Response(team_ser.data, status=status.HTTP_200_OK)
    
    @permission_required(['team_add'])
    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        name = data.get('name')
        description = data.get('description')
        project_name = data.get('project_name')
        manager = data.get('manager')

        if not name or not manager:
            return Response({"Msg": "Please Provide required fields name and manager id!"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)    
        
        # try:
        #     manager = Manager.objects.get(id=manager_id)
        # except Manager.DoesNotExist:
        #     return Response({"Msg": "Manager for the provided Id does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        # We dont need to explictely get the Manager and then pass to serialzier rather it will automatically get the Manager obj instance using the manager id passed
        
        team_ser = self.serializer_class(data={'name': name, 'description': description, 'project_name': project_name, 'manager': manager, 'created_by': user})

        if team_ser.is_valid():
            team_ser.save()
            return Response(team_ser.data, status=status.HTTP_201_CREATED)
        else:
            print(team_ser.errors)
            return Response({"Msg": "Could Not add a new Team!"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        