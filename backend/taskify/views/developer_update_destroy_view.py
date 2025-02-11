from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from taskify.models import Developer
from taskify.serializers import DeveloperSerializer
from taskify.decorator import permission_required

class DeveloperUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeveloperSerializer

    def get_developer_by_id(self, pk):
        try:
            return Developer.objects.get(pk=pk)
        except Developer.DoesNotExist:
            raise Http404({"Msg": "Developer for the provided Id does not exist!"})
    
    @permission_required(['developers_get'])
    def get(self, request, pk):
        developer = self.get_developer_by_id(pk=pk)
        developer_ser = DeveloperSerializer(developer)
        return Response(developer_ser.data, status=status.HTTP_200_OK)

    @permission_required({'developer_edit'})
    def put(self, request, pk):
        developer = self.get_developer_by_id(pk=pk)  
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
