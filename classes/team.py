## IMPORT ##
############

WAITING = 1
WORKING = 0


class Team:
    def __init__(self, id):
        """
        Initialize a maintenance team with its id.


        Attributes:
            id: int = team id
            availability: int = team availability. 0 = working, 1 = ready for a new assignment
        """

        self.id = id
        self.availability = WAITING

    def get_id(self):
        """Returns the team id."""
        return self.id

    def get_availability(self):
        """Returns the team availability. 0 = working, 1 = ready for a new assignment"""
        return self.availability

    def new_mission(self):
        """Put the team in working mode when a maintenance starts."""
        self.availability = WORKING

    def end_mission(self):
        """Put the team in waiting mode when a maintenance end."""
        self.availability = WAITING
