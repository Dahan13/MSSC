## IMPORT ##
import time
import random
import clear_cache 

from strategies import *
from classes.planning import *
from classes.turbine import *
from classes.team import *
############

def weather_forecast(wind) :
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
    def get_day(self) :
        return self.days_count
    def next_day(self) :
        self.days_count += 1
        # update wind
        self.wind = weather_forecast(self.wind)
        self.wind_memory.append(self.wind)
        # add new maintenance mission
        missions_to_launch = basic_strategy(self.turbines, self.teams, self.planning)
        for m in missions_to_launch :
            self.planning.new_mission(m[0], m[1])
            for t in self.teams :
                if t.get_id() == m[1] :
                    t.new_mission()
                    self.total_cost += 50000
            for t in self.turbines :
                if t.get_id() == m[0] :
                    t.new_mission()
        # update all maintenance mission
        update_info = self.planning.make_progress(self.wind)
        turbines_repared = [u['turbine'] for u in update_info]
        teams_availabled = [u['team'] for u in update_info]
        for t in self.turbines :
            if t.get_id() in turbines_repared :
                t.repare()
                t.end_mission()
        for t in self.teams :
            if t.get_id() in teams_availabled :
                t.end_mission()
        # turbine production
        for t in self.turbines :
            if t.get_availability() :
                self.total_prod += t.produce(self.wind)
        # turbine damage
        for t in self.turbines :
            t.damage(self.wind)
    def display(self) :
        print("System Current Information")
        print("Day %d"%(self.days_count))
        print("==Turbine===")
        for t in self.turbines :
            t.display()
        print("==Teams=====")
        for t in self.teams :
            t.display()
        print("==Planning==")
        self.planning.display()
        print("==Total=====")
        print("Prod : %d"%(self.total_prod))
        print("Cost : %d"%(self.total_cost))
        print("="*30)
    def display_txt(self) :
        c = "System Current Information"+"\n"
        c += "Day %d"%(self.days_count)+"\n"
        c += "==Turbine==="+"\n"
        for t in self.turbines :
            c += t.display_txt()+"\n"
        c += "==Teams====="+"\n"
        for t in self.teams :
            c += t.display_txt()+"\n"
        c += "==Planning=="+"\n"
        c += self.planning.display_txt()+"\n"
        c += "==Total====="+"\n"
        c += "Prod : %d"%(self.total_prod)+"\n"
        c += "Cost : %d"%(self.total_cost)+"\n"
        c += "="*30+"\n"
        return c
clear_cache.clear()