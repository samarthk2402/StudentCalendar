from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from googleapiclient.discovery import build  # Import build
from google.oauth2.credentials import Credentials
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import UserCredentials
from datetime import datetime, timedelta

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


# Create your views here.
class GetCalendar(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Get user's Google credentials
        credentials = get_user_google_credentials(request.user)

        # Use the credentials to build the Google Calendar service object
        service = build('calendar', 'v3', credentials=credentials)

        # Get the current date and calculate the start and end of the current week
        now = datetime.utcnow()
        start_of_week = now - timedelta(days=now.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=6)  # Sunday

        # Convert the dates to RFC3339 format, required by Google Calendar API
        time_min = start_of_week.isoformat() + 'Z'  # Z means UTC time
        time_max = end_of_week.isoformat() + 'Z'

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
            response_event = {
                "summary": event["summary"],
                "start": event["start"],
                "end": event["end"] 
            }
            events_response.append(response_event)

        return Response({"events": events_response}, status=200)