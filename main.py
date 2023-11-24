## IMPORT ##
import random

from strategies import *
from classes.planning import *
from classes.turbine import *
from classes.team import *

############


def weather_forecast(wind):
    """Returns the wind speed for the next day depending on the wind speed of the current day."""
    r = random.random()
    match wind:
        case 1:
            if r >= 0.2 and r < 0.93:
                return 2
            elif r >= 0.93:
                return 3
        case 2:
            if r < 0.11:
                return 1
            elif r >= 0.85:
                return 3
        case 3:
            if r < 0.04:
                return 1
            elif r < 0.65:
                return 2
    return wind


class System:
    def __init__(self, N_turbines, N_teams):
        """
        Creates the system with N_turbines turbines and N_teams teams.

        Attributes:
            turbines: list = list of all turbines
            teams: list = list of all teams
            planning: Planning = planning of all undergoing missions
            wind: int = wind speed
            days_count: int = number of days since the beginning of the simulation
            total_prod: int = total energy produced since the beginning of the simulation
            total_cost: int = total cost since the beginning of the simulation
        """
        self.turbines = [Turbine(i) for i in range(1, N_turbines + 1)]
        self.teams = [Team(i) for i in range(1, N_teams + 1)]
        self.planning = Planning()
        self.wind = 1
        self.days_count = 0
        self.wind_days_count = 0
        self.total_prod = 0
        self.total_cost = N_teams * 100000

    def next_day(self, strategy):
        """Makes the system progress by a day by taking into account the strategy."""
        self.days_count += 1

        # if it's a new year, we pay the maintenance teams yearly fee
        if self.days_count % 365 == 0:
            self.total_cost += len(self.teams) * 100000

        # We update the wind speed for the next day
        self.wind = weather_forecast(self.wind)

        if self.wind > 1 :
            self.wind_days_count += 1

        # We decide which missions to launch according to the strategy
        missions_to_launch = strategy(self)

        # We launch the missions
        for m in missions_to_launch:
            self.planning.new_mission(m[0], m[1])

            # We search & set the corresponding team in maintenance mode
            for t in self.teams:
                if t.get_id() == m[1]:
                    t.new_mission()
                    self.total_cost += 50000

            # We search & set the corresponding turbine in maintenance mode
            for t in self.turbines:
                if t.get_id() == m[0]:
                    t.new_mission()

        # We make the maintenance missions progress for the day
        update_info = self.planning.make_progress(self.wind)

        # We retrive all turbines and teams that just finished their maintenance operation
        turbines_repared = [u["turbine"] for u in update_info]
        teams_availabled = [u["team"] for u in update_info]

        # We update these turbines and teams to be available for the next day
        for t in self.turbines:
            if t.get_id() in turbines_repared:
                t.repair()
                t.end_mission()
        for t in self.teams:
            if t.get_id() in teams_availabled:
                t.end_mission()

        # We make all the available turbines produce their energy for the day
        for t in self.turbines:
            if t.get_availability():
                self.total_prod += t.produce(self.wind)

        # We update all turbines states depending of the wind
        for t in self.turbines:
            t.damage(self.wind)

        for t in self.teams:
            if not(t.get_availability()) :
                t.work()

    def get_turbines(self):
        """Returns the list of all turbines."""
        return self.turbines

    def get_teams(self):
        """Returns the list of all teams."""
        return self.teams

    def get_planning(self):
        """Returns the mission planning."""
        return self.planning

    def get_wind(self):
        """Returns the wind speed."""
        return self.wind

    def get_days_count(self):
        """Returns the number of days since the beginning of the simulation."""
        return self.days_count

    def get_total_prod(self):
        """Returns the total energy produced since the beginning of the simulation."""
        return self.total_prod

    def get_total_cost(self):
        """Returns the total cost since the beginning of the simulation."""
        return self.total_cost

    def get_team_occupation_percentage(self) :
        l = [t.get_operating_days_count() for t in self.teams]
        s = 0
        for x in l :
            s += x/self.wind_days_count if self.days_count != 0 else 0
        return 100*s/len(self.teams) 
    
    def get_turbine_occupation_percentage(self) :
        l = [t.get_operating_days_count() for t in self.turbines]
        s = 0
        for x in l :
            s += x/self.wind_days_count if self.days_count != 0 else 0
        return 100*s/len(self.turbines)
    