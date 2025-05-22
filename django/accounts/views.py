from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
import json

# Create your views here.
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return JsonResponse({"message": "로그인 성공", "username": user.username})
        else:
            return JsonResponse({"error": "아이디 또는 비밀번호가 일치하지 않습니다."}, status=400)
    
    return JsonResponse({"error": "POST 요청만 허용됩니다."}, status=405)