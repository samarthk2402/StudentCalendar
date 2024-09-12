from django.contrib import admin
from django.urls import path, include
from users.views import GoogleOAuth2CallbackView, IsAuthenticated

urlpatterns = [
    path('admin/', admin.site.urls),
    path('google/callback/', GoogleOAuth2CallbackView.as_view(), name='google_callback'),
    path('is-authenticated', IsAuthenticated.as_view())
]
