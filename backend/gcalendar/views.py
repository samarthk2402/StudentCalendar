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
import pytz

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

def generate_free_time_slots(weekday_hours, weekend_hours, due_date, calendar_events):
    timezone = pytz.timezone('Europe/London')

    # Convert due_date string to a datetime object
    due_date = datetime.fromisoformat(due_date)

    # Check if due_date is naive and localize if necessary
    if due_date.tzinfo is None:
        due_date = timezone.localize(due_date)

    
     # Get current date and localize it
    today = datetime.now(timezone).replace(minute=0, second=0, microsecond=0)  # Current date with time at midnight

    free_time_slots = []
    
    # Loop through each day between today and the due date (inclusive)
    current_date = today
    while current_date <= due_date:
        # Determine if the current day is a weekday (Monday=0, Sunday=6)
        if current_date.weekday() < 5:
            start_hour, end_hour = weekday_hours  # Use weekday working hours
        else:
            start_hour, end_hour = weekend_hours  # Use weekend working hours
        
        # Generate free time slots for each hour within the specified working hours
        for hour in range(start_hour, end_hour):
            start_time = current_date.replace(hour=hour)
            end_time = start_time + timedelta(hours=1)
            # Ensure we don't generate time slots past the due date
            if end_time <= due_date + timedelta(days=1) and start_time > datetime.now(timezone):
                conflicting_events = 0
                for event in calendar_events:
                    event_start = datetime.fromisoformat(event["start"]["dateTime"])
                    event_end = datetime.fromisoformat(event["end"]["dateTime"])
                    if (event_start > start_time and event_start < end_time) or (event_end > start_time and event_end <end_time):
                        conflicting_events += 1

                if conflicting_events == 0:
                    free_time_slots.append((start_time.isoformat(), end_time.isoformat()))
        current_date += timedelta(days=1)
    
    return free_time_slots

def getHomeworkTimings(request, homework):
    credentials = get_user_google_credentials(request.user)
    service = build('calendar', 'v3', credentials=credentials)

    # Fetch calendar events from now till the due date
    events_result = service.events().list(
            calendarId='primary',
            timeMin=datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z',
            timeMax=homework.get("due_date"),
            singleEvents=True,
            orderBy='startTime'
        ).execute()
    
    events = events_result.get('items', [])

    free_slots = generate_free_time_slots((19, 21), (9, 12), homework["due_date"], events)

    timings = []

    # Split the string into hours, minutes, and seconds
    hours, minutes, seconds = map(int, homework["estimated_completion_time"].split(':'))
    print(homework["estimated_completion_time"])
    print(minutes)

    # Create a timedelta object
    time_needed = timedelta(hours=hours, minutes=minutes, seconds=seconds)

    for slot in free_slots:
        slot_start = datetime.fromisoformat(slot[0])
        slot_end = datetime.fromisoformat(slot[1])
        slot_duration = slot_end-slot_start
        print("Slot duration: ", slot_duration.total_seconds())
        print("Time Needed: ", time_needed.total_seconds())
        if slot_duration >= time_needed:
            timings.append((slot_start.isoformat(), (slot_start + time_needed).isoformat()))
            break
        elif slot_duration < time_needed:
            timings.append((slot_start.isoformat(), slot_end.isoformat()))
            time_needed -= slot_duration
            
    return timings


class AddHomework(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = HomeworkSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            # Save the new instance to the database
            serializer.save()

            timings = getHomeworkTimings(request, serializer.data)
            print(timings)

            for block in timings:
                print(block)
                new_homework = {
                    'summary': serializer.data.get("name"),
                    'start': {
                        'dateTime': block[0],
                        'timeZone': 'Europe/London'
                    },
                    'end': {
                        'dateTime': block[1],
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