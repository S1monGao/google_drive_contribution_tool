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
    print(filesInFolder)
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
    
    #fileName = "2018S2"
    #id , file= getFileInfo(fileName, files)

    list = []
    #team = service.teamdrives().get(teamDriveId="0ABWpUQItOU0xUk9PVA")
    #print(team)


    #file = service.files().get(fileId="0ABWpUQItOU0xUk9PVA", supportsTeamDrives=True).execute()
    file = service.files().list(corpora= "teamDrive",includeTeamDriveItems=True, supportsTeamDrives=True, teamDriveId= "0ABWpUQItOU0xUk9PVA").execute()
    print(file)
    #getFilesInFolder(team, list, service)

    #for i in list:
        #print(i)


    """

    teams = service.teamdrives().list().execute()
    for item in teams['items']:
        print(item['name'], item['id'])

    filesInFolder = service.children().list(folderId=""0ABWpUQItOU0xUk9PVA"", maxResults=1000).execute()
    print(filesInFolder)


    
    
    tmp = service.children().list(folderId="0ABWpUQItOU0xUk9PVA").execute()
    print(tmp)
    print("len of tmp is: ", len(tmp['items']))

    child = service.children().get(folderId="0ABWpUQItOU0xUk9PVA", childId="1JV2zn6owERSviN2_zbzW_WQiq_bj9bZq")
    print(child['name'])


    #for f in tmp['items']:
        #print(getFile(f['id'], service))
    """







if __name__ == '__main__':
    main()
