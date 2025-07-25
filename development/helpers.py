def copy_keys(source: dict,
              destination: dict,
              key_list: list,
              if_absent="",
              key_rename_list: list = None):
  """
  Copyes values for keys key_list from dictionary a to dictionary b.
  If a key is not present in a, creates the key pair using if_absent as value
  :PARAM source: source dictionary
  :PARAM destination: destination dictionary
  :PARAM key_list: list of keys to be copies
  :PARAM if_absent: values to be used is the key is not present in the source dictionary
  :PARAM key_rename_list: if present and of the same length of key_list, will replace keys in the same order
  """
  if key_rename_list and len(key_list) != len(key_rename_list):
    key_rename_list = None
  for i, key in enumerate(key_list):
    if key in source.keys():
      value = source[key]
    else:
      value = if_absent
    if key_rename_list:
      destination[key_rename_list[i]] = value
    else:
      destination[key] = value
