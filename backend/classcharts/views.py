from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from datetime import datetime, timedelta, date
from rest_framework.permissions import IsAuthenticated
from users.models import UserCredentials 

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
        student_id = response_data.get('data', {}).get('id')
        return session_id, student_id  

    except requests.RequestException as e:
        print(f"An error occurred during the request: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Create your views here.
class ClassChartsLogin(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        code = request.data.get("code")
        dob = datetime.strptime(request.data.get("dob"), "%Y-%m-%d")

        session_id, student_id = login(code, dob)

        if session_id and student_id:
            # url = f"https://www.classcharts.com/apiv2student/homeworks/{student_id}?display_date=due_date&from={date.today()}&to={date.today() + timedelta(days=30)}"
            # headers = {
            # "Authorization": f"Basic {session_id}"
            # }
            # response = requests.request("GET", url, headers=headers)
            
            # response_data = response.json()

            # # Check for errors in the response
            # if response.status_code != 200:
            #     raise Exception(f"Error {response.status_code}: {response_data.get('error', 'Unknown error')}")
            
            # # Extract list of  incompleted homeworks
            # homework_list = response_data.get("data", [])
            # for homework in homework_list:
            #     if homework.get('status').get('ticked') == "yes":
            #         homework_list.remove(homework)

            user = request.user
            user_credentials, created = UserCredentials.objects.update_or_create(
                user=user,
                defaults={
                    'classcharts_session_id': session_id,
                    'classcharts_student_id': student_id,
                }
            )

            return Response({"message": "Logged in successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Error linking you account! Please verify your code and date of birth"})
        
class VerifyClassChartsLogin(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        creds = user.usercredentials

        url = "https://www.classcharts.com/apiv2student/ping"
        headers = {
        "Authorization": f"Basic {creds.classcharts_session_id}"
        }
        json = {
        "include_data": "true"
        }
        response = requests.request("POST", url, headers=headers, json=json)

        response_data = response.json()

        if response.status_code != 200:
            return Response({"error":f"Error {response.status_code}: {response_data.get('error', 'Unknown error')}"}, status=status.HTTP_400_BAD_REQUEST)

        new_session_id = response_data.get("meta").get("session_id", "")

        if new_session_id != "":

            UserCredentials.objects.update_or_create(
                    user=user,
                    defaults={
                        'classcharts_session_id': response_data.get("meta").get("session_id"),
                    }
            )

        return Response({"message": "user authenticated"}, status=status.HTTP_200_OK)
    
