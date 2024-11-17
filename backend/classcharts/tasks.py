import threading
import time
from django.utils import timezone
from django.contrib.auth.models import User
from threading import Event
import requests
from datetime import date, timedelta
from gcalendar.serializers import HomeworkSerializer
from gcalendar.views import scheduleHomeworks

def daily_task():
    stop_event = Event()
    i = 1
    default_completion_time = 45
    synced_users = User.objects.filter(
        usercredentials__classcharts_session_id__isnull=False  # Check if classcharts_session_id is not None
    )

    while not stop_event.wait(86400):  # 86400 seconds = 24 hours
        # Perform the task for each user
        for user in synced_users:
            print(f"Running daily task {str(i)} for {user.username}")
            i += 1
            creds = user.usercredentials
            url = f"https://www.classcharts.com/apiv2student/homeworks/{creds.classcharts_student_id}?display_date=due_date&from={date.today()}&to={date.today() + timedelta(days=30)}"
            headers = {
            "Authorization": f"Basic {creds.classcharts_session_id}"
            }
            response = requests.request("GET", url, headers=headers)
            
            response_data = response.json()

            # Check for errors in the response
            if response_data.get('error'):
                print(f"Error {response.status_code}: {response_data.get('error', 'Unknown error')}")
            
            # Extract list of  incompleted homeworks
            homework_list = response_data.get("data", [])
            for homework in homework_list:
                if homework.get('status').get('ticked') == "yes":
                    homework_list.remove(homework)

            for homework in homework_list:
                print(homework.get("title"), " detected")

                #Add homeworks to calendar
                name = homework.get("title")
                due_date = homework.get("due_date")
                completion_time = homework.get("completion_time_value")
                completion_unit = homework.get("completion_time_unit")
                
                # Check if there is a completion time otherwise set to default
                if completion_time != "" and completion_time != None:
                    if completion_unit == "hours":
                        completion_time = int(completion_time)*60
                    elif completion_unit == "minutes":
                        completion_time = int(completion_time)
                else:
                    completion_time = default_completion_time

                already_assigned = False
                
                # check if already in homework
                for timetabled in user.homeworks.all():
                    if timetabled.name == name:
                        print(name, " is already assigned!")
                        already_assigned = True
                        continue # skip this homework as its already assigned

                if not already_assigned:
                    serializer = HomeworkSerializer(data={"name": name, "estimated_completion_time": completion_time, "due_date": due_date }, context={'user': user})
                    
                    if serializer.is_valid():
                        # Save the new instance to the database

                        instance = serializer.save()
                        print(instance.name, "saved")
                        scheduleHomeworks(user)
                                
            