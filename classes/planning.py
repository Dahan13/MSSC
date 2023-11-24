## IMPORT ##
############


class Mission:
    def __init__(self, turbine, team):
        """
        Creates a mission for a maintenance crew to repair a turbine.

        Attributes:
            turbine: int = turbine id
            team: int = team id
            progress: int = mission progress. 0 = mission not started, 1 = mission preparation day 1, 2 = mission preparation day 2, 3 = mission intervention day 1, 4 = mission intervention day 2, 5 = mission completed
        """

        self.turbine = turbine
        self.team = team
        self.progress = 0

    def get_team(self):
        """Returns the team id."""
        return self.team

    def get_turbine(self):
        """Returns the turbine id."""
        return self.turbine

    def get_progress(self):
        """Returns the mission progress. 0 = mission not started, 1 = mission preparation day 1, 2 = mission preparation day 2, 3 = mission intervention day 1, 4 = mission intervention day 2, 5 = mission completed"""
        return self.progress

    def get_info(self):
        """Returns a dictionary containing the mission infos"""
        return {"team": self.team, "turbine": self.turbine, "progress": self.progress}

    def make_progress(self, wind):
        """Makes the mission progress by a day by taking into account the wind. Returns the new mission progress."""
        if self.progress < 2:
            self.progress += 1
        else:
            if wind < 3: # if there is strong wind, intervention is not possible and is delayed
                self.progress += 1
        return self.progress


class Planning:

    def __init__(self):
        """Creates an empty planning that will contains all maintenance missions.

        Attributes:
            missions: list = list of all missions underway
        """

        self.missions = []

    def get_missions(self):
        """Returns the list of all missions underway."""
        return self.missions

    def get_attribution(self):
        """Returns a list of all missions underway with a tuple of their team and turbine."""
        for mission in self.missions:
            yield (mission.get_team(), mission.get_turbine())

    def new_mission(self, turbine, team):
        """Creates a new mission for a given maintenance crew to repair a given turbine."""
        self.missions.append(Mission(turbine, team))

    def make_progress(self, wind):
        """Makes all missions progress by a day by calling their make_progress methods. Returns a list of all missions that have been completed."""
        i = 0
        update = []
        # We check for each mission if it is completed or not
        while i < len(self.missions):
            res = self.missions[i].make_progress(wind)
            if res == 5:
                update.append(self.missions[i].get_info())
                self.missions.pop(i)
            else: # if the mission is not completed, we go to the next one
                i += 1
        return update
