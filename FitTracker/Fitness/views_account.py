from django.shortcuts import redirect, render
from .models import Profile
from .serializers import ProfileSerialzer, RegisterSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        loggedIn = False
        message = "User not logged in"
        details = ""
        if request.user.is_authenticated:
            loggedIn = True
            message = "User is logged in"
            details = request.user.first_name + " " + request.user.last_name + " ID: " + str(request.user.id)

        return Response({"err" : False, "message" : message, "data" : details , "loggedIn" : loggedIn}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        login(request, user)

        print(serializer.data , user)
        
        return super(LoginAPI, self).post(request, format=None)


class AccountView(APIView):
    serializer_class = RegisterSerializer
    # what kind of authentication to use. 
    # we will be using only token / session authentication
    # authentication_classes = [SessionAuthentication, BasicAuthentication] 

    def get(self, request, id=None):
        profiles = []

        if id == None:
            profiles = Profile.objects.filter(user__is_active = True)
        else:
            profiles.append(Profile.objects.get(user__id = id, user__is_active = True))

        data = []
        for profile in profiles:
            obj = ProfileSerialzer(profile)
            data.append(obj.data)

        return Response({"status": "success" , "data" : data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","message":"New Profile created successfully", "data": serializer.data, "append":True}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "message":"err", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        user = User.objects.get(id=id)
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","message":"user updated successfully", "data": serializer.data} , status=status.HTTP_200_OK)
        else:
            return Response({"status": "error","message":"err" ,"data": serializer.errors})
    
    def delete(self, request, id):

        user = User.objects.get(id = id)
        
        serializer = RegisterSerializer(user).data
        
        user.is_active = False
        user.save()
        
        return Response({"status": "success","message":"user deleted successfully", "data": serializer} , status=status.HTTP_200_OK)
        

class ProfileView(APIView):
    serializer_class = ProfileSerialzer
    # what kind of authentication to use. 
    # we will be using only token / session authentication
    # authentication_classes = [SessionAuthentication, BasicAuthentication] 

    def get(self, request, id=None):
        profiles = []

        if id == None:
            profiles = Profile.objects.filter(user__is_active = True)
        else:
            profiles.append(Profile.objects.get(user__id = id, user__is_active = True))

        data = []
        for profile in profiles:
            obj = ProfileSerialzer(profile).data
            data.append(obj)

        return Response({"status": "success" , "data" : data}, status=status.HTTP_200_OK)

    def patch(self, request, id):
        profile = Profile.objects.get(user__id=id)
        serializer = self.serializer_class(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","message":"profile updated successfully", "data": serializer.data} , status=status.HTTP_200_OK)
        else:
            return Response({"status": "error","message":"err" ,"data": serializer.errors})
   
