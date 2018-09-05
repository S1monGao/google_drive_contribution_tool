"""
Team We Showed Up
Assignment 2
Sprint 1


04/09/18
Keith Pang
Glyn Kendall
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
def Menu():
    quit = False
    # print('HELP\n\'choose file\': Choose the file or folder to view\n\'pie chart\': Prints pie chart of percentage contributions\n\'timeline\': Prints timelines of all group members between specified start and end points\n\'changes\': Prints changes made by all group members between specified start and end points\n\'help\': Prints help menu\n\'quit\': Exits the program\n')
    print('HELP\n\'v:<FILE_NAME>\': Graph revision changes for the file specified\n\'help\': Prints help menu\n\'quit\': Exits the program\n')

    while not quit:
        inp=input('Please choose a command: ')
        if inp == 'quit':
            quit = True
        elif inp.split(":")[0] == "v":
            main(inp.split(":")[1])
        elif inp == 'help':
            print('HELP\n\'v:<FILE_NAME>\': Graph revision changes for the file specified\n\'help\': Prints help menu\n\'quit\': Exits the program\n')
        else:
            print("Invalid command, please try again\n")
        # elif inp == 'pie chart':
        #     print('print pie chart of team contributions here')
        # elif inp == 'timeline':
        #     lowerBnd=input("Please choose date for start of timeline (dd/mm/yyyy): ")
        #     upperBnd = input("Please choose date for end of timeline (dd/mm/yyyy): ")
        #     print(lowerBnd,'<-------------->',upperBnd)
        # elif inp == 'changes':
        #     lowerBnd = input("Please choose date for start of changes (dd/mm/yyyy): ")
        #     upperBnd = input("Please choose date for end of changes (dd/mm/yyyy): ")
        #     print('print changes here')


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
    It only searches the first 200 files
    :param service: Google Drive rest API service
    :return: a list of file metadata objects that are either Google docs or sheets

    """

    items = service.files().list(maxResults=200).execute()
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
    print("Invalid file name, please try again")
    return False

def get_revision_content(revision, service):
    """
    From the revision metadata, it retrieves the actual text data and returns it as a string
    :param revision: Revision metadata for one revision
    :return: A string of the current stage of the file
    """
    text_link = revision['exportLinks']['text/plain']
    _, data = service._http.request(text_link)
    data = str(data, 'utf-8')
    return "".join(data.split())

def getRevisions(file, service):
    """
    Gets 1000 previous revisions for the file
    :param file: the file metadata that you want revisions for
    :return: An array of revision metadata
    """
    fileId = file['id']
    revisions = service.revisions().list(fileId=fileId, fields="*", maxResults=1000).execute()
    return revisions

def handleRevisionData(revisions, service):
    """
    From the revision data, this file creates a new User for each user who modified the code and adds their revision data
    to the user
    :param revisions: A list of revision metadata on the file that you want the data on
    :return: An array of users (a class) with their revision data
    """
    users = []
    previous_revision_num_chars = 0
    for revision in revisions['items']:
        revision_content = get_revision_content(revision, service)

        # Finding the number of chars changed in each revision
        num_chars_changed = len(revision_content) - previous_revision_num_chars
        is_addition = False
        if num_chars_changed > 0:
            is_addition = True
        num_chars_changed = abs(num_chars_changed)


        # update so that we later compare next revision to the current one
        previous_revision_num_chars = len(revision_content)

        # Get the name of the person who made the modification
        modifier_name = revision['lastModifyingUser']['displayName']

        # convert time of conversion to dt object
        modified_time = dt.datetime.strptime(revision['modifiedDate'][:-2], '%Y-%m-%dT%H:%M:%S.%f')
        # Hardcoded conversion to AEST
        modified_time = modified_time + dt.timedelta(hours=10)


        modifier_found = False
        revision_object = Revision(num_chars_changed, modified_time, is_addition)

        # Checking if the user is known or not, if not then it creates and adds user
        for user in users:
            if user.name == modifier_name:
                user.add_revision(revision_object)
                modifier_found = True
        if not modifier_found:
            new_user = User_v2(name=modifier_name)
            new_user.add_revision(revision_object)
            users.append(new_user)
    return users

def plot_pie_chart(users):
    """
    Creates and plots the pie chart
    :param users: A list of User class instances
    :return: None
    :postcondition: pie chart for number of revisions per user will be plotted
    """
    amounts = [user.num_added - user.num_deleted for user in users]
    labels = [user.name for user in users]
    plt.pie(amounts, labels=labels)
    plt.title("Work ratio of users")
    plt.show()

def plot_line_info(user, start_time, end_time, num_sections, is_additions):
    """

    :param user (User_v2 instance): A User class instance
    :param start_time (datetime): Time at which to start measuring changes
    :param end_time (datetime): Time at which to stop measuring changes
    :param num_sections (integer): The number of 6hr slots between start and end
    :param is_additions (boolean): Measuring additions or deletions
    :return: A list containing the number of revisions made by the user in each 6hr interval
    """
    num_revs_list = num_sections * [0]
    current_time = start_time
    revisions = [revision for revision in user.revisions]
    index = 0
    while current_time < end_time:
        while len(revisions) > 0 and current_time <= revisions[0].time <= current_time + dt.timedelta(hours=6):
            if revisions[0].is_add is is_additions:
                num_revs_list[index] += revisions[0].num_chars
            revisions.pop(0)
        current_time += dt.timedelta(hours=6)
        index += 1
    return num_revs_list

def plot_lines(users, start_time, end_time, is_additions):
    """
    Plots the line graphs for number of revisions for each user at each time slot
    :param users (List): A list of User class instances
    :param start_time (Datetime): Time at which to start measuring changes
    :param end_time (Datetime): Time at which to stop measuring changes
    :param is_additions (Boolean): Measuring additions or deletions
    :return: None
    :postcondition: line graphs for each user's revisions at each time interval are plotted
    """
    num_sections = int(((end_time - start_time) / dt.timedelta(hours=6) + 1) // 1)
    time_axis = num_sections * [0]
    time_axis[0] = start_time
    for i in range(1, num_sections):
        time_axis[i] = start_time + i*dt.timedelta(hours=6)
    for user in users:
        plt.plot(time_axis, plot_line_info(user, start_time, end_time, num_sections, is_additions))
    plt.legend([user.name for user in users], loc='upper right')
    plt.xlabel("Date and hour")
    plt.ylabel("Number of characters")
    if is_additions:
        plt.title("Number of characters added by each user at given times")
    else:
        plt.title("Number of characters deleted by each user at given times")
    plt.show()

def graphData(users, start_time, end_time):
    plot_pie_chart(users)
    plot_lines(users, start_time, end_time, True)
    plot_lines(users, start_time, end_time, False)

def main(fileName):
    service = authenticate()
    files = getDocsNSheets(service)

    # fileName = input("Enter the filename: ")
    # fileName = "Test Doc"
    file = getFileInfo(fileName, files)
    if not file:
        return
    revisions = getRevisions(file, service)
    users = handleRevisionData(revisions, service)

    # getting time of file creation and adding 10 hrs to convert to AEST
    start_time = dt.datetime.strptime(file['createdDate'][:-2], '%Y-%m-%dT%H:%M:%S.%f')
    start_time = start_time + dt.timedelta(hours=10)

    end_time = dt.datetime.now()
    graphData(users, start_time, end_time)

if __name__ == '__main__':
    # main()
    Menu()