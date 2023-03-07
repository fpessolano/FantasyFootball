class Stats:
  def __init__(self, values: list[int]):
    if len(values) != 5:
      raise ValueError("Stats must have 5 values") 
    self.reference = values[0]
    self.current = values[1]
    self.maximum = values[2]
    self.rest_modifier = values[3]
    self.active_modifier = values[4]