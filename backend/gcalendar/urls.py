from django.urls import path
from .views import *

urlpatterns = [
    path('events', GetCalendar.as_view()),
    path('homework/add', AddHomework.as_view()),
    path('homework/delete', DeleteHomework.as_view()),
    path('homework', GetHomeworks.as_view()),
]