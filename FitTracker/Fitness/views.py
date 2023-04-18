from django.shortcuts import redirect, render
from .models import Profile, FoodLog, ExerciseLog
#from .serializers import ProfileSerialzer, RegisterSerializer, FoodLogSerializerGet, FoodLogSerializerPost
from .serializers import *
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
import requests
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
import random

#Login needed to access this view
class FoodLogView(LoginRequiredMixin, APIView):
    #serializer_class = FoodLogSerializer
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FoodLogSerializerGet
        else:
            return FoodLogSerializerPost

    def get(self, request, format=None):
        # Retrieve all the food logs for the current user
        food_logs = FoodLog.objects.filter(user_profile=request.user.profile).select_related('food')
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(food_logs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        request.data['user_profile'] = request.user.profile.id
        serializer  = FoodLogSerializerPost(data=request.data)
        #serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Assign the current user's profile to the food log
            #serializer.validated_data['user_profile'] = request.user.profile
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExerciseLogView(LoginRequiredMixin, APIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ExerciseLogSerializerGet
        else:
            return ExerciseLogSerializerPost
    def get(self, request, format=None):
        # Retrieve all the exercise logs for the current user
        exercise_logs = ExerciseLog.objects.filter(user_profile=request.user.profile).select_related('exercise')
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(exercise_logs, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        request.data['user_profile'] = request.user.profile.id
        serializer  = ExerciseLogSerializerPost(data=request.data)
        #serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Assign the current user's profile to the food log
            #serializer.validated_data['user_profile'] = request.user.profile
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeasurementsLogView(LoginRequiredMixin, APIView):
    serializer_class = MeasurementsSerialzer
    def get(self, request, format=None):
        # Retrieve all the exercise logs for the current user
        M_logs = Measurements.objects.filter(user_profile=request.user.profile)
        serializer = self.serializer_class(M_logs, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        #Height in m, others in cm, weight in kg
        mutable_data = request.data.copy()
        mutable_data['user_profile'] = request.user.profile.id
        mutable_data['bmi'] = round(float(mutable_data['weight'])/(float(mutable_data['height'])**2),2) if 'height' in mutable_data and 'weight' in mutable_data else None
        mutable_data['waist_height_ratio'] = round(float(mutable_data['waist'])/(float(mutable_data['height'])*100),2) if 'height' in mutable_data and 'waist' in mutable_data else None
        mutable_data['waist_hip_ratio'] = round(float(mutable_data['waist'])/float(mutable_data['hip']),2) if 'waist' in mutable_data and 'hip' in mutable_data else None
        serializer = self.serializer_class(data = mutable_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def quotes(request):
    categories = ["health" , "inspirational"]
    category = categories[random.randint(0, len(categories) - 1)]

    url = "https://api.api-ninjas.com/v1/quotes/?category=" + category
    token = "koBCOTxY7knSZUSEgMuqjg==A7zNeVuvzNzPOHP0"

    header = {"X-Api-Key" : token}

    response = requests.get(url, headers=header)
    print(response.json())

    if response.status_code == 200:
        return Response({"err" : False, "data" : response.json()[0]}, status=status.HTTP_200_OK)
    
    return Response({"err" : True, "data" : response.json()}, status=response.status_code)



def hm(request):
    return render(request, "index.html")


class Dashboard(APIView):

    fr = 0

    def get(self, request):
        return render(request, "customs/dashboard.html", {})