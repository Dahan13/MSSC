## IMPORT ##
import random
############

# Wind : 1 .. 3
#   1 - LOW
#   2 - MEDIUM
#   3 - HIGH

# State : 1 .. 4
#   1 - No Defects
#   2 - Small Defects
#   3 - Important Defects
#   4 - Non Functional

def damage_calculator(wind, state) :
    r = random.random()
    match wind :
        case 1 :
            return state
        case 2 :
            match state :
                case 1 :
                    if r < 0.95 :
                        return 1
                    else :
                        return 2
                case 2 :
                    if r < 0.94 :
                        return 2
                    elif r < 0.99 :
                        return 3
                    else :
                        return 4
                case 3 :
                    if r < 0.84 :
                        return 3
                    else :
                        return 4
                case 4 :
                    return 4
        case 3 :
            match state :
                case 1 :
                    if r < 0.9 :
                        return 1
                    elif r < 0.99 :
                        return 2
                    else :
                        return 3
                case 2 :
                    if r < 0.87 :
                        return 2
                    elif r < 0.98 :
                        return 3
                    else :
                        return 4
                case 3 :
                    if r < 0.79 :
                        return 3
                    else :
                        return 4
                case 4 :
                    return 4
    return state

MAINTENANCE = 0
PRODUCTION = 1

class Turbine :
    def __init__(self, id) :
        self.id = id
        self.state = 1
        self.availability = PRODUCTION
        self.operating_days_count = 0
    def get_id(self) :
        return self.id
    def get_state(self) :
        return self.state
    def get_availability(self) :
        return self.availability
    def new_mission(self) :
        self.availability = MAINTENANCE
    def end_mission(self) :
        self.availability = PRODUCTION
    def repare(self) :
        self.state = 1
    def produce(self, wind) :
        match wind :
            case 1 : return 0
            case 2 : 
                if self.state < 4 :
                    self.operating_days_count += 1 
                    return 1
            case 3 :
                if self.state < 3 :
                    self.operating_days_count += 1
                    return 2
        return 0
    def damage(self, wind) :
        self.state = damage_calculator(wind, self.state)
    def display(self) :
        print("Turbine %d (state %d) - Production : %d"%(self.id,self.state,self.operating_days_count))