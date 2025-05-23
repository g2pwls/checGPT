from django.urls import path, include
# 프로젝트 루트 urls.py
urlpatterns = [
    path('api/', include('accounts.urls')),
    path('accounts/', include('accounts.urls')),
]