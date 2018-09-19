import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import datetime as dt


def plot_pie_chart(users, is_additions):
    """
    Creates and plots the pie chart
    :param users: A list of User class instances
    :param is_additions: Boolean to determine whether we plot additions or deletions (True if additions)
    :return: None
    :postcondition: pie chart for number of revisions per user will be plotted
    """
    fig = plt.figure()
    if is_additions:
        amounts = [user.num_added for user in users if user.num_added > 0]
        plt.pie(amounts)
        plt.title("Number of characters added by users")
        plt.legend([user.name for user in users if user.num_added > 0])
    else:
        amounts = [user.num_deleted for user in users if user.num_deleted > 0]
        plt.pie(amounts)
        plt.title("Number of characters deleted by users")
        plt.legend([user.name for user in users if user.num_deleted > 0])
    plt.show()
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
    fig, ax = plt.subplots()
    num_sections = int(((end_time - start_time) / dt.timedelta(hours=6) + 1) // 1)
    time_axis = num_sections * [0]
    time_axis[0] = start_time
    for i in range(1, num_sections):
        time_axis[i] = start_time + i*dt.timedelta(hours=6)
    for user in users:
        ax.plot(time_axis, plot_line_info(user, start_time, end_time, num_sections, is_additions))
    plt.xlabel("Date and hour")
    plt.ylabel("Number of characters")
    ax.xaxis_date()  # interpret the x-axis values as dates
    fig.autofmt_xdate()
    if is_additions:
        plt.legend([user.name for user in users if user.num_added > 0], loc='upper right')
        plt.title("Number of characters added by each user at given times")
    else:
        plt.legend([user.name for user in users if user.num_deleted > 0], loc='upper right')
        plt.title("Number of characters deleted by each user at given times")
    plt.show()
    return fig


def save_all_plots(plot_figures, file_name):
    file = PdfPages(filename=file_name)
    for figure in plot_figures:
        file.savefig(figure)
    file.close()


