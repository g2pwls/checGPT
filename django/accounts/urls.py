from django.urls import path
from .views import SignUpView, LoginView

urlpatterns = [
    path('register/', SignUpView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='custom_login'),
]
