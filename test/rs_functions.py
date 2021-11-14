from gflog_tables import *

# Addition
def gf_add(*args):
    result = 0
    for arg in args:
        result ^= arg

    return result

# Indexing
# First drive is 1, second drive is 2, etc...
def gf_drive(index):
    global gfilog

    return gfilog[index - 1]

# Multiplication
def gf_mul(a, b):
    global gflog
    global gfilog

    if a == 0 or b == 0:
        return 0
    else:
        return gfilog[(gflog[a] + gflog[b]) % 255]

# Division helper
def sub_gf8(a, b):
    if a > b:
        return a - b
    else:
        return (255 - (0 - (a - b)))

# Division
def gf_div(a, b):
    global gfilog
    global gflog

    return gfilog[sub_gf8(gflog[a], gflog[b])]
