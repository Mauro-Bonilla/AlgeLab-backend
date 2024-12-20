import logging
import requests
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import Profile

logger = logging.getLogger(__name__)
User = get_user_model()

@api_view(['GET'])
@permission_classes([AllowAny])
def github_login(request):
    github_login_url = (
        f'https://github.com/login/oauth/authorize'
        f'?client_id={settings.GITHUB_CLIENT_ID}'
        f'&redirect_uri={settings.GITHUB_REDIRECT_URI}'
        f'&scope=user'  # Optionally request specific scopes
    )
    return JsonResponse({'login_url': github_login_url})

@api_view(['GET'])
@permission_classes([AllowAny])
def github_callback(request):
    code = request.GET.get('code')
    logger.info(f"Received code from GitHub: {code}")
    
    if not code:
        return JsonResponse({"error": "No code received from GitHub"}, status=400)
    
    token_url = 'https://github.com/login/oauth/access_token'
    response = requests.post(
        token_url,
        data={
            'client_id': settings.GITHUB_CLIENT_ID,
            'client_secret': settings.GITHUB_CLIENT_SECRET,
            'code': code,
            'redirect_uri': settings.GITHUB_REDIRECT_URI,
        },
        headers={'Accept': 'application/json'}
    )
    
    logger.info(f"Full response from GitHub: {response.text}")
    
    try:
        response_data = response.json()
    except ValueError:
        logger.error(f"Failed to parse JSON response. Raw response: {response.text}")
        return JsonResponse({"error": "Invalid response from GitHub"}, status=500)
    
    access_token = response_data.get('access_token')
    
    if not access_token:
        error_description = response_data.get('error_description', 'Unknown error')
        logger.error(f"Failed to obtain access token. Error: {error_description}")
        return JsonResponse({"error": f"Failed to obtain access token: {error_description}"}, status=400)
    
    user_url = 'https://api.github.com/user'
    user_response = requests.get(
        user_url,
        headers={
            'Authorization': f'token {access_token}',
            'Accept': 'application/json'
        }
    )
    
    logger.info(f"User info response: {user_response.text}")
    
    try:
        user_data = user_response.json()
    except ValueError:
        logger.error(f"Failed to parse user info JSON. Raw response: {user_response.text}")
        return JsonResponse({"error": "Invalid user info response from GitHub"}, status=500)
    
    user, created = User.objects.get_or_create(username=user_data['login'])
    
    # Update or create user profile
    profile, _ = Profile.objects.get_or_create(user=user)
    profile.github_username = user_data['login']
    profile.save()
    
    jwt_token = create_jwt_token(user)
    
    response = redirect(settings.FRONTEND_URL + '/anh-algelab')
    response.set_cookie(
        'jwt_token',
        jwt_token,
        max_age=3600,
        httponly=True,
        secure=settings.JWT_COOKIE_SECURE,
        samesite=settings.JWT_COOKIE_SAMESITE,
        path='/',
    )
    return response

def create_jwt_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    return JsonResponse({
        'user_id': request.user.id,
        'username': request.user.username,
        'avatar_url': request.user.profile.avatar_url,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    response = JsonResponse({"message": "Successfully logged out"}, status=200)
    response.delete_cookie('jwt_token', path='/')
    return response

@api_view(['POST'])
@permission_classes([AllowAny])
def validate_token(request):
    token = request.COOKIES.get('jwt_token')
    if not token:
        return JsonResponse({"valid": False, "error": "No token provided"}, status=401)
    
    try:
        RefreshToken(token)
        return JsonResponse({"valid": True}, status=200)
    except Exception as e:
        return JsonResponse({"valid": False, "error": str(e)}, status=401)