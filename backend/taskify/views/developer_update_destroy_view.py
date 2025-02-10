from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from taskify.models import Developer, Team, Manager, User, Role
from taskify.serializers import DeveloperSerializer
from taskify.decorator import permission_required

class DeveloperUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeveloperSerializer

    @permission_required({'developer_edit'})
    def put(self, request, pk):
        try:
            developer = Developer.objects.get(pk=pk)
        except Developer.DoesNotExist:
            return Response({"Msg": "Developer for the provided Id does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        
        developer_ser = self.serializer_class(developer, data=request.data, partial=True)
        if developer_ser.is_valid():
            developer_ser.save()
            return Response(developer_ser.data, status=status.HTTP_200_OK)
        else:
            print(developer_ser.errors)
            return Response({"Msg": "Could not update developer some error occured!"}, status=status.HTTP_400_BAD_REQUEST)
    
    @permission_required(["developer_delete"])
    def delete(self, request, pk):
        try: 
            developer = Developer.objects.get(pk=pk)
        except Developer.DoesNotExist:
            return Response({"Msg": "Developer for the provided Id does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        
        developer.user.delete() 
        developer.delete()
        return Response({"Msg": "Developer Deleted Successfully"}, status=status.HTTP_200_OK)
