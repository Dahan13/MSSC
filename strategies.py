## IMPORT ##
############

def strategy_application(system, condition) :
    new_missions = []
    available_teams = []
    available_turbines = []
    for t in system.get_teams() :
        if t.get_availability() :
            available_teams.append(t)
    for t in system.get_turbines() :
        if t.get_availability() :
            available_turbines.append(t)
    for t in available_turbines :
        if len(available_teams) > 0 :
            if condition(system, t) :
                new_missions.append((t.get_id(), available_teams.pop().get_id()))
        else :
            break
    return new_missions

"""
            State   1   2   3   4   M
Production
0% - 100%           N   N   N   Y   N
"""
def condition_A(system, turbine) :
    state = turbine.get_state()
    return state == 4
def strategy_A(system) :
    return strategy_application(system, condition_A)

"""
            State   1   2   3   4   M
Production
0% - 70%            N   N   Y   Y   N
70% - 90%           N   N   N   Y   N
90% - 100%          N   N   N   N   N
"""
def condition_B(system, turbine) :
    state = turbine.get_state()
    ratio = turbine.get_operating_days_count()/system.get_days_count()
    return (state == 4 and ratio < 0.9) or (state == 3 and ratio < 0.7)
def strategy_B(system) :
    return strategy_application(system, condition_B)
