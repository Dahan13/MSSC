## IMPORT ##
############

def basic_strategy(turbines, teams, planning) :
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