"""
Team We Showed Up
Assignment 2
Sprint 1


04/09/18
Keith Pang
Glyn XXXXXXX
Josh De Luca
Michael Oren
Simon XXXXXXXXX

"""

from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime as dt
import matplotlib.pyplot as plt
from classes import User_v2, Revision

def authenticate():
    """
    This function authenticates the user, if there is no token.json file then it will open up a pop up to "log in" and
    authenticate the user. It then returns the service, which is the API and the access to all of it.
    :return: service - the API access variable
    """

    SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly https://www.googleapis.com/auth/drive.readonly'

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v2', http=creds.authorize(Http()))
    return service

def getDocsNSheets(service):
    """
    Gets all the files in the google drive that are google docs or sheets and returns a list of them
    It only searches the first 1000 files
    :param service: Google Drive rest API service
    :return: a list of file metadata objects that are either Google docs or sheets

    """

    items = service.files().list(maxResults=1000).execute()
    tmp = []
    # print file name for every google doc and sheet
    for f in items['items']:
        if "google-apps.document" in f['mimeType'] or "google-apps.spreadsheet" in f['mimeType']:
            tmp.append(f)
    return tmp


def getFileInfo(fileName, files):
    """
    Retrieves the files metadata based on fileName

    :param fileName: Name of the file that you want to get the metadata of
    :param files: A list of file metadata
    :return: the metadata of the file that matched the fileName
    """
    for file in files:
        if file['title'] == fileName:
            # print(file)
            return file











def main():
    # Need a way to alter start time to when the file was created
    start_time = dt.datetime(2018, 8, 29)
    end_time = dt.datetime.now()


    service = authenticate()
    files = getDocsNSheets(service)
    # fileName = input("Enter the filename: ")
    fileName = "Test Doc"
    file = getFileInfo(fileName, files)
    print(file['title'])
    revisions = service.revisions().list(fileId=item['id'], fields="*").execute()






if __name__ == '__main__':
    main()