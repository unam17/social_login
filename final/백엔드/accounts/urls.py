from django.urls import path
from .views import KakaoLoginView, KakaoCallbackView, UserProfileView

urlpatterns = [
    path('kakao/login/', KakaoLoginView.as_view(), name='kakao-login'),
    path('kakao/callback/', KakaoCallbackView.as_view(), name='kakao-callback'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]   