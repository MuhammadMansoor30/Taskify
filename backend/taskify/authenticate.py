from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

# Adding this CusomAuthtication class so that before each request we can get the access_token and validate the user before providing response.

class CustomAuthentication(JWTAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('access_token')
        try:
            validated_token = self.get_validated_token(token)
            return self.get_user(validated_token), validated_token
        except Exception:
            raise AuthenticationFailed('Invalid token.')

# class CustomAuthentication(JWTAuthentication):
#     def authenticate(self, request):
#         token = request.COOKIES.get('access_token')
#         refresh_token = request.COOKIES.get('refresh_token')
        
#         try:
#             validated_token = self.get_validated_token(token)
#             return self.get_user(validated_token), validated_token
#         except Exception:
#             if not refresh_token:
#                 raise AuthenticationFailed('Access token expired and no refresh token provided.')

#             try:
#                 refresh = RefreshToken(refresh_token)
#                 new_access_token = refresh.access_token

#                 response = Response({"msg": "Token refreshed successfully"})
#                 response.set_cookie('access_token', new_access_token, httponly=True)

#                 validated_token = self.get_validated_token(new_access_token)
#                 return self.get_user(validated_token), validated_token
#             except Exception:
#                 raise AuthenticationFailed('Invalid or expired refresh token.')
