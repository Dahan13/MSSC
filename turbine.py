class Turbine:


    def __init__(self):
        """Initialize a wind turbine object with default values
        
        Attributes:
            - state: 1 = very good condition, 2 = good condition, 3 = bad condition, 4 = very bad condition
            - maintenance: 0 = no maintenance, 1, 2 = preparation of maintenance, 3, 4, 5 = in maintenance
            - operating_days_count: number of days the turbine has been operating
        """
        self.state = 1
        self.maintenance = 0
        self.operating_days_count = 0

    def get_state(self):
        """Returns the state of the wind turbine"""
        return self.state
    
    def update_state(self, state):
        """Updates the state of the wind turbine"""
        if state < 1 or state > 4:
            raise ValueError("State must be between 1 and 4")
        self.state = state

    def get_maintenance(self):
        """Returns the maintenance status of the wind turbine"""
        return self.maintenance
    
    def update_maintenance(self, maintenance):
        """Updates the maintenance status of the wind turbine"""
        if maintenance < 0 or maintenance > 5:
            raise ValueError("Maintenance must be between 0 and 5")
        
        # If the turbine reach end of maintenance, it goes back to state 1
        if maintenance == 5:
            self.state = 1
            self.maintenance = 0
        else:
            self.maintenance = maintenance

    def increment_operating_days(self):
        """Increments the operating days count of the wind turbine"""
        self.operating_days_count += 1

    def is_usable(self):
        """Returns True if the turbine is usable, False otherwise"""
        return self.state < 4 and self.maintenance <= 2
    
    def calculate_output(self, wind):
        if (wind == 3 and self.state <= 2):
            self.increment_operating_days()
            return 2
        elif (wind == 2 and self.is_usable()):
            self.increment_operating_days()
            return 1
        else:
            return 0
    
    def calculate_productivity(self, windy_days_count):
        return self.operating_days_count / windy_days_count