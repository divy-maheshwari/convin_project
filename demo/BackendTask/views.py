from __future__ import print_function

from django.shortcuts import render, redirect
from django.urls import reverse
from urllib.parse import urlencode

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Create your views here.

from django.http import HttpResponse

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

cred = None
def GoogleCalendarInitView(request):
    global cred
    flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
    cred = flow.run_local_server(port=0)
    # if os.path.exists('token.json'):
    #     creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             'credentials.json', SCOPES)
    #         creds = flow.run_local_server(port=0)
    #     with open('token.json', 'w') as token:
    #         token.write(creds.to_json())

    return redirect('http://127.0.0.1:8000/rest/v1/calendar/redirect/')


def GoogleCalendarRedirectView(request):
    global cred
    #print(request.GET)
    try :
        #print("in the try")
        service = build('calendar', 'v3', credentials=cred)

        now = datetime.datetime.utcnow().isoformat() + 'Z'  
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                                maxResults=10, singleEvents=True,
                                                orderBy='startTime').execute()
        events = events_result.get('items', [])
        #print(events)

        if not events:
            #print('No upcoming events found.')
            return HttpResponse("No events found")
        #print("events")
        response_obj = []
        for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'])
                response_obj.append(start+" "+event['summary'])
        return HttpResponse(response_obj)
        
    except HttpError as error:
        print('An error occurred: %s' % error)

    return HttpResponse("you are at redirect.")
