class User:

    def __init__(self, name, colour):
        """
        :param name: The English name of the user
        :param name: The colour of the users' icon as a 3-tuple
        """
        self.name = name
        self.colour = colour
        self.revisions = []
        self.num_added = 0
        self.num_deleted = 0

    def add_revision(self, revision):
        self.revisions.append(revision)
        if revision.is_add:
            self.num_added += revision.num_chars
        else:
            self.num_deleted += revision.num_chars


class Edit:

    def __init__(self, time, content, is_add):
        """

        :param content (Integer): Characters added/deleted by user (including spaces)
        :param time (Datetime): Time at which revision was made
        :param is_add (Boolean): Whether revision was an addition or deletion
        """
        self.content = content
        self.time = time
        self.is_add = is_add
        self.num_chars = len(content.replace(" ", ""))


