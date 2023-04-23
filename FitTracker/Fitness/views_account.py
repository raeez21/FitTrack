from django.shortcuts import redirect, render, HttpResponseRedirect
from .models import Profile
from django.urls import reverse

from .serializers import ProfileSerialzer, RegisterSerializer, UserSerializer, ChangePasswordSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView

class ChangePassword(APIView):
    def patch(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # if using drf authtoken, create a new token 
        # if hasattr(user, 'auth_token'):
            # user.auth_token.delete()
        # token, created = Token.objects.get_or_create(user=user)
        # return new token
        return Response({'message': "Password Changed"}, status=status.HTTP_200_OK)


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    fr = 0
    def get(self, request):
        loggedIn = False
        message = "User not logged in"
        details = ""
        if request.user.is_authenticated:
            loggedIn = True
            message = "User is logged in"
            details = request.user.first_name + " " + request.user.last_name + " ID: " + str(request.user.id)

        data = {"err" : False, "message" : message, "data" : details , "loggedIn" : loggedIn}
        
        if self.fr == 1:
            self.fr = 0
            return render(request, "customs/signin.html", data)

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        print("DATA RECEVIED", request)

        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        login(request, user)


        print(serializer.data , user)
        
        return super(LoginAPI, self).post(request, format=None)


class AccountView(APIView):
    fr = 0
    # what kind of authentication to use. 
    # we will be using only token / session authentication
    # authentication_classes = [SessionAuthentication, BasicAuthentication] 

    def get(self, request, id=None):

        # if request.user.is_authenticated and self.fr == 1:
        #     return HttpResponseRedirect(reverse('dashboard'))

        users = []

        if id == None:
            users = User.objects.filter(is_active = True)
        else:
            users.append(User.objects.get(id = id, is_active = True))

        data = []
        for user in users:
            obj = UserSerializer(user)
            data.append(obj.data)

        data = {"status": "success" , "data" : data}
        
        if self.fr == 1:
            self.fr = 0
            return render(request, "customs/signup.html", data)
        else:
            return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request):
        print("POST", request.data, request)

        obj = User.objects.filter(email = request.data["email"])
        if len(obj) != 0:
            return Response({"statis": "error", "message" : "User with the provided email already exists" , "data" : {"message" : ["User with the provided email already exists"] }}, status=status.HTTP_400_BAD_REQUEST)

        serializer = RegisterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","message":"New Profile created successfully", "data": serializer.data, "append":True}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "message":"err", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        user = User.objects.get(id=id)
        serializer = RegisterSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","message":"user updated successfully", "data": serializer.data} , status=status.HTTP_200_OK)
        else:
            return Response({"status": "error","message":"err" ,"data": serializer.errors})
    
    def delete(self, request, id):

        user = User.objects.get(id = id)
        user.is_active = False
        user.save()
        
        serializer = UserSerializer(user).data
        
        return Response({"status": "success","message":"user deleted successfully", "data": serializer} , status=status.HTTP_200_OK)
        

class ProfileView(APIView):
    serializer_class = ProfileSerialzer
    fr = 0
    # what kind of authentication to use. 
    # we will be using only token / session authentication
    # authentication_classes = [SessionAuthentication, BasicAuthentication] 

    def get(self, request, id=None):
        profiles = []

        profiles.append( Profile.objects.get(user__id = request.user.id) )

        # if id == None:
        #     profiles = Profile.objects.filter(user__is_active = True)
        # else:
        #     profiles.append(Profile.objects.get(user__id = id, user__is_active = True))

        data = []
        for profile in profiles:
            obj = self.serializer_class(profile).data
            data.append(obj)

        data = {"status": "success" , "data" : data, "profile" : profiles[0]}

        if (self.fr == 1):
            self.fr = 0
            return render(request, "customs/settings.html" , data)
        
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, id = None):
        if id == None: 
            id = request.user.id

        profile = Profile.objects.get(user__id=id)
        serializer = self.serializer_class(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","message":"profile updated successfully", "data": serializer.data} , status=status.HTTP_200_OK)
        else:
            return Response({"status": "error","message":"err" ,"data": serializer.errors})
   
