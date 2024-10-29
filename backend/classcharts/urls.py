from django.urls import path
from .views import *

urlpatterns = [
    path('login', ClassChartsLogin.as_view()),
    path('verify', VerifyClassChartsLogin.as_view())

]