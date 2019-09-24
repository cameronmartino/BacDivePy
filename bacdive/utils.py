import string


def check_allow(mystring):
    allowed = string.ascii_letters + string.digits + ' '
    return all(c in allowed for c in mystring)
