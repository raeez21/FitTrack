from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.db import connection

# Create your views here.
def signup(request):
    if request.method == 'POST':
        table_name = 'Users'
        json_data = json.loads(request.body.decode('utf-8'))
        columns = ','.join(f'"{key}"' for key in json_data.keys())
        values = ','.join(f"'{value}'" for value in json_data.values())
        query = f'INSERT INTO "{table_name}" ({columns}) VALUES ({values})'
        with connection.cursor() as cursor:
            cursor.execute(query)
    return JsonResponse({'status': 'success'})