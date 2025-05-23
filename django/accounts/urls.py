from django.urls import path
from .views import SignUpView,  MyPageView, CustomAuthToken, get_csrf_token
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/get-csrf-token/', get_csrf_token, name='get_csrf_token'),
    path('api/signup/', SignUpView.as_view(), name='signup'),
    path('api/login/', CustomAuthToken.as_view(), name='login'),
    path('api/mypage/', MyPageView.as_view(), name='mypage')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
