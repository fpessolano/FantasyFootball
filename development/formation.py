# in progress

class Formation:
  """
  Objects describing and managing team formations
  """

  _standard_formation = "433"
  _bench_size = 9
  __allowed_formations = {
    _standard_formation:
    ["gk", "lb", "cf", "cf", "rb", "lm", "cm", "rm", "lw", "cf", "rw"]
  }
  __formations_form_modifier = {
    _standard_formation: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
  }

  def __init__(self, type: str = _standard_formation, selection=[], bench=[]):
    """
      Declare a team
      :param type: formation type
      """
    self.__selection = selection
    self.__bench = bench
    if type in Formation.__allowed_formations.keys():
      self.__type = type

    else:
      self.__type = Formation._standard_formation

  def get_details(self):
    return self.__type, Formation.__allowed_formations[self.__type]

  def set_details(self, type, formation_settings=None, form_modifier=None):
    if (formation_settings and type in Formation.__allowed_formations) or \
      len(formation_settings) != 11:
      return False
    self.__type = type
    if type not in Formation.__allowed_formations:
      Formation.__allowed_formations[type] = formation_settings
      if form_modifier and len(form_modifier) == 11:
        Formation.__formations_form_modifier[type] = form_modifier

  def set_team(self, selection, bench):
    if len(selection) != 11 or len(bench) != Formation._bench_size:
      return False
    self.__selection = selection
    self.__bench = bench

  def get_team(self):
    return self.__selection, self.__bench
