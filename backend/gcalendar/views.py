from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from googleapiclient.discovery import build  # Import build
from google.oauth2.credentials import Credentials
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import UserCredentials
from datetime import datetime, timedelta
from .models import Homework
from .serializers import HomeworkSerializer
from rest_framework import status
def get_user_google_credentials(user):
    user_credentials = UserCredentials.objects.get(user=user)

    credentials = Credentials(
        token=user_credentials.access_token, 
        refresh_token=user_credentials.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET
    )

    return credentials

def addEventToCalendar(request, event):
    # Get user's Google credentials
    credentials = get_user_google_credentials(request.user)

    # Use the credentials to build the Google Calendar service object
    service = build('calendar', 'v3', credentials=credentials)
    event = service.events().insert(calendarId='primary', body=event).execute()
    print("Event created: "+ event.get("summary"))

class AddHomework(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = HomeworkSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            # Save the new instance to the database
            serializer.save()

            new_homework = {
                'summary': serializer.data.get("name"),
                'start': {
                    'dateTime': datetime.utcnow().isoformat(),
                    'timeZone': 'Europe/London'
                },
                'end': {
                    'dateTime': datetime.utcnow().isoformat(),
                    'timeZone': 'Europe/London'
                }
            }

            addEventToCalendar(request, new_homework)


            return Response({"message": f"{request.data.get("name")} was successfully added to your calendar"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Create your views here.
class GetCalendar(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Get user's Google credentials
        credentials = get_user_google_credentials(request.user)

        # Use the credentials to build the Google Calendar service object
        service = build('calendar', 'v3', credentials=credentials)

        from datetime import datetime, timedelta

        # Get the current date
        now = datetime.utcnow()

        # Set the minimum time as today (start of the day)
        time_min = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'  # Today at 00:00:00 UTC

        # Set the maximum time as 6 days from today (end of the day)
        time_max = (now + timedelta(days=6)).replace(hour=23, minute=59, second=59, microsecond=999999).isoformat() + 'Z'  # 6 days from now at 23:59:59 UTC

        # Fetch calendar events for the current week
        events_result = service.events().list(
            calendarId='primary',
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()


        events = events_result.get('items', [])
        events_response = []


        for event in events:
            if event["summary"]:
                summary = event["summary"]
            else:
                summary = "Untitled"

            response_event = {
                "summary": summary,
                "start": event["start"],
                "end": event["end"] 
            }
            events_response.append(response_event)


        return Response({"events": events_response}, status=200)