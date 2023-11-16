## IMPORT ##
############

# Wind : 1 .. 3
#   1 - LOW
#   2 - MEDIUM
#   3 - HIGH

# Progress : 1 .. 5
#   0 - Plannification - Day 1
#   1 - Plannification - Day 2
#   2 - Maintenance - Day 3
#   3 - Maintenance - Day 4
#   4 - Maintenance - Day 5

class Mission :
    def __init__(self, team, turbine) :
        self.team = team
        self.turbine = turbine
        self.progress = 0
    def make_progress(self, wind) :
        if self.progress == 0 : 
            self.progress += 1
        else :
            if wind < 3 :
                self.progress += 1
                if self.progress == 5 :
                    return 1
        return 0
    def get_info(self) :
        return {"team":self.team,"turbine":self.turbine,"progress":self.progress}
    def get_team(self) :
        return self.team
    def get_turbine(self) :
        return self.turbine
    def get_progress(self) :
        return self.progress

class Planning :
    def __init__(self) :
        self.missions = []
    def add_mission(self, team, turbine) :
        self.missions.append(Mission(team, turbine))
    def get_mission(self) :
        return self.missions
    def make_progress(self, wind) :
        i = 0
        update = []
        while i < len(self.missions) :
            res = self.missions[i].make_progress(wind)
            if res == 1 :
                update.append(self.missions[i].get_info())
                self.missions.pop(i)
            else :
                i += 1
        return update
    def get_unavailable_turbines(self) :
        return [m.get_turbine() for m in self.missions]
    def display(self) :
        c = ""
        for i, el in enumerate(self.missions) :
            c += "%d - Team %2d is working on Turbine %2d \tProgress : %d / 5\n"%(i,self.missions[i].get_team(),self.missions[i].get_turbine(),self.missions[i].get_progress())
        return c