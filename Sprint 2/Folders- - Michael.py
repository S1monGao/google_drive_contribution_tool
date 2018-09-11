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
        if "google-apps.document" in f['mimeType'] or "google-apps.spreadsheet" in f['mimeType'] or "":
            tmp.append(f)

    return tmp


def getFileInfo(fileName, files):
    for file in files:
        if file['title'] == fileName:
            # print(file)
            return file['id'], file

def getNameFromId(fileId, service):
    return service.files().get(fileId=fileId).execute()['title']


def getFolders(service):
    files = service.files().list(maxResults=1000).execute()
    folders = []

    for f in files['items']:
        if "folder" in f['mimeType']:
            folders.append(f)

    return folders

def getFilesInFolder(folderName, folders, list, service):

    for folder in folders:
        if folder['title'] == folderName:
            filesInFolder = service.children().list(folderId=folder['id'], maxResults=1000).execute()
    for f in filesInFolder['items']:
        list.append([getNameFromId(f['id'], service), f['id']])
    #return list




def main():
    service = authenticate()
    files = listFiles(service)
    # fileName = input("What is the name of the file: ")
    # fileName = "Test Doc"
    fileName = "Agile Methods"
    id , file = getFileInfo(fileName, files)



    folders = getFolders(service)
    list = []
    folderName = "FIT2107 CEEBS"


    getFilesInFolder(folderName, folders, list, service)
    for i in list:
        print(i[0])




if __name__ == '__main__':
    main()
