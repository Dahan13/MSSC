## IMPORT ##
import time
import random
from planning import *
from turbine import *
from team import *
############

def evelyne_dheliat(wind) :
    r = random.random()
    match wind :
        case 1 :
            if r < 0.2 :
                return 1
            elif r < 0.93 :
                return 2
            else :
                return 3
        case 2 :
            if r < 0.11 :
                return 1
            elif r < 0.85 :
                return 2
            else :
                return 3
        case 3 :
            if r < 0.04 :
                return 1
            elif r < 0.65 :
                return 2
            else :
                return 3

def maintenance_strategy(turbines, teams) :
    new_missions = []
    available_teams = []
    for t in teams :
        if t.get_availability() :
            available_teams.append(t)
    for t in turbines :
        if t.get_state() == 4 :
            if len(available_teams) > 0 :
                new_missions.append((t.get_id(), available_teams.pop().get_id()))
        if len(available_teams) == 0 :
            break
    return new_missions

class System :
    def __init__(self, N_turbines, N_teams) :
        self.turbines = [Turbine(i) for i in range(1, N_turbines+1)]
        self.teams = [Team(i) for i in range(1, N_teams+1)]
        self.planning = Planning()
        self.wind = 1
        self.days_count = 0
        self.total_prod = 0
        self.total_cost = N_teams * 100000
        self.wind_memory = []
    def next_day(self) :
        self.days_count += 1

        # update wind
        self.wind = evelyne_dheliat(self.wind)
        self.wind_memory.append(self.wind)

        # add new maintenance mission
        missions_to_launch = maintenance_strategy(self.turbines, self.teams)
        for m in missions_to_launch :
            self.planning.add_mission(m[0], m[1])
            for t in self.teams :
                if t.get_id() == m[1] :
                    t.new_mission()
                    self.total_cost += 50000

        # update all maintenance mission
        update_info = self.planning.make_progress(self.wind)
        turbines_repared = [u['turbine'] for u in update_info]
        teams_availabled = [u['team'] for u in update_info]

        for t in self.turbines :
            if t.get_id() in turbines_repared :
                t.repare()
        for t in self.teams :
            if t.get_id() in teams_availabled :
                t.end_mission()

        # unavailable turbines
        unavailable_turbines = self.planning.get_unavailable_turbines()

        # turbine production
        for t in self.turbines :
            if not(t.get_id() in unavailable_turbines) :
                self.total_prod += t.produce(self.wind)

        # turbine damage
        for t in self.turbines :
            t.damage(self.wind)

    def display(self) :
        print("System Current Information")
        print("Day %d"%(self.days_count))
        print("Turbine")
        for t in self.turbines :
            t.display()
        print("Teams")
        for t in self.teams :
            t.display()
        print("Planning")
        self.planning.display()
        print("Total")
        print("Prod : %d"%(self.total_prod))
        print("Cost : %d"%(self.total_cost))

## TEST ##

NUMBER_OF_TURBINES = 20
NUMBER_OF_TEAMS = 5
NUMBER_OF_DAYS = 100

system = System(NUMBER_OF_TURBINES, NUMBER_OF_TEAMS) 
for k in range(NUMBER_OF_DAYS) :
    system.next_day()
    if k%10 == 9 :
        system.display()
        time.sleep(5)

##########