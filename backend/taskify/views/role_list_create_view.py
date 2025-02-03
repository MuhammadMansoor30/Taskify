from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from taskify.models import Role, Permission
from taskify.serializers import RoleSerializer

class RoleListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        role = Role.objects.all()
        serializer = RoleSerializer(role, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwrags):
        data = request.data
        user = request.user
        name = data.get('name', None)
        code_name = data.get('code_name', None)
        permissions = data.get('permissions', None)
        perm_lst = []

        if name is None or code_name is None or permissions is None:
            return Response({"msg": "Fields Cannot be None. Provide name, code_name and permissions"}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            for permission in permissions:
                print(permission)
                try:
                    perm = Permission.objects.get(id=permission)
                    perm_lst.append(perm)
                    print(permission)
                    print(perm_lst)
                except Permission.DoesNotExist:
                    raise Exception("Invalid Permission")

            role = Role.objects.create(name = name, code_name = code_name, created_by=user)
            role.permissions.clear()
            role.permissions.add(*perm_lst)
            role.save()

            role_ser = RoleSerializer(role)

            return Response(role_ser.data, status=status.HTTP_201_CREATED)
        
