def generate_tables():
    polynomial = 0x11d
    s = 8
    gf_elements = 1 << s

    gflog = gf_elements * [0]
    gfilog = gf_elements * [0]

    b = 1
    for i in range(0, gf_elements):
        gflog[b] = i & 255
        gfilog[i] = b & 255
        b <<= 1
        if b & gf_elements:
            b ^= polynomial

    gflog[1] = 0;
    return (gflog, gfilog)

def dump_table(caption, tab):
    item = 0
    print("--- {} ---".format(caption))
    for i in tab:
        print("0x{:02x}, ".format(i), end="")
        item += 1
        if item % 16 == 0:
            item = 0
            print()
    print("")

(gflog, gfilog) = generate_tables()
