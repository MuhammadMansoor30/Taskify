from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from taskify.models import WorkItem, Task
from taskify.serializers import WorkItemSerializer
from taskify.decorator import permission_required
from taskify.filters import WorkItemFilters, get_manager_or_developer

class WorkItemListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkItemSerializer
    filterset_class = WorkItemFilters

    @permission_required(['work_get'])
    def get(self, *args, **kwargs):
        manager, developer = get_manager_or_developer(self.request.user)
        
        if self.request.user.is_staff:
            workItems = WorkItem.objects.all()
        elif manager is not None:
            workItems = WorkItem.objects.filter(task__team__manager=manager) 
        elif developer is not None:
            workItems = WorkItem.objects.filter(task__team__developers=developer) 

        workItems = WorkItemFilters(self.request.GET, queryset=workItems).qs    # Gets the queryset using the query params from the url and applies filters
        workItem_ser = self.serializer_class(workItems, many=True)
        return Response(workItem_ser.data, status=status.HTTP_200_OK)

    @permission_required(['work_publish'])
    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        file = request.FILES.get('file')

        if file:
            try:
                Task.objects.get(id=data.get('task'))
            except Task.DoesNotExist:
                return Response({"Msg": "The task for the provided id does not exist!"}, status=status.HTTP_404_NOT_FOUND)
            
            workItem_data = {"name": data.get('name'),
                             "file": file,
                             "status": data.get('status') or "In Progress",
                             "is_approved": data.get('is_approved') or False,
                             "task": data.get('task')}
            
            workItem_ser = self.serializer_class(data=workItem_data, context={"added_by": user})

            if workItem_ser.is_valid():
                workItem_ser.save()
                return Response(workItem_ser.data, status=status.HTTP_201_CREATED)
            else:
                print(workItem_ser.error_messages)
                return Response({"Msg": "Could Not add work Item some error occurred!"}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response({"Msg": "File is Required for adding Work Item."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)