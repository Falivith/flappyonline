ip = "172.19.208.1"


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


def convert_string_in_tuple(s):
    s = s.strip("()")
    values = s.split(",")
    tup = tuple(int(value.strip()) for value in values)
    return tup

