from django.shortcuts import redirect, render
from .models import Profile, FoodLog
from .serializers import ProfileSerialzer, RegisterSerializer, FoodLogSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse




class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        login(request, user)
        
        return super(LoginAPI, self).post(request._request, format=None)


class AccountView(APIView):
    serializer_class = RegisterSerializer
    # what kind of authentication to use. 
    # we will be using only token / session authentication
    # authentication_classes = [SessionAuthentication, BasicAuthentication] 

    def get(self, request, id=None):
        # return only 1 profile
        # since id is provided
        return Response({"status": "success"}, status=status.HTTP_200_OK)
        # id = 1
        # if id:
        #     profile = get_object_or_404(Profile, id=id)
        #     serializer = self.serializer_class(profile)
            # return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        
        # # return 'pagination_class' profiles 
        # profile = Profile.objects.all()
        # page = self.paginate_queryset(profile)
        # if page is not None:
        #     # workflows = Profile.objects.filter(is_deleted=False)
        #     serializer = self.serializer_class(page, many=True)
        #     return self.get_paginated_response(serializer.data)

    
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","message":"New Profile created successfully", "data": serializer.data, "append":True}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "message":"err", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None):
        profile = Profile.objects.get(id=id)
        serializer = self.serializer_class(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","message":"Profile updated successfully", "data": serializer.data})
        else:
            return Response({"status": "error","message":"err" ,"data": serializer.errors})


#Login needed to access this view
class FoodLogView(LoginRequiredMixin, APIView):
    serializer_class = FoodLogSerializer

    def get(self, request, format=None):
        # Retrieve all the food logs for the current user

        ####TODO USE THE BELOW CODE ONCE FRONT END READY
        # user = request.user
        # user_profile = Profile.objects.get(user=user)
        # foodlogs = FoodLog.objects.filter(user_profile=user_profile)
        # foodlogs_data = []
        # for foodlog in foodlogs:
        #     foodlogs_data.append({
        #         'date': foodlog.date,
        #         'food_name': foodlog.food.name,
        #         'username': user.username,
        #     })
        # context = {
        #     'foodlogs_data': foodlogs_data,
        # }
        # return JsonResponse(context)

        ###AS A PLACEHOLDER USE This for now
        food_logs = FoodLog.objects.filter(user_profile=request.user.profile)
        serializer = self.serializer_class(food_logs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Assign the current user's profile to the food log
            serializer.validated_data['user_profile'] = request.user.profile
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)