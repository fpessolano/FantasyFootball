ALL = "ref"


class Single:
    """
    Class to define and manager individual attributes.
    """

    ACTIVITY_TIME_UNIT_MINUTES = 5
    TRAIN_TIME_UNIT_HOURS = 4
    REST_TIME_UNIT_HOURS = 6
    MINIMUM_STAT = 10.0
    ACTIVITY_INTENSITY = {"match": 2, "derby": 3, "final": 4, "match_light": 1,
                          "intense_training": 2, "normal_training": 1.5, "light_training": 1}
    REST_INTENSITY = {"full_rest": 2, "rest": 1, "holidays": 1.5}
    INJURY_SEVERITY = {'light': 1, "normal": 1, "serious": 2, "severe": 3}

    def __init__(self, values: list[int]):
        """
        Attibutes needs the following values:
            reference (0) : is the official (face) value
            current (1): the the actual value taking into consideration effects of activities
            maximum (2): is the the maximum value allowed due to activities
            activity_modifier (3): the coefficient that affects attribute reduction per activity units as defined in ACTIVITY_TIME_UNIT_MINUTES
            rest_modifier (4) : the coefficient that affects attribute reduction per rest units as defined in REST_TIME_UNIT_DAYS
            train_modifier (5) : the coefficient that affects attribute reduction per rest units as defined in TRAIN_TIME_UNIT_HOURS    
        """
        if len(values) != 6:
            raise ValueError("Stats must have 6 values")
        self.__reference = values[0]
        self.__current = values[1]
        self.__maximum = values[2]
        self.__activity_modifier = values[3]
        self.__rest_modifier = values[4]
        self.__train_modifier = values[5]
        self.__exhaution_level = 0

    def maxed(self):
        self.__current = self.__maximum

    def full_potential(self):
        self.__current = self.__maximum
        self.__reference = self.__maximum

    def act(self, intensity, time_minutes):
        if self.__current < Single.MINIMUM_STAT:
            # injured
            return
        if self.__exhaution_level:
            self.__exhaution_level = 100
            self.__current = Single.MINIMUM_STAT
            return
        current_value = self.__current - self.__activity_modifier * (
            intensity / 2) * (time_minutes / Single.ACTIVITY_TIME_UNIT_MINUTES)
        if current_value < 2 * Single.MINIMUM_STAT:
            when = 2*Single.ACTIVITY_TIME_UNIT_MINUTES * \
                (self.__current - 2 * Single.MINIMUM_STAT) / \
                (self.__activity_modifier * intensity)
            self.__exhaution_level = round(
                ((time_minutes - when) / time_minutes) * 100)
            time_minutes = when
        self.__current = current_value if current_value > Single.MINIMUM_STAT else Single.MINIMUM_STAT
        new_reference = self.__reference + self.__train_modifier * (
            intensity / 2) * (time_minutes / (Single.TRAIN_TIME_UNIT_HOURS * 60))
        self.__reference = new_reference if new_reference < self.__maximum else self.__maximum

    def rest(self, intensity, time_hours):
        if self.__current < Single.MINIMUM_STAT:
            # injured
            return
        self.__exhaution_level = 0
        current_value = self.__current + self.__rest_modifier * (
            3 - intensity / 2) * (time_hours / Single.REST_TIME_UNIT_HOURS)
        self.__current = current_value if current_value < self.__reference else self.__reference

    def injury(self, severity, time_days):
        self.__exhaution_level = 0
        self.__current = Single.MINIMUM_STAT - 1
        new_reference = self.__reference - self.__train_modifier * (
            severity / 2) * (time_days * 24 * 60 / (Single.TRAIN_TIME_UNIT_HOURS * 60))
        self.__reference = new_reference if new_reference > Single.MINIMUM_STAT else Single.MINIMUM_STAT

    def holidays(self, time_days):
        self.__exhaution_level = 0
        new_reference = self.__reference - self.__train_modifier * (
            Single.REST_INTENSITY["holidays"] / 2) * (time_days * 24 * 60 / (Single.TRAIN_TIME_UNIT_HOURS * 60))
        self.__reference = new_reference if new_reference > Single.MINIMUM_STAT else Single.MINIMUM_STAT
        self.__current = self.__reference

    def read(self, rounded=True):
        if rounded:
            return {
                "reference": round(self.__reference),
                "current": round(self.__current),
                "maximum": round(self.__maximum),
                "exhaustion": self.__exhaution_level
            }
        return {
            "reference": self.__reference,
            "current": self.__current,
            "maximum": self.__maximum,
            "exhaustion": self.__exhaution_level
        }


class Group:

    def __init__(self):
        self.__items = {}
        self.__original_definitions = {}

    def define(self, name: str, values: list[int]):
        """
        If the attribute exists, it gets overwritten without warning
        values needs the following values:
            reference (0) : is the official (face) value
            current (1): the the actual value taking into consideration effects of activities
            maximum (2): is the the maximum value allowed due to activities
            activity_modifier (3): the coefficient that affects attribute reduction per activity units as defined in ACTIVITY_TIME_UNIT_MINUTES
            rest_modifier (4) : the coefficient that affects attribute reduction per rest units as defined in REST_TIME_UNIT_DAYS
            train_modifier (5) : the coefficient that affects attribute reduction per rest units as defined in TRAIN_TIME_UNIT_HOURS    
        """
        try:
            self.__items[name] = Single(values)
            self.__original_definitions[name] = values
            return True
        except:
            return False

    def modifiers_mask(self, mask, enable_skipped=False):
        self.__items.clear()
        for name, values in self.__original_definitions.items():
            if name in mask:
                modifier = mask[name]
            else:
                modifier = int(enable_skipped)
            values = values[0:3] + [x * modifier for x in values[3:]]
            self.__items[name] = Single(values)

    def reset(self):
        self.modifiers_mask({}, True)

    def __getattr__(self, method_name):
        if len(self.__items) == 0:
            return lambda *args: None
        else:
            def method(*args, **kwargs):
                if len(args) == 0:
                    return
                elif args[0] == ALL:
                    results = []
                    for key in self.__items.keys():
                        if hasattr(self.__items[key], method_name):
                            called_method = getattr(
                                self.__items[key], method_name)
                            if len(args) > 1:
                                results.append(called_method(*args[1:]))
                            else:
                                results.append(called_method())
                    return results
                elif args[0] in self.__items.keys():
                    if hasattr(self.__items[args[0]], method_name):
                        called_method = getattr(
                            self.__items[args[0]], method_name)
                        if len(args) > 1:
                            return called_method(*args[1:])
                        else:
                            return called_method()
            return method


if __name__ == "__main__":
    test = Group()
    test.define("one", [55, 65, 88, 1.5, 5, 0.01])
    test.define("two", [55, 65, 88, 1.5, 5, 0.01])
    print(test.read(ALL))
    # test.full_potential(att.ALL)
    # print(test.read(att.ALL))
    test.act("two", 3, 95)
    print(test.read(ALL))
    test.modifiers_mask({"one":0.5})
    test.act(ALL, 3, 95)
    print(test.read(ALL))
    test.reset()
    test.act(ALL, 3, 95)
    print(test.read(ALL))
