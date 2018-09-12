from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# Updated by Michael on the 11/09/18 to change to V2 of the API

def authenticate():
    SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly https://www.googleapis.com/auth/drive.readonly'

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v2', http=creds.authorize(Http()))
    return service


def listFiles(service):
    """
    gets all the files in the google drive that are google docs or sheets and returns a list of them
    It only searches the first 1000 files
    :param service: Google Drive rest service
    :return: a list of file metadata objects that are either docs or sheets
    """

    files = service.files().list(maxResults=1000).execute()
    tmp = []
    # print file name for every google doc and sheet
    for f in files['items']:
        if "google-apps.document" in f['mimeType'] or "google-apps.spreadsheet" in f['mimeType'] or "folder" in f['mimeType']:
            tmp.append(f)
    return tmp


def getFileInfo(fileName, files):
    for file in files:
        if file['title'] == fileName:
            return file['id'], file

def getNameFromId(fileId, service):
    return service.files().get(fileId=fileId).execute()['title']

def getFile(fileId, service):
    return service.files().get(fileId=fileId).execute()

def getFilesInFolder(folder, list, service):
    filesInFolder = service.children().list(folderId=folder['id'], maxResults=1000).execute()
    if filesInFolder['items']:
        for f in filesInFolder['items']:
            tmp = getFile(f['id'], service)
            if "folder" in tmp['mimeType']:
                getFilesInFolder(tmp, list, service)
            elif "google-apps.document" in tmp['mimeType'] or "google-apps.spreadsheet" in tmp['mimeType']:
                list.append([getNameFromId(tmp['id'], service), tmp['id']])
    else:
        list.append([getNameFromId(folder['id'], service), folder['id']])





def main():
    service = authenticate()
    files = listFiles(service)
    # fileName = input("What is the name of the file or folder: ")
    fileName = "2018S2"
    id , file= getFileInfo(fileName, files)

    list = []
    getFilesInFolder(file, list, service)

    for i in list:
        print(i[0])




if __name__ == '__main__':
    main()
