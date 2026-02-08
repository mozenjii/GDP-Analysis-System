def safeExtend(lst, value):
    if isinstance(value, list):
        lst.extend(value)
    else:
        lst.append(value)
    return lst