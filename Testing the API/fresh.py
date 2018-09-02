from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools



def authenticate():
    SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly https://www.googleapis.com/auth/drive.readonly'

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))
    return service


def listFiles(service):
    """
    gets all the files in the google drive that are google docs or sheets and returns a list of them
    It only searches the first 1000 files
    :param service: Google Drive rest service
    :return: a list of file metadata objects that are either docs or sheets
    """

    files = service.files().list(pageSize=1000).execute()
    tmp = []
    # print file name for every google doc and sheet
    for f in files['files']:
        if "google-apps.document" in f['mimeType'] or "google-apps.spreadsheet" in f['mimeType']:
            tmp.append(f)

    return tmp


def getFileInfo(fileName, files):
    for file in files:
        if file['name'] == fileName:
            # print(file)
            return file['id']


def main():
    service = authenticate()
    files = listFiles(service)
    # fileName = input("What is the name of the file: ")
    fileName = "Test Doc"
    id = getFileInfo(fileName, files)


    revisions = service.revisions().list(fileId=id, fields="*").execute()
    for r in revisions['revisions']:
        print("\n", r, "\n")




if __name__ == '__main__':
    main()
