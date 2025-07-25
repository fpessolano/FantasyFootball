# SCRATCH FILE: Attribute bank/collection system
# Imports attribute classes and defines collections of player attributes
# Incomplete implementation - planned to manage multiple attribute types
# Not used in main application - experimental attribute grouping system

from attribute import Single as at
# import functools
# import inspect

# SEASON_DEFAULT_CAP = {"limit": 3.0, "daily_rate": 1.0, "cap": 0.9}
# HOLIDAYS_DEFAULT_CAP = {"limit": 3.0, "daily_rate": 0.5, "cap": 0.75}

# to be done

ALL = "ref"


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
            self.__items[name] = at(values)
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
            self.__items[name] = at(values)

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
