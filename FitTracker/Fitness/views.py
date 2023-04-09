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
import requests
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
import random

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
