from django.contrib import admin
from django.urls import path, include
from users.views import GoogleOAuth2CallbackView, GoogleProfile
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('google/callback/', GoogleOAuth2CallbackView.as_view(), name='google_callback'),
    path('user/google/profile', GoogleProfile.as_view(), name='google_profile'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
