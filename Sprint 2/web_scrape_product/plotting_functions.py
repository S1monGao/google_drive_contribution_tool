import matplotlib.pyplot as plt


def plot_pie_chart(users, is_additions):
    """
    Creates and plots the pie chart
    :param users: A list of User class instances
    :param is_additions: Boolean to determine whether we plot additions or deletions (True if additions)
    :return: None
    :postcondition: pie chart for number of revisions per user will be plotted
    """
    if is_additions:
        amounts = [user.num_added for user in users]
        plt.title("Number of characters added by users")
    else:
        amounts = [user.num_deleted for user in users if user.num_deleted > 0]
        plt.title("Number of characters deleted by users")
    plt.pie(amounts)
    plt.legend([user.name for user in users])
    plt.show()
