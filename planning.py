

# Team : 1 .. T
# Turbine : 1 .. 20
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
    def display(self) :
        c = ""
        for i, el in enumerate(self.missions) :
            c += "%d - Team %2d is working on Turbine %2d \tProgress : %d / 5\n"%(i,self.missions[i].get_team(),self.missions[i].get_turbine(),self.missions[i].get_progress())
        return c
    
########## TEST ##########

planning = Planning()
planning.add_mission(5, 15)
planning.make_progress(2)
planning.add_mission(2, 6)
planning.make_progress(2)
planning.make_progress(3)
planning.make_progress(1)
planning.add_mission(1, 5)
planning.make_progress(3)
print(planning.display())