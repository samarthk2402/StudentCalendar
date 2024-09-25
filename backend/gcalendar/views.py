from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from googleapiclient.discovery import build  # Import build
from google.oauth2.credentials import Credentials
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
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

    return event.get("id")

def generate_free_time_slots(weekday_hours, weekend_hours, due_date, calendar_events, buffer_time):
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
        
        beginning_working_hour = current_date.replace(hour=start_hour)
        end_working_hour = current_date.replace(hour=end_hour)

        start_time = beginning_working_hour
        end_time = end_working_hour


        conflicting_events = []

        for event in calendar_events:
            event_start = datetime.fromisoformat(event["start"]["dateTime"])
            event_end = datetime.fromisoformat(event["end"]["dateTime"])
            if (event_start > start_time and event_start < end_time) or (event_end > start_time and event_end <end_time):
                conflicting_events.append(event)
                print("Conflicting event: ", event.get("summary"))


        for event in conflicting_events:
            event_start = datetime.fromisoformat(event["start"]["dateTime"])
            event_end = datetime.fromisoformat(event["end"]["dateTime"])
            
            if event_start == start_time:
                start_time = event_end + buffer_time

            if event_start > start_time:
                if start_time > datetime.now(timezone):
                    free_time_slots.append((start_time.isoformat(), event_start.isoformat()))
                start_time = event_end + buffer_time

        if start_time == beginning_working_hour or start_time < end_time:
            if start_time > datetime.now(timezone):
                free_time_slots.append((start_time.isoformat(), end_time.isoformat()))

        current_date += timedelta(days=1)
    
    print(free_time_slots)
    return free_time_slots

def getHomeworkTimings(request, homework):
    credentials = get_user_google_credentials(request.user)
    service = build('calendar', 'v3', credentials=credentials)

    timezone = pytz.timezone('Europe/London')

    weekday_work_hours = (19, 21)
    weekend_work_hours = (9, 12)

    # Fetch calendar events from now till the due date
    events_result = service.events().list(
            calendarId='primary',
            timeMin=datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z',
            timeMax=homework.get("due_date"),
            singleEvents=True,
            orderBy='startTime'
        ).execute()
    
    events = events_result.get('items', [])

    free_slots = generate_free_time_slots(weekday_work_hours, weekend_work_hours, homework["due_date"], events, timedelta(minutes=15))

    timings = []

    # Split the string into hours, minutes, and seconds
    hours, minutes, seconds = map(int, homework["estimated_completion_time"].split(':'))

    # Create a timedelta object
    time_needed = timedelta(hours=hours, minutes=minutes, seconds=seconds)
    
    max_time = timedelta(minutes=45)

    if time_needed > max_time:

        days_until_due = []

        for start, end in free_slots:

            start_date = datetime.fromisoformat(start).date()
            if not start_date in days_until_due:
                days_until_due.append(start_date)

        spaced_out_time = len(days_until_due) * max_time

        if spaced_out_time >= time_needed:
            for day in days_until_due:
                # List to store the intervals that match the target date
                slots_on_this_day = []
                time_needed = max_time

                # Find all intervals where the start or end date matches the target date
                for start, end in free_slots:
                    # Check if the start or end date matches the target date
                    if datetime.fromisoformat(start).date() == day:
                        slots_on_this_day.append((start, end))

                for slot in slots_on_this_day:
                    slot_start = datetime.fromisoformat(slot[0])
                    slot_end = datetime.fromisoformat(slot[1])
                    slot_duration = slot_end-slot_start
                    if slot_duration >= time_needed:
                        timings.append((slot_start.isoformat(), (slot_start + time_needed).isoformat()))
                        break
                    elif slot_duration < time_needed:
                        timings.append((slot_start.isoformat(), slot_end.isoformat()))
                        time_needed -= slot_duration

        else:
            print("Homework cannot be spaced out")
    else:

        for slot in free_slots:
            slot_start = datetime.fromisoformat(slot[0])
            slot_end = datetime.fromisoformat(slot[1])
            slot_duration = slot_end-slot_start
            print("Slot duration: ", slot_duration.total_seconds())
            print("Time Needed: ", time_needed.total_seconds())
            if slot_duration >= time_needed:
                timings.append((slot_start.isoformat(), (slot_start + time_needed).isoformat()))
                break

    if not len(timings) > 0:
        for slot in free_slots:
            slot_start = datetime.fromisoformat(slot[0])
            slot_end = datetime.fromisoformat(slot[1])
            slot_duration = slot_end-slot_start
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
            homework_instance =  serializer.save()

            timings = getHomeworkTimings(request, serializer.data)

            ids = []

            for block in timings:
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
        
                ids.append(addEventToCalendar(request, new_homework))


            if len(ids)>1:
                # Update the Homework instance with the event_id
                homework_instance.event_ids = ids
                homework_instance.save()
            else:
                homework_instance.event_id = ids[0]
                homework_instance.save()


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
    
class GetHomeworks(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HomeworkSerializer
    
    def get_queryset(self):
        user = self.request.user
        return user.homeworks.all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Add the 'id' to the serialized data manually
        response_data = []
        for homework, data in zip(queryset, serializer.data):
            data_with_id = {**data, 'id': homework.id}
            response_data.append(data_with_id)

        return Response(response_data)
    
class DeleteHomework(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, format=None):
        homework_id = request.data.get("id")
        homework = Homework.objects.get(id=homework_id)

        if homework == None:
            return Response({"Bad Request" : "Homework does not exist..."}, status=status.HTTP_400_BAD_REQUEST)

        # Get user's Google credentials
        credentials = get_user_google_credentials(request.user)

        # Use the credentials to build the Google Calendar service object
        service = build('calendar', 'v3', credentials=credentials)

        if len(homework.event_ids) > 0:
            for event_id in homework.event_ids:
                service.events().delete(calendarId='primary', eventId=event_id).execute()
        else:
            if homework.event_id:
                service.events().delete(calendarId='primary', eventId=homework.event_id).execute()

        homework.delete()

        return Response({"message": "Deleted successfully!"}, status=204)

