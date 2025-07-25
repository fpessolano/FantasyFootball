# SCRATCH FILE: Old attribute constants and definitions
# Contains outdated attribute management constants (training times, stat limits)
# Early iteration of player stats system with different time mechanics
# Not used in main application - replaced by newer attribute.py approach

ACTIVITY_TIME_UNIT_MINUTES = 5
TRAIN_TIME_UNIT_HOURS = 2
REST_TIME_UNIT_DAYS = 2
MINIMUM_STAT = 5.0
SEASON_DEFAULT_CAP = {"limit": 3.0, "daily_rate": 1.0, "cap": 0.9}
HOLIDAYS_DEFAULT_CAP = {"limit": 3.0, "daily_rate": 0.5, "cap": 0.75}


class Attribute:
    """
    Attibutes consistes of the following values:
    reference (0) : is the official (face) value
    current (1): the the actual value taking into consideration effects of activities
    maximum (2): is the the maximum value allowed due to activities
    __activity_modifier (3): the coefficient that affects attribute reduction per activity units as defined in ACTIVITY_TIME_UNIT_MINUTES
    __rest_modifier (4) : the coefficient that affects attribute reduction per rest units as defined in REST_TIME_UNIT_DAYS
    __train_modifier (5) : the coefficient that affects attribute reduction per rest units as defined in TRAIN_TIME_UNIT_HOURS    
    """

    def __init__(self, values: list[int]):
        if len(values) != 5:
            raise ValueError("Stats must have 5 values")
        self.reference = values[0]
        self.current = values[1]
        self.maximum = values[2]
        self.__activity_modifier = values[3]
        self.__rest_modifier = values[4]
        self.__train_modifier = values[5]

    def activity(self, intensity, time):
        # change it to affect reference (goes up) and current (goes down)
        current_value = self.current - self.__activity_modifier * (
            intensity / 2) * (time / ACTIVITY_TIME_UNIT_MINUTES)
        self.current = round(
            current_value) if current_value > MINIMUM_STAT else MINIMUM_STAT

    def rest(self, intensity, time):
        # change it to affect current (to refefence) and if too long resting affects current and reference (both down)
        # long rest also covers injury
        current_value = self.current + self.__rest_modifier * (
            intensity / 2) * (time / REST_TIME_UNIT_DAYS)
        self.current = round(
            current_value) if current_value < self.maximum else self.maximum

    def train(self, intensity, time):
        # change it to affect reference (goes up) and current (goes down)
        current_value = self.current + self.__train_modifier * (
            intensity / 2) * (time / TRAIN_TIME_UNIT_HOURS)
        self.current = round(
            current_value) if current_value < self.maximum else self.maximum


class Attributes:

    def __init__(self, name: str):
        self.all = {}
        self.role_mask = {}
        self.name = name

    INTENSITY = {
        "rest": 0,
        "low": 1,
        "normal": 2,
        "high": 3,
        "very_high": 4,
    }

    def add(self, name: str, values: list[int], role_mask: bool = False):
        if len(values) != 5:
            return False
        self.all[name] = Attribute(values)
        self.role_mask[name] = role_mask
        return True

    def get(self, name: str = ""):
        if name in self.all.keys():
            return {
                "reference": self.all[name].reference,
                "maximum": self.all[name].maximum,
                "current": self.all[name].current
            }
        elif name == "":
            result = {}
            for name in self.all.keys():
                result[name] = self.get(name)
            return result
        else:
            return {}

    def maximise(self, name: str = ""):
        if name in self.all.keys():
            self.all[name].current = round(self.all[name].maximum + 0.01)
        elif name == "":
            for key in self.all.keys():
                self.maximise(key)

    def reset(self, name: str = ""):
        if name in self.all.keys():
            self.all[name].maximum = self.all[name].reference
            self.all[name].current = self.all[name].reference
        elif name == "":
            for key in self.all.keys():
                self.all[key].maximum = self.all[key].reference
                self.all[key].current = self.all[key].reference

    def upgrade(self, skip_role_mask: bool = True):
        for key in self.all.keys():
            if skip_role_mask or not self.role_mask[key]:
                self.all[key].reference = round(self.all[key].maximum + 0.01)
        self.maximise()

    def inc(self, name: str = "", skip_role_mask: bool = True):
        if name != "":
            if name in self.all.keys() and (skip_role_mask
                                            or not self.role_mask[name]):
                self.all[name].maximum += 0.5
        else:
            for key in self.all.keys():
                if (skip_role_mask or not self.role_mask[key]):
                    self.all[key].maximum += 0.5

    def dec(self, name: str = "", skip_role_mask: bool = True):
        if name != "":
            if name in self.all.keys() and (skip_role_mask
                                            or not self.role_mask[name]):
                self.all[name].maximum -= 0.5
        else:
            for key in self.all.keys():
                if (skip_role_mask or not self.role_mask[key]):
                    self.all[key].maximum -= 0.5

    def action(self, intensity, time, skip=[]):
        for key in self.all.keys():
            if key not in skip:
                Attribute.activity_reduction(self.all[key], intensity, time)

    def rest(self, intensity, time, capping, skip=[]):
        for key in self.all.keys():
            if key not in skip:
                if time > capping["limit"]:
                    Attribute.rest_increase(
                        self.all[key], intensity, capping["limit"])
                    current_value = self.all[key].current - capping["daily_rate"] * (
                        intensity) / 2 * (time - capping["limit"]) / REST_TIME_UNIT_DAYS
                    self.all[key].current = round(
                        current_value) if current_value > self.all[key].maximum * capping[
                        "cap"] else self.all[key].maximum * capping["cap"]
                else:
                    Attribute.rest_increase(self.all[key], intensity, time)
