import json

from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
# Create your views here.

@csrf_exempt
def user_login(request):
    status_code = 200
    msg = ""
    data = dict()
    csrf_token = None
    if request.method == "POST":
        request_data = json.loads(request.body)

        print(request_data)

        username = request_data.get("username")
        password = request_data.get("password")

        if username and password:
            user = authenticate(request=request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                status_code = 200
                msg = "User logged-in Successfully"
                if request.user.is_authenticated:
                    csrf_token = get_token(request)
            else:
                status_code = 409
                msg = "Invalid email or password"
        else:
            msg = "User information missing"
    else:
        status_code = 400  # bad request
        msg = "Invalid Request by client"

    data["msg"] = msg
    data['csrf_token'] = csrf_token

    return JsonResponse(data=data, status=status_code)


def user_logout(request):
    status_code = 200
    msg = ""
    data = dict()

    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
            msg = "User logged-out successfully"
        else:
            status_code = 404
            msg = "User not found"
    else:
        status_code = 400
        msg = "Invalid Request by client"

    data["msg"] = msg

    return JsonResponse(data=data, status=status_code)

@csrf_exempt
def user_signup(request):
    status_code = 200
    msg = ""
    data = dict()
    if request.method == "POST":
        request_data = json.loads(request.body)

        username = request_data.get("username")
        email = request_data.get("email")
        password = request_data.get("password")

        if username and email and password:
            if not User.objects.filter(username=username).exists():
                user = User(email=email, username=username)
                user.set_password(password)
                user.save()
                status_code = 201
                msg = "User created Successfully"
            else:
                status_code = 409
                msg = "User already exists"
        else:
            msg = "User information missing"
    else:
        status_code = 400  # bad request
        msg = "Invalid Request by client"
    
    data["msg"] = msg

    return JsonResponse(data=data, status=status_code)
