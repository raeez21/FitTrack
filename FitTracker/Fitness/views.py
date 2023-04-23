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
from django.db.models import Sum,F, Max, Q
from django.utils import timezone
import json
from datetime import datetime, timedelta
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from datetime import date

#from django.db.models.functions import TruncDate

def get_food_API(food_name):
    api_key = '9666665392544b19a09736838fa4bc9f'
    url = f'https://api.spoonacular.com/recipes/complexSearch?query={food_name}&addRecipeNutrition=true&apiKey={api_key}'
    response = requests.get(url)

    if response.ok:
        #print("hi",response.json()['results'])
        if len(response.json()['results']) == 0:
            error_data = {'error':'No item found'}
            return JsonResponse(error_data,status=404)
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
        food_logs = FoodLog.objects.filter(user_profile=request.user.profile).order_by('-date')#.select_related('food')
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(food_logs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        mutable_data = request.data.copy()
        mutable_data['user_profile'] = request.user.profile.id
        food_name = mutable_data['food_name']
        food_data = Food.objects.filter(food_name__iexact=food_name)#.first()
        
        if food_data.exists():
            food_data = food_data.first()
            print("Found in DB")
        else:
            print("Not found in DB:, searching in API")
            food_data = get_food_API(food_name)
            if isinstance(food_data,JsonResponse):
                return Response(food_data.content.decode('utf-8'), status=status.HTTP_404_NOT_FOUND)
            print("Found from API")
            food_data = FoodDict(food_data)
        print("food",food_data.carbs_per_serving)
        mutable_data["food_name"]=food_data.food_name
        mutable_data["carbs"] = float(mutable_data['quantity'])*float(food_data.carbs_per_serving)
        mutable_data["calories"] = float(mutable_data['quantity'])*float(food_data.cal_per_serving)
        mutable_data["proteins"] = float(mutable_data["quantity"])*float(food_data.pro_per_serving)
        mutable_data["fat"] = float(mutable_data["quantity"])*float(food_data.fat_per_serving)
        mutable_data["food_id"] = food_data.food_id
        #print("req ddata final:",request.data)
        serializer  = FoodLogSerializerPost(data=mutable_data)
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
        exercise_logs = ExerciseLog.objects.filter(user_profile=request.user.profile).select_related('exercise').order_by('-date')
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(exercise_logs, many=True)

        exercises = Exercise.objects.all()
        exercises_data = [{'id': exercise.id, 'name': exercise.name} for exercise in exercises]

        #return Response(serializer.data)
        return Response({'exercise_logs': serializer.data, 'exercises': exercises_data})
    def post(self, request, format=None):
        mutable_data = request.data.copy()
        mutable_data['user_profile'] = request.user.profile.id
        serializer  = ExerciseLogSerializerPost(data=mutable_data)
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


def quotes():
    categories = ["health" , "inspirational"]
    category = categories[random.randint(0, len(categories) - 1)]

    url = "https://api.api-ninjas.com/v1/quotes/?category=" + category
    token = "koBCOTxY7knSZUSEgMuqjg==A7zNeVuvzNzPOHP0"

    header = {"X-Api-Key" : token}

    response = requests.get(url, headers=header)
    print(response.json())



    if response.status_code == 200:
        return False, response.json()[0]
    
    return True, response.json()



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
        user_id = request.user.profile.id
        error, quote = quotes()


        allExercises = Exercise.objects.all()
    
        target_water = Profile.objects.filter(user_id = user_id).values_list('target_water_intake',flat=True).first()
        water_consumed = FoodLog.objects.filter\
                        ( user_profile_id=user_id, 
                          food_id=0, #Food ID of Water is 0
                          date__date = timezone.now().date()
                        ).aggregate(Sum('quantity'))['quantity__sum'] or 0 
                        
        # one_week_ago = datetime.now() - timedelta(weeks=1)
        # #logs = list(FoodLog.objects.filter(date__gte=one_week_ago).values('food_name', 'date', 'calories', 'proteins', 'fat', 'carbs'))
        # #json_logs = json.dumps(logs)

        #Retrieve foodlog table data for last 1 week to display the graph
        one_week_ago = timezone.now() - timedelta(days=7)
        #The below query gives a list of dict. Each dict is a summary of daily total nutrients, like that we have summary of last 7 days
        #as of now, only the calorie value is used in dashboard, if other nutrients needed uncomment the below lines
        logs = FoodLog.objects.filter(user_profile_id=user_id, date__gte=one_week_ago).\
                values(log_date = F('date__date')).\
                annotate(total_calories=Sum('calories'))
                        #total_proteins=Sum('proteins'),
                        #total_fat=Sum('fat'),
                        #total_carbs=Sum('carbs'))
        target_calories = ( TargetsHistory.objects\
                                .filter(user_profile_id=user_id, target_type='target_calorie_intake')\
                                .filter(Q(created_on__gte=datetime.now() - timedelta(days=7)))
                                .values(date = F('created_on__date'))
                                .annotate(target_calorie_intake=Max('target_value'))
                                .order_by('created_on__date'))

        
        #logs = FoodLog.objects.filter(date__gte=one_week_ago).values('food_name', 'calories','proteins','fat','carbs')
        logs_json = json.dumps(list(logs),cls=CustomJSONEncoder)
        target_calories = json.dumps(list(target_calories),cls=CustomJSONEncoder)
        
        data = {'exercises' : allExercises, 'quote' : { 'quote' : quote["quote"], 'author' : quote['author']}, 'target_water_intake':target_water, 'water_consumed': water_consumed,"one_week_FoodLog":logs_json,"target_calories":target_calories}

        print("Data",data)
        return render(request, "customs/dashboard.html", data) # {} is the data from DB to front end