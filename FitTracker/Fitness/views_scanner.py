from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, permissions

from .views import get_food_API, FoodDict
import requests
from django.http import JsonResponse
from .serializers import FoodLogSerializerPost

def get_food_API_UPC(UPC):
    api_key = '9666665392544b19a09736838fa4bc9f'
    url = f'https://api.spoonacular.com/food/products/upc/{UPC}?apiKey={api_key}'
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

def save_record(user_id,food_data):
    mutable_data = {}
    mutable_data['user_profile'] = user_id
    mutable_data["food_name"]=food_data.food_name
    mutable_data['quantity'] = 1
    mutable_data["carbs"] = float(mutable_data['quantity'])*float(food_data.carbs_per_serving)
    mutable_data["calories"] = float(mutable_data['quantity'])*float(food_data.cal_per_serving)
    mutable_data["proteins"] = float(mutable_data["quantity"])*float(food_data.pro_per_serving)
    mutable_data["fat"] = float(mutable_data["quantity"])*float(food_data.fat_per_serving)
    mutable_data["food_id"] = food_data.food_id
    
    serializer  = FoodLogSerializerPost(data=mutable_data)
    if serializer.is_valid():
            # Assign the current user's profile to the food log
            #serializer.validated_data['user_profile'] = request.user.profile
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class Scanner(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, id):
        
        TOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJmZDRhN2NmNy0xMDZmLTRiNWYtYTUzNi0xZDgzZGM0MjUzMDMiLCJpc3MiOiJjb20uZWFuLWRiIiwiaWF0IjoxNjgwODkxNzUwLCJleHAiOjE3MTI0Mjc3NTB9.gpNGwG9SEH48hBUrrEV1enukflTpJNGsa2U8i66hwdTJStiyCRsSARnoHWZrVjNu3OSApb7ekfY0d1quHxvDCQ"
        URL = "https://ean-db.com/api/v1/product/" + id

        header = {"Authorization" : "Bearer " + TOKEN}
        

        resp = requests.get(URL, headers=header)
        print("response:",resp.json())
        user_id = request.user.profile.id
        if resp.status_code == 200:
            #print(":resp",resp.json())
            food_name = resp.json()["product"]["titles"]["en"]
            print(food_name)
            food_data = get_food_API(food_name)
            if isinstance(food_data,JsonResponse):
                print("Not found")
                return Response(food_data.content.decode('utf-8'), status=status.HTTP_404_NOT_FOUND)
            print("hmmm")
            food_data = FoodDict(food_data)
            print("here:",food_data.food_name)
            rec = save_record(user_id,food_data)
            print("type",type(rec.data))
            return Response({"err" : False, "data" : rec.data}, status=status.HTTP_200_OK)
            #print("Resp codE:",resp.status_code)
        elif resp.status_code == 404:
            error_data = {'error':'No product found after scanning the code'}
            return JsonResponse(error_data,status=404)
            #return Repsonse({'err':True,""})
        
        return Response({"err" : True, "data" : f"error {resp.status_code}"}, status=resp.status_code)






