class PD:
    # Constructor for PD
    def __init__(self, p, d, max_return=-1): 
        self.p = p
        self.d = d
        self.max_return = max_return
        self.last_diff = 0

    # Calculate output based on current and target value
    def calc(self, value, target): 
        diff = target - value                                           # difference between target and current value
        r_value = self.p * diff + self.d * (self.last_diff - diff)      # calculate return value
        self.last_diff = diff                                           # save current diff for next cycle (necessary for d part)
        
        if (abs(r_value) > self.max_return) and (self.max_return > 0):  # check for max value
            r_value = r_value / abs(r_value) * self.max_return
            
        return r_value