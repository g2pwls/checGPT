from django.urls import path
from .views import SignUpView,  MyPageView, CustomAuthToken, get_csrf_token,  UserProfileView, FollowView, FollowStatusView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/get-csrf-token/', get_csrf_token, name='get_csrf_token'),
    path('api/signup/', SignUpView.as_view(), name='signup'),
    path('api/login/', CustomAuthToken.as_view(), name='login'),
    path('api/mypage/', MyPageView.as_view(), name='mypage'),
    path('api/users/<int:user_id>/profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/follow/<int:user_id>/', FollowView.as_view()),
    path('api/follow/<int:user_id>/status/', FollowStatusView.as_view()),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
