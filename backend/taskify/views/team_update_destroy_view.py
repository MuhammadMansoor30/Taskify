from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from taskify.models import Team
from taskify.serializers import TeamSerializer
from taskify.decorator import permission_required

class TeamUpdateDestroyView(APIView):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get_team_by_id(self, pk):
        try:
            return Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            raise Http404({"Msg": "Team with the provided id does not exist"})
    
    @permission_required(['team_get_id'])
    def get(self, request, pk):
        team = self.get_team_by_id(pk=pk)
        team_ser = TeamSerializer(team)
        return Response(team_ser.data, status=status.HTTP_200_OK)

    @permission_required(["team_edit"])
    def put(self, request, pk):
        team = self.get_team_by_id(pk=pk)
        
        team_ser = self.serializer_class(team, data=request.data, partial=True)

        if team_ser.is_valid():
            team_ser.save()
            return Response(team_ser.data, status=status.HTTP_200_OK)
        else:
            print(team_ser.errors)
            return Response({"Msg": "Could not update Team an error occurred!"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    @permission_required(['team_delete'])
    def delete(self, request, pk):
        try:
            team = Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            return Response({"Msg": "Team with the provided id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        team.delete()

        return Response({"Msg": "Team Deleted Successfully"}, status=status.HTTP_200_OK)