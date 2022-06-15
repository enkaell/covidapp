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


class LoginView(APIView):

    def get(self, request):
        try:
            request.query_params.dict()['username']
        except KeyError:
            return Response("Не введено имя пользователя")
        username = request.query_params.dict()['username']
        password = secrets.token_urlsafe(10)
        try:
            User.objects.create_user(username=username, password=password)
        except IntegrityError:
            return Response("Данное имя пользователя уже занято")
        return Response({"username": username, "password": password})

    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']
        except KeyError:
            return Response("Не введено имя пользователя или пароль")
        try:
            user = authenticate(username=username, password=password)
        except User.DoesNotExist:
            return Response("Неправильно введены данные")
        if user:
            token = Token.objects.get_or_create(user=user)[0].key
            login(request, user)
            return Response({"token": token}, status=status.HTTP_200_OK)
        else:
            return Response("Данной учетной записи не существует")


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
            return Response("Записи не существует")
        return Response(serializer.data)

    def post(self, request):
        try:
            first_name = request.data['first_name']
            second_name = request.data['second_name']
            last_name = request.data['last_name']
            sex = request.data['sex']
            age = request.data['age']
            diagnosis = request.data['diagnosis']
            comment = request.data['comment']
        except KeyError:
            return Response("Данные не введены")
        try:
            UserCard.objects.create(first_name=first_name, second_name=second_name, last_name=last_name, sex=sex, age=age,
                        diagnosis=diagnosis, comment=comment, user_id=request.user.id)
        except IntegrityError:
            return Response("Данные уже существуют")
        return Response("Данные сохранены")

    def put(self, request):
        recs, created = UserCard.objects.update_or_create(user_id=request.user.id, defaults=request.data)
        recs.save()
        return Response("Данные обновлены")

class DailyDictView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        res = []
        try:
            record = DailyDictionary.objects.filter(user=request.user.pk)
        except:
            return Response("Записей не существует")
        if len(record) > 1:
            for i in record:
                res.append(DailyDictSerializer(i).data)
            return Response(res)
        else:
            return Response(record.data)
