from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        cookies = request.COOKIES
        
        refresh_token = cookies.get('refresh_token', None)
        try:
            RefreshToken(refresh_token).blacklist()
        except TokenError as e:
            print(e)

        response = Response({"Msg": "Successfully Logged Out!"}, status=status.HTTP_200_OK)

        response.set_cookie('access_token', None)
        response.set_cookie('refresh_token', None)   # Setting cookies to None so that we remove the user tokens from the final response cookies

        return response


# To logout a user we have to blaclist the tokens and remove them from the cookies as well.
# For blacklisting we have to add "rest_framework_simplejwt.token_blacklist" to the installed apps and apply migrations. Then afterwards we can access the blacklist() method.