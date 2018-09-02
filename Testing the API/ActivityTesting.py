from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/activity'

def main():
    """Shows basic usage of the Drive Activity API.
    Prints information about the last 10 events that occured the user's Drive.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials1.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('appsactivity', 'v1', http=creds.authorize(Http()))

    # Call the Drive Activity API
    results = service.activities().list(source='drive.google.com',
        drive_ancestorId='root', pageSize=10).execute()
    activities = results.get('activities', [])

    if not activities:
        print('No activity.')
    else:
        print('Recent activity:')
        for activity in activities:
            event = activity['combinedEvent']
            print("\n",activity)
            #print("\n", event, "\n")
            user = event.get('user', None)
            target = event.get('target', None)
            if user is None or target is None:
                continue
            time = datetime.datetime.fromtimestamp(
                int(event['eventTimeMillis'])/1000)
            print('{0}: {1}, {2}, {3} ({4}) {5}'.format(time, user['name'],
                event['primaryEventType'], target['name'], target['mimeType'], target['id']))



if __name__ == '__main__':
    main()