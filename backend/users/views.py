
from rest_framework.views import APIView
from rest_framework.response import Response
from google_auth_oauthlib.flow import Flow
from google.auth.transport import requests
from django.urls import reverse
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import UserCredentials
from googleapiclient.discovery import build  # Import build
from google.oauth2.credentials import Credentials
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponseRedirect
from rest_framework.permissions import IsAuthenticated
import tempfile
import os
import uuid

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def get_user_google_credentials(user):
    user_credentials = UserCredentials.objects.get(user=user)

    credentials = Credentials(
        token=user_credentials.decrypted_access_token, 
        refresh_token=user_credentials.decrypted_refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET
    )

    return credentials


class GoogleOAuth2CallbackView(APIView):

    def get(self, request, *args, **kwargs):

        if "error" in request.GET:
            return Response({"error": request.GET.get("error")}, status=400)
        
        # Get client secrets from environment variable
        client_secrets_json = os.environ.get('GOOGLE_CLIENT_SECRETS_FILE')

        # Write the client secrets to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(client_secrets_json.encode())
            temp_file_path = temp_file.name
        
        # Initialize the flow object
        flow = Flow.from_client_secrets_file(
            temp_file_path,
            scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid", "https://www.googleapis.com/auth/calendar"],
        )
        flow.redirect_uri = request.build_absolute_uri(reverse('google_callback'))

        # Exchange the authorization code for tokens
        authorization_response = request.get_full_path()
        flow.fetch_token(authorization_response=authorization_response)

        # Get the credentials
        credentials = flow.credentials

        # Use the credentials to build the service object
        service = build('oauth2', 'v2', credentials=credentials)
        userinfo = service.userinfo().get().execute()

        # Extract user information
        email = userinfo.get("email")
        username = userinfo.get("email").split('@')[0]

        # Check if the user already exists by email
        try:
            user = User.objects.get(email=email)
            # User exists, log them in
            print("Logging in user : ", user)
            print("Session ID: ", self.request.session.session_key)
            login(self.request, user)

        except User.DoesNotExist:
            # User does not exist, create a new one
            user = User.objects.create_user(username=username, email=email)
            user.set_unusable_password()  # Set an unusable password
            user.save()
            print("Creating user account: ", user)
            login(self.request, user)

        # Update or create the user credentials
        UserCredentials.objects.update_or_create(
            user=user,
            defaults={
                'access_token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'scopes': ','.join(credentials.scopes)
            }
        )

        tokens = get_tokens_for_user(user)

        data = {'token': tokens["access"], 'refresh': tokens["refresh"]}
        print("Access token: " , tokens["access"])
        print("Refresh token: " , tokens["refresh"])
        # Convert data to a query string format
        query_string = '&'.join(f'{key}={value}' for key, value in data.items())
        # Redirect with query string
        redirect_url = f"{settings.FRONTEND_DOMAIN}?{query_string}"
        return HttpResponseRedirect(redirect_url)


class GoogleProfile(APIView):
    def get(self, request, format=None):
        permission_classes = [IsAuthenticated]

        credentials = get_user_google_credentials(request.user)

        # Use the credentials to build the service object
        service = build('oauth2', 'v2', credentials=credentials)
        userinfo = service.userinfo().get().execute()


        # Extract user information
        email = userinfo.get("email")
        name = userinfo.get("name")
        profile_picture = userinfo.get("picture")
        
        return Response({
            "name": name,
            "email": email,
            "picture_url": profile_picture
        }, status=200)

