from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# Updated by Michael on the 03/10/18 to implement functions that will work with the GUI

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
def getFolderInTeamDrive(service, folderName, teamDriveName):
    id = getTeamDriveId(service, teamDriveName)
    files = service.files().list(corpora="teamDrive", includeTeamDriveItems=True, supportsTeamDrives=True, teamDriveId=id).execute()['items']
    for f in files:
        if f['title'] == folderName:
            return f

def getFile(fileId, service):
    return service.files().get(fileId=fileId, supportsTeamDrives=True).execute()

def getFilesInFolder(id, service):
    alist = []
    filesInFolder = service.children().list(folderId=id, maxResults=1000).execute()
    # Checking the folder is not empty
    if filesInFolder['items']:
        for f in filesInFolder['items']:
            tmp = getFile(f['id'], service)
            if "folder" in tmp['mimeType']:
                alist.extend(getFilesInFolder(tmp['id'], service))
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
        if "google-apps.document" in file['mimeType']:
            fileList.append(file)

        if "folder" in file['mimeType']:
            fileList.extend(getFilesInFolder(file['id'], service))
    return fileList

def convertFilesToUrls(files):
    urls = []
    for file in files:
        urls.append(file['alternateLink'])
    return urls

def getFileInTeamDrive(service, fileName, teamDriveName):
    teamDriveId = getTeamDriveId(service, teamDriveName)
    files = service.files().list(corpora="teamDrive", includeTeamDriveItems=True, supportsTeamDrives=True, teamDriveId=teamDriveId).execute()
    print(files)


def main():
    service = authenticate()

    # GET ALL THE FILES WITHIN A TEAM DRIVE
    teamDriveName = "FIT2101"
    # teamDriveName = input("Enter the name of the team drive you wish to enter: ")
    # id = getTeamDriveId(service, teamDriveName)
    # files = getTeamDriveFilesnFolders(service, id)
    # for i in files:
    #     print(i['title'], i['alternateLink'])

    getFileInTeamDrive(service, "hey", teamDriveName)

    """
    # GET A FOLDER WITHIN A TEAM DRIVE
    # FolderName => 
    folderName = "Assignment 1"
    folder = getFolderInTeamDrive(service, folderName, teamDriveName)
    folderFiles = getFilesInFolder(folder['id'],service)
    # for f in folderFiles:
    #     print(f['title'],"\n", f['alternateLink'], "\n")

    urls = convertFilesToUrls(folderFiles)
    print(urls)


    folder = getTeamDriveId(service, teamDriveName)
    folderFiles = getFilesInFolder(folder, service)

    for f in folderFiles:
        print(f['title'], "\n")

    # urls = convertFilesToUrls(folderFiles)
    # print(urls)
    """






if __name__ == '__main__':
    main()
