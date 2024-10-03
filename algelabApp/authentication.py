from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        jwt_token = request.COOKIES.get('jwt_token')

        if jwt_token is None:
            return None

        try:
            validated_token = self.get_validated_token(jwt_token)
            user = self.get_user(validated_token)
            return (user, validated_token)
        except Exception:
            return None
