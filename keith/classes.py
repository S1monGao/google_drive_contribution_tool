class User:

    def __init__(self, name):
        """
        :param name: The English name of the user
        :attribute times: A list of times at which the user made revisions
        :attribute num_rev: The total number of revisions made by a user
        """
        self.name = name
        self.times = []
        self.num_rev = 0

    def __str__(self):
        string_to_return = "--------\n"
        string_to_return += self.name + "\n"
        string_to_return += str(self.times)
        return string_to_return

class User_v2:

    def __init__(self, name):
        """
        :param name: The English name of the user
        :attribute times: A list of times at which the user made revisions
        :attribute num_rev: The total number of revisions made by a user
        """
        self.name = name
        self.revisions = []
        self.num_added = 0
        self.num_deleted = 0

    def add_revision(self, revision):
        self.revisions.append(revision)
        if revision.is_add:
            self.num_added += revision.num_chars
        else:
            self.num_deleted += revision.num_chars


class Revision:

    def __init__(self, num_chars, time, is_add=True):
        self.num_chars = num_chars
        self.time = time
        self.is_add = is_add

