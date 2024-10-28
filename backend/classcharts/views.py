from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from datetime import datetime

def login(code, dob, remember_me=True):
    # Prepare the form data
    form = {
        'code': code,
        'dob': dob.strftime('%Y-%m-%d'),
        'remember_me': '1' if remember_me else '0',
        'recaptcha-token': 'no-token-available'
    }


    url = "https://www.classcharts.com/apiv2student/login"

    try:
        # Send the POST request
        response = requests.post(url, data=form)

        # Parse the response
        response_data = response.json()
        
        # Check for errors in the response
        if response.status_code != 200:
            raise Exception(f"Error {response.status_code}: {response_data.get('error', 'Unknown error')}")
        
        # Extract session ID if login is successful
        session_id = response_data.get('meta', {}).get('session_id')
        return session_id  

    except requests.RequestException as e:
        print(f"An error occurred during the request: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Create your views here.
class ClassChartsLogin(APIView):

    def post(self, request):
        code = request.data.get("code")
        dob = datetime.strptime(request.data.get("dob"), "%Y-%m-%d")

        session_id = login(code, dob)
        if session_id:
            return Response({"message": "Logged in successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Error linking you account! Please verify your code and date of birth"})

    
