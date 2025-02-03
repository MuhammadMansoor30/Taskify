from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from taskify.models import Permission
from taskify.serializers import PermissionSerializer

class PermissionListView(ListAPIView):
    queryset = Permission.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PermissionSerializer
