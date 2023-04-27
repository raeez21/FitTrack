from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, permissions

from .views import get_food_API, FoodDict
import requests
from django.http import JsonResponse

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


class Scanner(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, id):
        
        TOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJmZDRhN2NmNy0xMDZmLTRiNWYtYTUzNi0xZDgzZGM0MjUzMDMiLCJpc3MiOiJjb20uZWFuLWRiIiwiaWF0IjoxNjgwODkxNzUwLCJleHAiOjE3MTI0Mjc3NTB9.gpNGwG9SEH48hBUrrEV1enukflTpJNGsa2U8i66hwdTJStiyCRsSARnoHWZrVjNu3OSApb7ekfY0d1quHxvDCQ"
        URL = "https://ean-db.com/api/v1/product/" + id

        header = {"Authorization" : "Bearer " + TOKEN}
        

        resp = requests.get(URL, headers=header)
        
        if resp.status_code == 200:
            print(":resp",resp.json())
            food_name = resp.json()["product"]["titles"]["en"]
            print(food_name)
            food_data = get_food_API(food_name)
            if isinstance(food_data,JsonResponse):
                #print("Not foun")
                return Response(food_data.content.decode('utf-8'), status=status.HTTP_404_NOT_FOUND)
            food_data = FoodDict(food_data)
            print("food data:",food_data)
            return Response({"err" : False, "data" : content}, status=status.HTTP_200_OK)
        
        return Response({"err" : True, "data" : content}, status=content["error"]["code"])






