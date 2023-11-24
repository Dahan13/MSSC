## IMPORT ##
import random

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
    def next_day(self, strategy) :
        self.days_count += 1
        self.wind = weather_forecast(self.wind)
        missions_to_launch = strategy(self)
        for m in missions_to_launch :
            self.planning.new_mission(m[0], m[1])
            for t in self.teams :
                if t.get_id() == m[1] :
                    t.new_mission()
                    self.total_cost += 50000
            for t in self.turbines :
                if t.get_id() == m[0] :
                    t.new_mission()
        update_info = self.planning.make_progress(self.wind)
        turbines_repared = [u['turbine'] for u in update_info]
        teams_availabled = [u['team'] for u in update_info]
        for t in self.turbines :
            if t.get_id() in turbines_repared :
                t.repair()
                t.end_mission()
        for t in self.teams :
            if t.get_id() in teams_availabled :
                t.end_mission()
        for t in self.turbines :
            if t.get_availability() :
                self.total_prod += t.produce(self.wind)
        for t in self.turbines :
            t.damage(self.wind)
    def get_turbines(self) :
        return self.turbines
    def get_teams(self) :
        return self.teams
    def get_planning(self) :
        return self.planning
    def get_wind(self) :
        return self.wind
    def get_days_count(self) :
        return self.days_count
    def get_total_prod(self) :
        return self.total_prod
    def get_total_cost(self) :
        return self.total_cost 
    def get_wind_memory(self) :
        return self.wind_memory