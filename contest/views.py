from multiprocessing import context
from pickle import TRUE
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from rest_framework import status
from django.http import JsonResponse
from classes.models import Class, Class_user
from account.models import User
from .models import Contest, Exam
from . import serializers

# Create your views here.

class ContestView(APIView):
    #permission_classes = [IsAdminUser]

    def get_object(self, class_id):
        classid = generics.get_object_or_404(Class, id = class_id)
        return classid

    def post(self,request):
        data = request.data
        
        Create_Class = Class(name=data['name'], year=data['year'], semester=data['semester'], created_user=request.user)
        Create_Class.save()

        print(Create_Class.id)
        # 교수 본인 추가
        data = {}
        data['username'] = request.user
        data['privilege'] = 2
        data["is_show"] = True
        data["class_id"] = Create_Class.id
        serializer = serializers.Class_user_Serializer(data=data) #Request의 data를 UserSerializer로 변환
            
        if serializer.is_valid():
            serializer.save() #UserSerializer의 유효성 검사를 한 뒤 DB에 저장
            user = Class_user.objects.filter(username = request.user).filter(class_id = Create_Class.id)
            Create_Class.users.add(user[0])

        return Response(serializers.ClassSerializer(Create_Class).data, status=status.HTTP_201_CREATED) #client에게 JSON response 전달
        
    def get(self, request, **kwargs):
        if kwargs.get('class_id') is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            class_id = kwargs.get('class_id')
            classid = self.get_object(class_id)
            class_list_serializer = serializers.ClassSerializer(Class.objects.get(id=class_id))
            return Response(class_list_serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, **kwargs):
        if kwargs.get('class_id') is None:
            return Response("Fail", status=status.HTTP_400_BAD_REQUEST)
        else:
            class_id = kwargs.get('class_id')
            classid = self.get_object(class_id)

            data = request.data
            user = Class.objects.get(id=class_id)
            if user.created_user == request.user:
                user.name = data["name"]
                user.year = data["year"]
                user.semester = data["semester"]
                user.save(force_update=True)
                class_list_serializer = serializers.ClassSerializer(user)
                return Response(class_list_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("Fail", status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, **kwargs):
        if kwargs.get('class_id') is None:
            return Response("Fail", status=status.HTTP_400_BAD_REQUEST)
        else:
            class_id = kwargs.get('class_id')
            classid = self.get_object(class_id)

            user = Class.objects.get(id=class_id)
            if user.created_user == request.user:
                user.delete()
                return Response("Success", status=status.HTTP_200_OK)
            else:
                return Response("Fail", status=status.HTTP_400_BAD_REQUEST)


class ContestProblemView(APIView):
    #permission_classes = [IsAdminUser]

    def get_object(self, class_id):
        classid = generics.get_object_or_404(Class, id = class_id)
        return classid

    def get(self, request, **kwargs):
        if kwargs.get('class_id') is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            class_id = kwargs.get('class_id')
            classid = self.get_object(class_id)
            user = Class.objects.get(id=class_id)
            datas = user.users.all()
            #print(datas)
            class_Userlist_serializer = serializers.Class_user_Get_Serializer(datas, many=True)
            #return Response(data, status=status.HTTP_200_OK)
            return Response(class_Userlist_serializer.data, status=status.HTTP_200_OK)

class ContestProblemInfoView(APIView):
    #permission_classes = [IsAdminUser]

    def get_object(self, class_id):
        classid = generics.get_object_or_404(Class, id = class_id)
        return classid

    def post(self,request, class_id):
        classid = self.get_object(class_id)

        # 기존 std 삭제
        user = Class.objects.get(id=class_id)
        if user.created_user == request.user:
            user_list = user.users.all()
            for users in user_list:
                if users.privilege == 0:
                    user.users.remove(users.id)
                    users.delete()

        # std 추가
        user_does_not_exist = {}
        user_does_not_exist['does_not_exist'] = []
        user_does_not_exist['is_existed'] = []
        datas = request.data
        user_add = Class.objects.get(id=class_id)
        for data in datas:
            is_check_user = User.objects.filter(username = data['username']).count()
            is_check_class_user = Class_user.objects.filter(username = data['username']).filter(class_id = class_id).count()
            if is_check_user == 0:
                user_does_not_exist['does_not_exist'].append(data['username'])
                continue
            if is_check_class_user != 0:
                user_does_not_exist['is_existed'].append(data['username'])
                continue
            
            data["is_show"] = True
            data["privilege"] = 0
            data["class_id"] = class_id
            
            serializer = serializers.Class_user_Serializer(data=data)
            
            if serializer.is_valid():
                serializer.save()
                user = Class_user.objects.filter(username = data['username']).filter(class_id = class_id)
                user_add.users.add(user[0])
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # 출력
        if (len(user_does_not_exist['does_not_exist']) == 0) and (len(user_does_not_exist['is_existed']) == 0):
            users_datas = user_add.users.all()
            class_Userlist_serializer = serializers.Class_user_Get_Serializer(users_datas, many=True)
            return Response(class_Userlist_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(user_does_not_exist, status=status.HTTP_201_CREATED)