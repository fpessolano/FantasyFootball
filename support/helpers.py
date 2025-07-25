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


def get_validated_input(prompt, valid_options=None, input_type=str, 
                       case_sensitive=False, allow_empty=False,
                       min_value=None, max_value=None):
    """
    Get validated user input with automatic retry on invalid input.
    
    :param prompt: The prompt to display to the user
    :param valid_options: List/tuple of valid options (for choice inputs)
    :param input_type: Expected type (str, int, float)
    :param case_sensitive: Whether string comparisons are case sensitive
    :param allow_empty: Whether empty input is allowed
    :param min_value: Minimum value for numeric inputs
    :param max_value: Maximum value for numeric inputs
    :return: Validated user input
    """
    while True:
        user_input = input(prompt).strip()
        
        # Handle empty input
        if not user_input:
            if allow_empty:
                return user_input
            else:
                print("!!! ERROR: Input cannot be empty !!!")
                continue
        
        # Type conversion and validation
        try:
            if input_type in (int, float):
                value = input_type(user_input)
                
                # Check numeric bounds
                if min_value is not None and value < min_value:
                    print(f"!!! ERROR: Value must be at least {min_value} !!!")
                    continue
                if max_value is not None and value > max_value:
                    print(f"!!! ERROR: Value must be at most {max_value} !!!")
                    continue
                    
                return value
            else:
                # String input
                if not case_sensitive and valid_options:
                    user_input_lower = user_input.lower()
                    valid_options_lower = [opt.lower() for opt in valid_options]
                    if user_input_lower in valid_options_lower:
                        # Return original case option
                        idx = valid_options_lower.index(user_input_lower)
                        return valid_options[idx]
                elif valid_options and user_input not in valid_options:
                    print(f"!!! ERROR: Please choose from: {', '.join(str(o) for o in valid_options)} !!!")
                    continue
                else:
                    return user_input
                    
        except ValueError:
            print(f"!!! ERROR: Invalid {input_type.__name__} value !!!")
            continue
            
    # Should never reach here
    return None
