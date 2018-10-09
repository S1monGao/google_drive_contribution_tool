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



def getTeamDriveId(service, teamDriveName):
    teamDrives =  service.teamdrives().list().execute()['items']
    for team in teamDrives:
        if team['name'] == teamDriveName:
            return team['id']






def convertFilesToUrls(files):
    urls = []
    for file in files:
        urls.append(file['alternateLink'])
    return urls

def getFileInTeamDrive(service, fileName, teamDriveName):
    teamDriveId = getTeamDriveId(service, teamDriveName)
    files = service.files().list(corpora="teamDrive", includeTeamDriveItems=True, supportsTeamDrives=True, teamDriveId=teamDriveId).execute()['items']
    for file in files:
     print(file['title'])




def listTeamDrives(service):
    """
    A Function that lists all of the team drives that the user is a part of
    :param service: The authenticated google API Service
    :return: an array with a list of tuples (name, teamDriveId)
    """
    list = []
    teamDrives = service.teamdrives().list().execute()['items']
    for team in teamDrives:
        list.append((team['name'],team['id']))
    return list

def listFoldersInTeamDrive(service, teamDriveId):
    """
    A function that gets a list of all the folders that exist within a team drive. This includes sub folders
    :param service: The authenticated Google API service
    :param teamDriveId: The id for the target team drive
    :return: a list of tuples of the form (folderName, folderId)
    """
    files = service.files().list(corpora="teamDrive", includeTeamDriveItems=True, supportsTeamDrives=True,
                                 teamDriveId=teamDriveId).execute()['items']
    folderList = []
    for file in files:
        if "folder" in file['mimeType']:
            folderList.append((file['title'], file['id']))
    return folderList

def listDocsInFolder(service, folderId):
    """
    A function that lists all the google docs  in a folder,
    :param service: The authenticated Google API service
    :param folderId: The Id of the folder that you want the children of
    :return: a list of tuples in the form (fileName, fileId)
    """
    files = service.children().list(folderId=folderId, maxResults=1000).execute()['items']
    docList = []
    for file in files:
        trueFile = service.files().get(fileId=file['id'], supportsTeamDrives= True).execute()
        if "google-apps.document" in trueFile['mimeType']:
            docList.append((trueFile['title'], trueFile['id']))
    return docList


def listAllFilesInTeamDrive(service, teamDriveId):
    """
    A Function that lists all the files in a teamDrive
    :param service: The Google API
    :param teamDriveId: the id of the team drive you want the files of
    :return: a list of tuples in the form (fileName, fileId)
    """
    files = service.files().list(corpora="teamDrive", includeTeamDriveItems=True, supportsTeamDrives=True, teamDriveId=teamDriveId).execute()['items']
    fileList = []
    for file in files:

        # Getting all the docs
        if "google-apps.document" in file['mimeType']:
            fileList.append((file['title'], file['id']))

        if "folder" in file['mimeType']:
            fileList.extend(getFilesInFolder(file['id'], service))
    return fileList

def getFilesInFolder(id, service):
    """
    An auxillary function for listAllFilesInTeamDrive()
    :param id: folder id
    :param service: google api service
    :return: a list of files in the folder and all of its subfolders
    """
    alist = []
    filesInFolder = service.children().list(folderId=id, maxResults=1000).execute()
    # Checking the folder is not empty
    if filesInFolder['items']:
        for f in filesInFolder['items']:
            tmp = service.files().get(fileId=f['id'], supportsTeamDrives=True).execute()
            if "folder" in tmp['mimeType']:
                alist.extend(getFilesInFolder(tmp['id'], service))
            elif "google-apps.document" in tmp['mimeType']:
                alist.append((tmp['title'], tmp['id']))
    return alist

def listDocsNotInAFolder(service, teamDriveId):
    """
    A function to get all the files in the root level of a teamDrive
    :param service: the google API service
    :param teamDriveId: The Id of the teamDrive
    :return: a list of tuples in the for (name, id)
    """
    files = service.files().list(corpora="teamDrive", includeTeamDriveItems=True, supportsTeamDrives=True,
                                 teamDriveId=teamDriveId).execute()['items']
    filelist = []
    for file in files:
        if "google-apps.document" in file['mimeType']:
            filelist.append((file['title'], file['id']))
    return filelist




def main():
    service = authenticate()

    # GET ALL THE FILES WITHIN A TEAM DRIVE
    teamDriveName = "FIT2101"
    # teamDriveName = input("Enter the name of the team drive you wish to enter: ")
    # id = getTeamDriveId(service, teamDriveName)
    # files = getTeamDriveFilesnFolders(service, id)
    # for i in files:
    #     print(i['title'], i['alternateLink'])

    # getFileInTeamDrive(service, "hey", teamDriveName)

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
    teamDrives = listTeamDrives(service)
    print(teamDrives, "\n")

    folderList = listFoldersInTeamDrive(service, "0ABWpUQItOU0xUk9PVA")
    print(folderList)
    print("\n")

    files = listDocsNotInAFolder(service, "0ABWpUQItOU0xUk9PVA")
    print(files)

    # inFolder = listDocsInFolder(service, "1JV2zn6owERSviN2_zbzW_WQiq_bj9bZq")
    # print(inFolder)
    #
    # allteamdrivefiles = listAllFilesInTeamDrive(service, "0ABWpUQItOU0xUk9PVA")
    # print("\n\n\n", allteamdrivefiles)





if __name__ == '__main__':
    main()
