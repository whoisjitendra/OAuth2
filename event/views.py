from django.conf import settings
from google_auth_oauthlib.flow import  Flow
from googleapiclient.discovery import build
from rest_framework.views import APIView
from rest_framework.response import Response



class InitView(APIView):
    def get(self, request):
        
        oauth_flow = Flow.from_client_secrets_file(
            settings.GOOGLE_CLIENT_SECRETS_FILE,
            scopes=['https://www.googleapis.com/auth/calendar.readonly'],
            redirect_uri=request.build_absolute_uri('/rest/calendar/redirect/')
        )
        authorization_url, state = oauth_flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        request.session['oauth_state'] = state
        
        return Response({"Authorization Url": authorization_url})
    
class OutputView(APIView):
    def get(self, request):
        state = request.session.pop('oauth_state', '')
        oauth_flow = Flow.from_client_secrets_file(
            settings.GOOGLE_CLIENT_SECRETS_FILE,
            scopes=['https://www.googleapis.com/auth/calendar.readonly'],
            state=state,
            redirect_uri=request.build_absolute_uri('/rest/calendar/redirect/')
        )
        authorization_response = request.build_absolute_uri()
        
        
        oauth_flow.fetch_token(authorization_response=authorization_response)

        credentials = oauth_flow.credentials
        calender_service = build('calendar', 'v3', credentials=credentials)
        events = calender_service.events().list(calendarId='primary', maxResults=20).execute()
        event_output = events.get('items', [])
        return Response({'events': events})
