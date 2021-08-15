
import re


def re_comma2space(data):
    return re.sub(",", " ", data)


def re_sub_slash(data):
    return re.sub("/", " ", data)


def re_sub_dot(data):
    return re.sub(".", " ", data)


def re_sub_minus(data):
    return re.sub("-", " ", data)


def re_sub_equal_sign(data):
    return re.sub("=", " ", data)


def re_sub_colon(data):
    return re.sub(":", " ", data)


def re_sub_dot(data):
    return re.sub("\.", " ", data)


def re_sub_slash2comma(data):
    return re.sub("/", ",", data)

