## IMPORT ##
############

def strategy_A(system) :
    turbines = system.get_turbines()
    teams = system.get_teams()
    new_missions = []
    available_teams = []
    available_turbines = []
    for t in teams :
        if t.get_availability() :
            available_teams.append(t)
    for t in turbines :
        if t.get_availability() :
            available_turbines.append(t)
    for t in available_turbines :
        if len(available_teams) > 0 :
            if t.get_state() == 4 :
                new_missions.append((t.get_id(), available_teams.pop().get_id()))
        else :
            break
    return new_missions

def strategy_B(system) :
    turbines = system.get_turbines()
    teams = system.get_teams()
    days = system.get_days_count()
    new_missions = []
    available_teams = []
    available_turbines = []
    for t in teams :
        if t.get_availability() :
            available_teams.append(t)
    for t in turbines :
        if t.get_availability() :
            available_turbines.append(t)
    for t in available_turbines :
        if len(available_teams) > 0 :
            if (t.get_state() == 4 and t.get_operating_days_count()/days < 0.9) or (t.get_state() == 3 and t.get_operating_days_count()/days < 0.7) :
                new_missions.append((t.get_id(), available_teams.pop().get_id()))
        else :
            break
    return new_missions