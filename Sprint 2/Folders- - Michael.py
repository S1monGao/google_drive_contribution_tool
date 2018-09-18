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




# From here down is useful!!!!

def getFile(fileId, service):
    return service.files().get(fileId=fileId, supportsTeamDrives=True).execute()

def getFilesInFolder(folder, service):
    alist = []
    filesInFolder = service.children().list(folderId=folder['id'], maxResults=1000).execute()
    # Checking the folder is not empty
    if filesInFolder['items']:
        for f in filesInFolder['items']:
            tmp = getFile(f['id'], service)
            if "folder" in tmp['mimeType']:
                alist.extend(getFilesInFolder(tmp, service))
            elif "google-apps.document" in tmp['mimeType'] or "google-apps.spreadsheet" in tmp['mimeType']:
                alist.append(tmp)
    return alist


def getTeamDriveId(service, teamDriveName):
    teamDrives =  service.teamdrives().list().execute()['items']
    for team in teamDrives:
        if team['name'] == teamDriveName:
            return team['id']

def getTeamDriveFilesnFolders(service, teamDriveId):
    files = service.files().list(corpora="teamDrive", includeTeamDriveItems=True, supportsTeamDrives=True, teamDriveId=teamDriveId).execute()['items']
    fileList = []
    for file in files:

        # Getting all the docs and sheets
        if "google-apps.document" in file['mimeType'] or "google-apps.spreadsheet" in file['mimeType']:
            fileList.append(file)

        if "folder" in file['mimeType']:
            fileList.extend(getFilesInFolder(file, service))
    return fileList

def main():
    service = authenticate()

    file = service.files().list(corpora= "teamDrive",includeTeamDriveItems=True, supportsTeamDrives=True, teamDriveId= "0ABWpUQItOU0xUk9PVA").execute()

    teamDriveName = "FIT2101"
    id = getTeamDriveId(service, teamDriveName)
    files = getTeamDriveFilesnFolders(service, id)
    for i in files:
        print(i['title'], i['alternateLink'])



if __name__ == '__main__':
    main()
