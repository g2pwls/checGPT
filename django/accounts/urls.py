from django.urls import path
from .views import SignUpView, LoginView, MyPageView

urlpatterns = [
    path('api/signup/', SignUpView.as_view(), name='signup'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('mypage/', MyPageView.as_view(), name='mypage')
]
