# accounts/views.py

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import SignUpSerializer, MyPageSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'detail': 'CSRF cookie set'})


class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입 성공"}, status=201)
        return Response(serializer.errors, status=400)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'non_field_errors': ['Unable to log in with provided credentials.']}, status=400)
        
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'name': user.name,
        })

class MyPageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = MyPageSerializer(request.user)
        return Response(serializer.data)
