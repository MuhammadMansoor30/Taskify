from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from taskify.models import Task
from taskify.serializers import TaskSerializer
from taskify.decorator import permission_required

class TaskUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_task_by_id(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404({"Msg": "Task for the provided id does not exist!"})
    
    @permission_required(['task_get_id'])
    def get(self, request, pk):
        task = self.get_task_by_id(pk=pk)
        task_ser = TaskSerializer(task)
        return Response(task_ser.data, status=status.HTTP_200_OK)

    @permission_required(['task_edit'])
    def put(self, request, pk):
        data = request.data

        task = self.get_task_by_id(pk=pk)
        task_ser = self.serializer_class(task, data=data, partial=True)

        if task_ser.is_valid():
            task_ser.save()
            return Response(task_ser.data, status=status.HTTP_200_OK)
        else:
            print(task_ser.errors)
            return Response({"Msg": "Could Not Update task some error occured!"}, status=status.HTTP_400_BAD_REQUEST)
    
    @permission_required(['task_delete'])
    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({"Msg": "Task for the provided id does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        
        task.delete()
        return Response({"Msg": "Task deleted Successfully"}, status=status.HTTP_200_OK)
    