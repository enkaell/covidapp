from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import secrets
from django.db import IntegrityError
from django.contrib.auth import authenticate
from .serializers import *
from .models import *
from rest_framework import permissions
from django.contrib.auth import login, logout


def get(request):
    try:
        request.query_params.dict()['username']
    except KeyError:
        return Response("Не введено имя пользователя", status=status.HTTP_400_BAD_REQUEST)
    username = request.query_params.dict()['username']
    password = secrets.token_urlsafe(10)
    user = authenticate(username=username, password=password)
    login(request, user)
    try:
        User.objects.create_user(username=username, password=password)
    except IntegrityError:
        return Response("Данное имя пользователя уже занято", status=status.HTTP_400_BAD_REQUEST)
    return Response({"username": username, "password": password})


class LoginView(APIView):

    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']
        except KeyError:
            return Response("Не введено имя пользователя или пароль", status=status.HTTP_400_BAD_REQUEST)
        try:
            user = authenticate(username=username, password=password)
        except User.DoesNotExist:
            return Response("Неправильно введены данные", status=status.HTTP_400_BAD_REQUEST)
        if user:
            token = Token.objects.get_or_create(user=user)[0].key
            login(request, user)
            return Response({"token": token}, status=status.HTTP_200_OK)
        else:
            return Response("Данной учетной записи не существует", status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def get(self, request):
        logout(request)
        try:
            request.user.auth_token.delete()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserCardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            record = UserCard.objects.get(user_id=request.user.pk)
            serializer = UserCardSerializer(record)
        except:
            return Response("Записи не существует", status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)


class DailyDictView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        res = []
        try:
            record = DailyDictionary.objects.filter(user=request.user.pk)
        except:
            return Response("Записей не существует", status=status.HTTP_400_BAD_REQUEST)
        if len(record) > 1:
            for i in record:
                res.append(DailyDictSerializer(i).data)
            return Response(res)
        else:
            return Response(record.data)
