from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from taskify.models import WorkItem,Task
from taskify.serializers import WorkItemSerializer
from taskify.decorator import permission_required
import os

class WorkItemUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkItemSerializer

    def get_workItem(self, pk):
        try:
            return WorkItem.objects.get(pk=pk)
        except WorkItem.DoesNotExist:
            raise Http404({"Msg": "Work Item for the provided id does not exist!"})

    @permission_required(['work_get'])
    def get(self, request, pk):
        workItem = self.get_workItem(pk=pk)
        workItem_ser = WorkItemSerializer(workItem)
        return Response(workItem_ser.data, status=status.HTTP_200_OK)   

    @permission_required(['work_edit'])
    def put(self, request, pk):
        workItem = self.get_workItem(pk=pk)
        
        workItem_ser = self.serializer_class(workItem, data=request.data, partial=True)
        if workItem_ser.is_valid():
            workItem_ser.save()
            return Response(workItem_ser.data, status=status.HTTP_200_OK)
        else:
            print(workItem_ser.error_messages)
            return Response({"Msg": "Could not Update Work Item some error occured!"}, status=status.HTTP_400_BAD_REQUEST)
    
    @permission_required(['work_delete'])
    def delete(self, request, pk):
        try:
            workItem = WorkItem.objects.get(pk=pk)
        except WorkItem.DoesNotExist:
            return Response({"Msg": "Work Item for the provided id does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        
        file = workItem.file
        if file: 
            file_path = f"work_files/{file}"

            if os.path.exists(file_path):
                os.remove(file_path)

        workItem.delete()
        return Response({"Msg": "Work Item deleted Successfully"}, status=status.HTTP_200_OK)


class WorkItemApproveView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkItemSerializer

    @permission_required(['approve_work'])
    def put(self, request, pk):
        try:
            workItem = WorkItem.objects.get(pk=pk)
        except WorkItem.DoesNotExist:
            return Response({"Msg": "Work Item for the provided id does not exist!"}, status=status.HTTP_404_NOT_FOUND)
    
        workItem.is_approved = True
        workItem.save()

        workItem_ser = self.serializer_class(workItem).data

        try:
            task = Task.objects.get(id=workItem_ser['task'])
        except Task.DoesNotExist:
            return Response({"Msg": "Task for the provided id does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        
        task.status = 'Approved'
        task.save()
        
        return Response({"Msg": "Approved Successfully"}, status=status.HTTP_200_OK)