## IMPORT ##
import random

############

MAINTENANCE = 0
PRODUCTION = 1

class Turbine:
    def __init__(self, id):
        """
        Initialize a turbine with its id.

        Attributes:
            id: int = turbine id
            state: int = turbine state. 1 = new, 2 = slightly damaged, 3 = moderately damaged, 4 = heavily damaged
            availability: int = turbine availability. 0 = in maintenance, 1 = producing energy
            operating_days_count: int = number of days the turbine has been operating
        """
        self.id = id
        self.state = 1
        self.availability = PRODUCTION
        self.operating_days_count = 0

    def get_id(self):
        """Returns the turbine id."""
        return self.id

    def get_state(self):
        """Returns the turbine state. 1 = new, 2 = slightly damaged, 3 = moderately damaged, 4 = heavily damaged"""
        return self.state

    def get_availability(self):
        """Returns the turbine availability. 0 = in maintenance, 1 = producing energy"""
        return self.availability

    def get_operating_days_count(self):
        """Returns the number of days the turbine has been operating"""
        return self.operating_days_count

    def new_mission(self):
        """Put the turbine in maintenance mode when a maintenance starts."""
        self.availability = MAINTENANCE

    def end_mission(self):
        """Put the turbine in production mode when a maintenance end."""
        self.availability = PRODUCTION

    def repair(self):
        """Repair the turbine."""
        self.state = 1

    def produce(self, wind):
        """Returns energy produced by the turbine depending on the wind speed."""
        match wind:
            case 1: # if there is no wind, no energy is produced
                return 0
            case 2: # if there is medium wind and the turbine is not destroyed, it produces a medium amount of energy
                if self.state < 4:
                    self.operating_days_count += 1
                    return 1
            case 3: # if there is a strong wind and the turbine is not heavily damaged, it produces a large amount of energy. It produces a medium amount of energy if the turbine is moderately damaged
                if self.state < 3:
                    self.operating_days_count += 1
                    return 2
                elif self.state == 3:
                    self.operating_days_count += 1
                    return 1
        return 0

    # medium_wind_damage_probabilities = [
    #     [0.95, 0.05, 0, 0],
    #     [0, 0.94, 0.05, 0.01],
    #     [0, 0, 0.86, 0.14],
    #     [0, 0, 0, 1]
    # ]

    # heavy_wind_damage_probabilities = [
    #     [0.9, 0.09, 0.01, 0],
    #     [0, 0.87, 0.11, 0.02],
    #     [0, 0, 0.79, 0.21],
    #     [0, 0, 0, 1]
    # ]

    def damage(self, wind):
        """Damage the turbine depending on the wind speed and the state of the turbine."""
        r = random.random()
        match wind:
            case 2:
                match self.state:
                    case 1:
                        if r >= 0.95:
                            self.state = 2
                    case 2:
                        if r >= 0.94 and r < 0.99:
                            self.state = 3
                        elif r >= 0.99:
                            self.state = 4
                    case 3:
                        if r >= 0.86:
                            self.state = 4
            case 3:
                match self.state:
                    case 1:
                        if r >= 0.9 and r < 0.99:
                            self.state = 2
                        elif r >= 0.99:
                            self.state = 3
                    case 2:
                        if r >= 0.87 and r < 0.98:
                            self.state = 3
                        elif r >= 0.98:
                            self.state = 4
                    case 3:
                        if r >= 0.79:
                            self.state = 4
