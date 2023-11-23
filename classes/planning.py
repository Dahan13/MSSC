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
    def __init__(self, turbine, team) :
        self.turbine = turbine
        self.team = team
        self.progress = 0
    def get_team(self) :
        return self.team
    def get_turbine(self) :
        return self.turbine
    def get_progress(self) :
        return self.progress
    def get_info(self) :
        return {"team":self.team,"turbine":self.turbine,"progress":self.progress}
    def make_progress(self, wind) :
        if self.progress < 2 : 
            self.progress += 1
        else :
            if wind < 3 :
                self.progress += 1
        return self.progress

class Planning :
    def __init__(self) :
        self.missions = []
    def get_missions(self) :
        return self.missions
    def get_attribution(self) :
        for mission in self.missions :
            yield (mission.get_team(), mission.get_turbine())
    def new_mission(self, turbine, team) :
        self.missions.append(Mission(turbine, team))
    def make_progress(self, wind) :
        i = 0
        update = []
        while i < len(self.missions) :
            res = self.missions[i].make_progress(wind)
            if res == 5 :
                update.append(self.missions[i].get_info())
                self.missions.pop(i)
            else :
                i += 1
        return update