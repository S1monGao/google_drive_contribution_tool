from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime as dt
import matplotlib.pyplot as plt
from classes import User_v2, Revision


# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly https://www.googleapis.com/auth/drive.readonly'
start_time = dt.datetime(2018, 8, 29)
end_time = dt.datetime.now()

# Authenticating and creating service
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('drive', 'v2', http=creds.authorize(Http()))


def main():

    # Call the Drive v3 API
    results = service.files().list().execute()
    items = results['items']

    if not items:
        print('No files found.')
    else:
        for item in items:
            if item['title'] == "Test Doc":
                print('{0} ({1})'.format(item['title'], item['id']))
                revisions = service.revisions().list(fileId=item['id'], fields="*").execute()
                users = [] #Will store a list of user class instances
                previous_revision_num_chars = 0
                for revision in revisions['items']:
                    revision_content = get_revision_content(revision)
                    num_chars_changed = len(revision_content) - previous_revision_num_chars
                    is_addition = False
                    if num_chars_changed > 0:
                        is_addition = True
                    num_chars_changed = abs(num_chars_changed)
                    previous_revision_num_chars = len(revision_content) #update so that we later compare next revision to the current one

                    modifier_name = revision['lastModifyingUser']['displayName'] #Get the name of the person who made the modification
                    modified_time = dt.datetime.strptime(revision['modifiedDate'][:-2], '%Y-%m-%dT%H:%M:%S.%f') # convert time of conversion to dt object
                    modified_time = modified_time + dt.timedelta(hours=10) # Hardcoded conversion to AEST
                    modifier_found = False
                    revision_object = Revision(num_chars_changed, modified_time, is_addition)
                    for user in users:
                        if user.name == modifier_name:
                            user.add_revision(revision_object)
                            modifier_found = True
                    if not modifier_found:
                        new_user = User_v2(name=modifier_name)
                        new_user.add_revision(revision_object)
                        users.append(new_user)
                plot_pie_chart(users)
                plot_lines(users, start_time, end_time, True)
                plot_lines(users, start_time, end_time, False)
                break


def get_revision_content(revision):
    text_link = revision['exportLinks']['text/plain']
    _, data = service._http.request(text_link)
    data = str(data, 'utf-8')
    return "".join(data.split())


def plot_pie_chart(users):
    """
    Creates and plots the pie chart
    :param users: A list of User class instances
    :return: None
    :postcondition: pie chart for number of revisions per user will be plotted
    """
    amounts = [user.num_added - user.num_deleted for user in users] #subtracting so that we get net change
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

if __name__ == '__main__':
    main()