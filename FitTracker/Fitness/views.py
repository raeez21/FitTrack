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
from django.db.models import Sum
from django.utils import timezone
import json
from datetime import datetime, timedelta
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from datetime import date


def get_food_API(food_name):
    api_key = '9666665392544b19a09736838fa4bc9f'
    url = f'https://api.spoonacular.com/recipes/complexSearch?query={food_name}&addRecipeNutrition=true&apiKey={api_key}'
    response = requests.get(url)

    if response.ok:
        data = response.json()['results'][0]#json.loads(response.text)
        food_data = {"food_name":data['title'],\
                     "food_id":data["id"],
                     "carbs_per_serving" :next((nutrient['amount'] for nutrient in data['nutrition']['nutrients'] if nutrient['name'] == 'Carbohydrates'), None),
                     "fat_per_serving" : next((nutrient['amount'] for nutrient in data['nutrition']['nutrients'] if nutrient['name'] == 'Fat'), None),
                     "pro_per_serving" : next((nutrient['amount'] for nutrient in data['nutrition']['nutrients'] if nutrient['name'] == 'Protein'), None),
                     "cal_per_serving" : next((nutrient['amount'] for nutrient in data['nutrition']['nutrients'] if nutrient['name'] == 'Calories'), None)}
        return food_data
    else:
        error_data = {'error': 'Unable to retrieve recipe search results'}
        return JsonResponse(error_data, status=500)

class FoodDict:
    def __init__(self, dictionary):
        self.__dict__ = dictionary

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
        food_logs = FoodLog.objects.filter(user_profile=request.user.profile)#.select_related('food')
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(food_logs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        request.data['user_profile'] = request.user.profile.id
        food_name = request.data['food_name']
        food_data = Food.objects.filter(food_name=food_name)#.first()
        
        if food_data.exists():
            food_data = food_data.first()
            print("Found in DB")
        else:
            print("Not found in DB:, searching in API")
            food_data = get_food_API(food_name)
            food_data = FoodDict(food_data)
        request.data["food_name"]=food_data.food_name
        request.data["carbs"] = request.data['quantity']*food_data.carbs_per_serving
        request.data["calories"] = request.data['quantity']*food_data.cal_per_serving
        request.data["proteins"] = request.data["quantity"]*food_data.pro_per_serving
        request.data["fat"] = request.data["quantity"]*food_data.fat_per_serving
        request.data["food_id"] = food_data.food_id
        #print("req ddata final:",request.data)
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


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        return super().default(obj)


class Dashboard(APIView):

    fr = 0

    def get(self, request):
        
        target_water = Profile.objects.filter(user_id = request.user.profile.id).values_list('target_water_intake',flat=True).first()
        water_consumed = FoodLog.objects.filter\
                        ( user_profile_id=request.user.profile.id, 
                          food_id=0, #Food ID of Water is 0
                          date__date = timezone.now().date()
                        ).aggregate(Sum('quantity'))['quantity__sum']

                        
        # one_week_ago = datetime.now() - timedelta(weeks=1)
        # #logs = list(FoodLog.objects.filter(date__gte=one_week_ago).values('food_name', 'date', 'calories', 'proteins', 'fat', 'carbs'))
        # #json_logs = json.dumps(logs)

        #Retrieve foodlog table data for last 1 week to display the graph
        one_week_ago = timezone.now() - timedelta(days=7)
        #The below query gives a list of dict. Each dict is a summary of daily total nutrients, like that we have summary of last 7 days
        logs = FoodLog.objects.filter(user_profile_id=1, date__gte=one_week_ago).\
                values('date__date').\
                annotate(total_calories=Sum('calories'),
                        total_proteins=Sum('proteins'),
                        total_fat=Sum('fat'),
                        total_carbs=Sum('carbs'))
        #logs = FoodLog.objects.filter(date__gte=one_week_ago).values('food_name', 'calories','proteins','fat','carbs')
        logs_json = json.dumps(list(logs),cls=CustomJSONEncoder)
        data = {'target_water_intake':target_water, 'water_consumed': water_consumed,"one_week_FoodLog":logs_json}

        print("Data",data)
        return render(request, "customs/dashboard.html", {}) # {} is the data from DB to front end