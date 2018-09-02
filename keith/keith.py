from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import io
from googleapiclient.http import MediaIoBaseDownload
import datetime as dt
import matplotlib.pyplot as plt
from classes import User


# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'
start_time = dt.datetime(2018, 8, 29)
end_time = dt.datetime.now()


def main():

    # Authenticating and creating service
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        for item in items:
            if item['name'] == "Test Doc":
                print('{0} ({1})'.format(item['name'], item['id']))
                revisions = service.revisions().list(fileId=item['id'], fields="*").execute()
                users = [] #Will store a list of user class instances
                for revision in revisions['revisions']:
                    print(revision)
                    modifier = revision['lastModifyingUser']
                    modifier_name = modifier['displayName'] #Get the name of the person who made the modification
                    modified_time = dt.datetime.strptime(revision['modifiedTime'][:-2], '%Y-%m-%dT%H:%M:%S.%f') # convert time of conversion to dt object
                    modified_time = modified_time + dt.timedelta(hours=10) # Hardcoded conversion to AEST
                    modifier_found = False
                    for user in users:
                        if user.name == modifier_name:
                            user.times.append(modified_time)
                            user.num_rev += 1
                            modifier_found = True
                    if not modifier_found:
                        new_user = User(name=modifier_name)
                        new_user.times.append(modified_time)
                        new_user.num_rev += 1
                        users.append(new_user)
                for user in users:
                    print(user)
                plot_pie_chart(users)
                plot_lines(users, start_time, end_time)
                break


def main2():
    """
    Prints all the revisions of Test Doc and attempts to download (doesn't work so ignore)
    """

    # Authenticating and creating service
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        for item in items:
            if item['name'] == "Test Doc":
                print('{0} ({1})'.format(item['name'], item['id']))
                revisions = service.revisions().list(fileId=item['id'], fields="*")
                revisions = revisions.execute()
                for revision in revisions['revisions']:
                    print(revision['id'])
                    request = service.revisions().get_media(fileId=item['id'], revisionId=revision['id'])
                    downloaded = io.BytesIO()
                    downloader = MediaIoBaseDownload(downloaded, request)
                    done = False
                    while done is False:
                        # _ is a placeholder for a progress object that we ignore.
                        # (Our file is small, so we skip reporting progress.)
                        _, done = downloader.next_chunk()

                    downloaded.seek(0)
                    print('Downloaded file contents are: {}'.format(downloaded.read()))
                    print(revision)
                break


def plot_pie_chart(users):
    """
    Creates and plots the pie chart
    :param users: A list of User class instances
    :return: None
    :postcondition: pie chart for number of revisions per user will be plotted
    """
    amounts = [user.num_rev for user in users]
    labels = [user.name for user in users]
    plt.pie(amounts, labels=labels)
    plt.title("Work ratio of users")
    plt.show()


def plot_line_info(user, start_time, end_time, num_sections):
    """

    :param user: A User class instance
    :param start_time: Time at which to start measuring changes
    :param end_time: Time at which to stop measuring changes
    :param num_sections: The number of 6hr slots between start and end
    :return: A list containing the number of revisions made by the user in each 6hr interval
    """
    num_revs_list = num_sections * [0]
    current_time = start_time
    times = user.times
    index = 0
    while current_time < end_time:
        while len(times) > 0 and current_time <= times[0] <= current_time + dt.timedelta(hours=6):
            num_revs_list[index] += 1
            times.pop(0)
        current_time += dt.timedelta(hours=6)
        index += 1
    return num_revs_list


def plot_lines(users, start_time, end_time):
    """
    Plots the line graphs for number of revisions for each user at each time slot
    :param users: A list of User class instances
    :param start_time: Time at which to start measuring changes
    :param end_time: Time at which to stop measuring changes
    :return: None
    :postcondition: line graphs for each user's revisions at each time interval are plotted
    """
    num_sections = int(((end_time - start_time) / dt.timedelta(hours=6) + 1) // 1)
    time_axis = num_sections * [0]
    time_axis[0] = start_time
    for i in range(1, num_sections):
        time_axis[i] = start_time + i*dt.timedelta(hours=6)
    for user in users:
        plt.plot(time_axis, plot_line_info(user, start_time, end_time, num_sections))
    plt.legend([user.name for user in users], loc='upper right')
    plt.xlabel("Date and hour")
    plt.ylabel("Number of revisions")
    plt.title("Revisions for each user at given times")
    plt.show()

if __name__ == '__main__':
    main()