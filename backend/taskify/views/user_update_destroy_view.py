from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from taskify.models import User
from taskify.serializers import UserSerializer
from taskify.decorator import permission_required

class UserUpdateDestroyView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_user_by_id(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404({"Msg": "Team with the provided id does not exist"})
    
    @permission_required(['team_get_id'])
    def get(self, request, pk):
        user = self.get_user_by_id(pk=pk)
        user_ser = self.serializer_class(user)
        return Response(user_ser.data, status=status.HTTP_200_OK)

    # @permission_required(["user_edit"])
    def put(self, request, pk):
        user = self.get_user_by_id(pk=pk)
        
        user_ser = self.serializer_class(user, data=request.data, partial=True)

        if user_ser.is_valid():
            user_ser.save()
            return Response(user_ser.data, status=status.HTTP_201_CREATED)
        else:
            print(user_ser.errors)
            return Response({"Msg": "Could not update User an error occurred!"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    # @permission_required(['user_delete'])
    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"Msg": "User with the provided id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        user.delete()

        return Response({"Msg": "User Deleted Successfully"}, status=status.HTTP_200_OK)