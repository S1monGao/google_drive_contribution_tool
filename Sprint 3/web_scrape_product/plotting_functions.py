import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import datetime as dt


def get_num_chars_in_time_frame(user, is_additions, start_time, end_time):
    return sum(edit.num_chars for edit in user.edits if edit.is_add is is_additions and start_time <= edit.time <= end_time)


def plot_pie_chart(users, is_additions, start_time, end_time):
    """
    Creates and plots the pie chart
    :param users: A list of User class instances
    :param is_additions: Boolean to determine whether we plot additions or deletions (True if additions)
    :return: None
    :postcondition: pie chart for number of revisions per user will be plotted
    """
    fig = plt.figure()
    amounts = [get_num_chars_in_time_frame(user, is_additions, start_time, end_time) for user in users]
    legend_array = [users[i].name for i in range(len(users)) if amounts[i] > 0]
    amounts = [amount for amount in amounts if amount > 0]
    plt.pie(amounts, labels=amounts)
    plt.title("Number of characters added by users")
    plt.legend(legend_array)
    return fig


def plot_line_info(user, start_time, end_time, num_sections, is_additions):
    """

    :param user: A User class instance
    :param start_time (datetime): Time at which to start measuring changes
    :param end_time (datetime): Time at which to stop measuring changes
    :param num_sections (integer): The number of 6hr slots between start and end
    :param is_additions (boolean): Measuring additions or deletions
    :return: A list containing the number of revisions made by the user in each 6hr interval
    """
    num_revs_list = num_sections * [0]
    current_time = start_time
    edits = [edit for edit in user.edits]
    index = 0

    #Deletes Edits outside of user specified time range so that they arent added to the line graphs
    while len(edits) > 0 and edits[-1].time < start_time:
        edits.pop()

    while current_time < end_time:
        while len(edits) > 0 and current_time <= edits[-1].time <= current_time + dt.timedelta(hours=6):
            if edits[-1].is_add is is_additions:
                num_revs_list[index] += edits[-1].num_chars
            edits.pop()
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
    fig = plt.figure()
    num_sections = int(((end_time - start_time) / dt.timedelta(hours=6) + 1) // 1)
    time_axis = num_sections * [0]
    time_axis[0] = start_time
    for i in range(1, num_sections):
        time_axis[i] = start_time + i*dt.timedelta(hours=6)
    for user in users:
        plt.plot(time_axis, plot_line_info(user, start_time, end_time, num_sections, is_additions), alpha=0.5)
    plt.xlabel("Date and hour")
    plt.ylabel("Number of characters")
    plt.gcf().autofmt_xdate()
    plt.legend([user.name for user in users], loc='upper right')
    if is_additions:
        plt.title("Number of characters added by each user at given times")
    else:
        plt.title("Number of characters deleted by each user at given times")
    return fig


def save_all_plots(plot_figures, file_name):
    """

    :param plot_figures: Array of figure objects
    :param file_name: Name of pdf file, e.g. 'test.pdf'
    :return:
    """
    file = PdfPages(filename=file_name)
    for figure in plot_figures:
        file.savefig(figure)
    file.close()


