from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient import errors




def authenticate():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))
    return service

def listFiles(service):
    files = service.files().list().execute()
    return  files['files']


def getFileInfo(fileName, files):
    for file in files:
        if file['name'] == fileName:
            print(file)

def main():
    service = authenticate()
    files = listFiles(service)
    # fileName = input("What is the name of the file: ")
    fileName = "LECTURE2.pdf"
    getFileInfo(fileName, files)


if __name__ == '__main__':
    main()
