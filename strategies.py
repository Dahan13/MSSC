## IMPORT ##
############

from ast import main


def strategy_application(system, condition):
    """Returns a list of new missions for a given system depending on the chosen conditions."""
    new_missions = []

    # We begin by retrieving all available teams and functioning turbines
    available_teams = system.get_available_teams()
    available_turbines = []
    for t in system.get_turbines():
        if t.get_availability():
            available_turbines.append(t)

    # Now for each turbine, we check if it meets the condition to start the maintenance and if there are still available teams
    for t in available_turbines:
        if len(available_teams) > 0:
            if condition(system, t):
                new_missions.append((t.get_id(), available_teams.pop().get_id()))
        else: # if there are no more available teams, we stop the loop
            break
    return new_missions


"""
            State   1   2   3   4   M
Production
0% - 100%           N   N   N   Y   N
"""


def condition_A(system, turbine):
    """Returns True if the turbine is heavily damaged and False otherwise."""
    state = turbine.get_state()
    return state == 4


def strategy_A(system):
    """Returns a list of new missions for a given system depending on condition_A."""
    return strategy_application(system, condition_A)


"""
            State   1   2   3   4   M
Production
0% - 70%            N   N   Y   Y   N
70% - 90%           N   N   N   Y   N
90% - 100%          N   N   N   N   N
"""


def condition_B(system, turbine):
    """Returns True if the turbine is moderately damaged and operated for less than 70% of the time or if the turbine is heavily damaged and operated for less than 90% of the time.
    It returns false otherwise"""
    state = turbine.get_state()
    ratio = turbine.get_operating_days_count() / system.get_days_count()
    return (state == 4 and ratio < 0.9) or (state == 3 and ratio < 0.7)


def strategy_B(system):
    """Returns a list of new missions for a given system depending on condition_B."""
    return strategy_application(system, condition_B)

"""
            State   1   2   3   4   M
Wind Speed
1                   N   N   Y   Y   N
2                   N   N   N   Y   N
3                   N   N   Y   Y   N
"""


def condition_C(system, turbine):
    """Returns True if the turbine is moderately or heavily damaged and wind speed is high or non-existant. Returns True if the turbine is heavily damaged and wind speed is medium."""
    state = turbine.get_state()
    wind_speed = system.get_wind()
    return (state == 4) or (state >= 3 and wind_speed != 2)


def strategy_C(system):
    """Returns a list of new missions for a given system depending on condition_C."""
    return strategy_application(system, condition_C)

"""
                            State   1   2   3   4   M
Maintenance availability
>= 90%                              N   Y   Y   Y   N
>= 40% and < 90%                    N   N   Y   Y   N
< 40%                               N   N   N   Y   N
"""


def condition_D(system, turbine):
    """Returns True if turbine is slightly or more damaged and 90% of maintenace crews are available, or if the turbine is moderately or more damaged and between 40 and 90% of maintenance crews are available. 
    Returns also True if less than 40% of maintenance crew is available but the turbine is heavily damaged. Returns False otherwise."""
    state = turbine.get_state()
    maintenance_crew_availability = system.get_maintenance_crew_availability()
    return (state >= 2 and maintenance_crew_availability >= 0.9) or (state >= 3 and maintenance_crew_availability >= 0.4) or (state == 4 and maintenance_crew_availability < 0.4)


def strategy_D(system):
    """Returns a list of new missions for a given system depending on condition_D."""
    return strategy_application(system, condition_D)
