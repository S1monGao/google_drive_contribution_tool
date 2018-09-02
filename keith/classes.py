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
