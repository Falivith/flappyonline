# IPV4 da sua máquina

ip = "172.19.208.1"
port = 5555


def read_pos(str):

    if str is None or "," not in str:
        return 200, 200

    x_str, y_str = str.split(',')
    x = int(x_str)
    y = int(y_str)
    return x, y


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


def convert_string_in_tuple(s):
    s = s.strip("()")
    values = s.split(",")
    tup = tuple(int(value.strip()) for value in values)
    return tup

