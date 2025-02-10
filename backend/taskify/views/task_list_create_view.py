from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from taskify.models import Task, Team, User
from taskify.serializers import TaskSerializer
from taskify.decorator import permission_required

class TaskListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    @permission_required(['tasks_get'])
    def get(self, *args, **kwargs):
        tasks = Task.objects.all()
        task_ser = self.serializer_class(tasks, many=True)
        return Response(task_ser.data, status=status.HTTP_200_OK)
    
    @permission_required(['task_add'])
    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user

        try:
            Team.objects.get(id=data.get('team'))
        except Team.DoesNotExist:
            return Response({"Msg": "The Team for the provided Id does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        
        assigned_to = data.get("assigned_to")
        if assigned_to:
            try:
                User.objects.get(id=assigned_to)
            except User.DoesNotExist:
                return Response({"Msg": "The User assigned the current task does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        
        task_data = {"title": data.get('title'),
                     "description": data.get('description'),
                     "team": data.get('team'),
                     "is_completed": data.get('is_completed') or False,
                     "priority": data.get('priority'),
                     "assigned_to": assigned_to}

        task_ser = self.serializer_class(data=task_data, context={"created_by": user})
        if task_ser.is_valid():
            task_ser.save()
            return Response(task_ser.data, status=status.HTTP_201_CREATED)
        else:
            print(task_ser.errors)
            return Response({"Msg": "Could not add a new Task some error occured"}, status=status.HTTP_400_BAD_REQUEST)