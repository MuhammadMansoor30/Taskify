from django.http import Http404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from taskify.models import Manager
from taskify.serializers import ManagerSerializer
from taskify.decorator import permission_required

class ManagerUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ManagerSerializer

    def get_manager_by_id(self, pk):
        try:
            return Manager.objects.get(pk=pk)
        except Manager.DoesNotExist:
            raise Http404({"Msg": "Manager with the given id does not exist!"})

    @permission_required(['manager_get'])
    def get(self, request, pk):
        manager = self.get_manager_by_id(pk=pk)
        manager_ser = ManagerSerializer(manager)
        return Response(manager_ser.data, status=status.HTTP_200_OK)

    @permission_required(['manager_edit'])
    def put(self, request, pk):
        manager = self.get_manager_by_id(pk=pk)
        manager_ser = self.serializer_class(manager, data=request.data, partial=False)   # Format for Update: 'Obj to update', 'New Data to update with', 'patially update or full'
        
        if manager_ser.is_valid():
            manager_ser.save()
            return Response(manager_ser.data, status=status.HTTP_200_OK)
        else:
            print(manager_ser.errors)
            return Response({"Msg": "Errors Updating Manager!"}, status=status.HTTP_400_BAD_REQUEST)
    
    @permission_required(['manager_delete'])
    def delete(self, request, pk):
        try:
            manager = Manager.objects.get(pk=pk)
        except Manager.DoesNotExist:
            return Response({"Msg": "Manager with the given id does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        
        manager.user.delete()  # Deletes the associated user with the manager
        manager.delete()       # Deletes the manager itself

        return Response({"Msg": "Manager Deleted Sucessfully"}, status=status.HTTP_200_OK)