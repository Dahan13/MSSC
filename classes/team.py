## IMPORT ##
############

WAITING = 1
WORKING = 0

class Team :
    def __init__(self, id) :
        self.id = id
        self.availability = WAITING
    def get_id(self) :
        return self.id
    def get_availability(self) :
        return self.availability
    def new_mission(self) :
        self.availability = WORKING
    def end_mission(self) :
        self.availability = WAITING