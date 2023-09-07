def convert_bool_string_to_bool(bool_string):
    """
    To avoid ambiguities, this convertor force the user to adhere to the convention that only strings that satisfy the
    following conditions will be deemed as a True boolean value:
        - a string with only 4 chars; and
        - upper() of such string == 'TRUE'
    """
    if str(bool_string).upper() == 'TRUE':
        return True
    return False