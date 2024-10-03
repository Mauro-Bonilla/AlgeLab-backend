from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import InvalidToken

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        User = get_user_model()
        jwt_token = request.COOKIES.get('jwt_token')

        if jwt_token:
            try:
                jwt_auth = JWTAuthentication()
                validated_token = jwt_auth.get_validated_token(jwt_token)
                request.user = jwt_auth.get_user(validated_token)
            except InvalidToken:
                # Token is invalid
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()
