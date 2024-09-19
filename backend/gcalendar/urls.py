from django.urls import path
from .views import *

urlpatterns = [
    path('events', GetCalendar.as_view())
]