# accounts/views.py

from django.shortcuts import redirect
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer
import requests

class KakaoLoginView(APIView):
    def get(self, request):
        kakao_auth_url = (
            f"https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={settings.KAKAO_CLIENT_ID}&redirect_uri={settings.KAKAO_REDIRECT_URI}"
        )
        return redirect(kakao_auth_url)

class KakaoCallbackView(APIView):
    def get(self, request):
        code = request.GET.get('code')
        token_url = "https://kauth.kakao.com/oauth/token"
        user_info_url = "https://kapi.kakao.com/v2/user/me"
        redirect_uri = settings.KAKAO_REDIRECT_URI
        client_id = settings.KAKAO_CLIENT_ID

        token_data = {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'code': code,
        }

        token_response = requests.post(token_url, data=token_data)
        token_json = token_response.json()
        access_token = token_json.get('access_token')

        user_info_headers = {
            'Authorization': f'Bearer {access_token}',
        }

        user_info_response = requests.get(user_info_url, headers=user_info_headers)
        user_info_json = user_info_response.json()

        kakao_id = user_info_json.get('id')
        kakao_account = user_info_json.get('kakao_account')
        profile = kakao_account.get('profile')
        name = profile.get('nickname')
        email = kakao_account.get('email')
        phone_number = kakao_account.get('phone_number', '000-0000-0000')

        user, created = User.objects.get_or_create(
            kakao_id=kakao_id,
            defaults={'name': name, 'email': email, 'phone_number': phone_number}
        )

        if not created:
            user.name = name
            user.email = email
            user.phone_number = phone_number
            user.save()

        refresh = RefreshToken.for_user(user)

        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(response_data)

class UserProfileView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
