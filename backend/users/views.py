from rest_framework.views import APIView
from rest_framework.response import Response
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests
from urllib.parse import urlencode
from django.urls import reverse
from django.conf import settings
from django.shortcuts import redirect

class IsAuthenticated(APIView):
    def get(self, request, format=None):
        if "credentials" in request.session:
            return Response(status=200)
        return Response(status=400)


class GoogleOAuth2CallbackView(APIView):

    def get(self, request, *args, **kwargs):
        if "error" in request.GET:
            return Response({"error": request.GET.get("error")}, status=400)

        client_secrets_file = r'C:\Users\samar\OneDrive\Documents\Dev\AutoHomeworkScheduler\client_secret_1086056028133-gdsavhkbqdhnls4luen4ccteoaat7ogi.apps.googleusercontent.com.json'

        # Initialize the flow object
        flow = Flow.from_client_secrets_file(
            client_secrets_file,
            scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid", "https://www.googleapis.com/auth/calendar"],
        )
        flow.redirect_uri = request.build_absolute_uri(reverse('google_callback'))

        # Exchange the authorization code for tokens
        authorization_response = request.get_full_path()
        flow.fetch_token(authorization_response=authorization_response)

        # Get the credentials
        credentials = flow.credentials

        request.session['credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

        return redirect(settings.FRONTEND_DOMAIN)
