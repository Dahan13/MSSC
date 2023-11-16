## IMPORT ##
############

WAITING = 1
WORKING = 0

class Team :
    def __init__(self, id) :
        self.id = id
        self.state = WAITING
    def get_id(self) :
        return self.id
    def get_availability(self) :
        return self.state
    def new_mission(self) :
        self.state = WORKING
    def end_mission(self) :
        self.state = WORKING
    def display(self) :
        print("Team %d is currently %s"%(self.id, "WORKING" if self.state == WORKING else "WAITING"))