from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, permissions


import requests


class Scanner(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, id):
        
        TOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJmZDRhN2NmNy0xMDZmLTRiNWYtYTUzNi0xZDgzZGM0MjUzMDMiLCJpc3MiOiJjb20uZWFuLWRiIiwiaWF0IjoxNjgwODkxNzUwLCJleHAiOjE3MTI0Mjc3NTB9.gpNGwG9SEH48hBUrrEV1enukflTpJNGsa2U8i66hwdTJStiyCRsSARnoHWZrVjNu3OSApb7ekfY0d1quHxvDCQ"
        URL = "https://ean-db.com/api/v1/product/" + id

        header = {"Authorization" : "Bearer " + TOKEN}
        

        resp = requests.get(URL, headers=header)
        content = resp.json()

        if resp.status_code == 200:
            return Response({"err" : False, "data" : content}, status=status.HTTP_200_OK)
        
        return Response({"err" : True, "data" : content}, status=content["error"]["code"])






