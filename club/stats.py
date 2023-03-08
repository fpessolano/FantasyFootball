# TODO comment


class Stats:

  def __init__(self, values: list[int]):
    if len(values) != 5:
      raise ValueError("Stats must have 5 values")
    self.reference = values[0]
    self.current = values[1]
    self.__maximum = values[2]
    self.__active_modifier = values[3]
    self.__rest_modifier = values[4]

  INTENSITY = {
    "rest": 0,
    "low": 1,
    "normal": 2,
    "high": 3,
    "very_high": 4,
  }

  __ACTIVITY_TIME_UNIT_MINUTE = 5
  __REST_TIME_UNIT_DAYS = 1
  __MINIMUM_STAT = 5.0
  SEASON_DEFAULT_CAP = [3.0, 1.0, 0.9]
  HOLIDAYS_DEFAULT_CAP = [3.0, 0.5, 0.75]

  def reset(self):
    self.__maximum = self.reference
    self.cuurent = self.reference

  def fully_fit(self):
    self.current = round(self.__maximum + 0.01)

  def upgrade(self):
    self.reference = round(self.__maximum + 0.01)
    self.fully_fit()

  def dec(self):
    self.__maximum -= 0.5

  def inc(self):
    self.__maximum += 0.5

  def set(self, values: list[int]):
    if len(values) != 5:
      return False
    self.reference = values[0]
    self.current = values[1]
    self.__maximum = values[2]
    self.__active_modifier = values[3]
    self.__rest_modifier = values[4]
    return True

  def get(self):
    return self.reference, self.__maximum, self.current

  def action(self, intensity: int, time: int):
    current_value = self.current - self.__active_modifier * (
      intensity / 2) * time / Stats.__ACTIVITY_TIME_UNIT_MINUTE
    if current_value > Stats.__MINIMUM_STAT:
      self.current = round(current_value)
    else:
      self.current = Stats.__MINIMUM_STAT

  def rest(self, intensity: int, time: int, cap):
    if len(cap) != 3:
      raise (ValueError("Capping must have 3 values"))
    [limit, daily_rate, cap] = cap

    def calculate(stats, intensity, time):
      current_value = stats.current + stats.__rest_modifier * (
        intensity / 2) * time / Stats.__REST_TIME_UNIT_DAYS
      if current_value < stats.__maximum:
        return round(current_value + 0.01)
      else:
        return round(self.__maximum + 0.01)

    if time > limit:
      self.current = calculate(self, intensity, limit)
      current_value = self.current - daily_rate * (intensity / 2) * (
        time - limit) / Stats.__REST_TIME_UNIT_DAYS
      if current_value > self.__maximum * cap:
        self.current = round(current_value + 0.01)
      else:
        self.current = round(self.__maximum * cap + 0.01)
    else:
      self.current = calculate(self, intensity, time)
