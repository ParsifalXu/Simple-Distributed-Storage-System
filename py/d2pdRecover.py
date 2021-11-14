# recover d2 and pd
from rs_functions import *

# We have these drives...
image1 = [ ord('f'), ord('i'), ord('r'), ord('s'), ord('t') ]
image3 = [ ord('t'), ord('h'), ord('i'), ord('r'), ord('d') ]
imageRS = [ 0x4d, 0x1e, 0x0d, 0x7a, 0x31 ]

# ...and these drives are dead
imagePD = [0] * 5
image2 = [0] * 5

for i in range(0, 5):
    partialRS = gf_add(gf_mul(gf_drive(1), image1[i]),
                       imageRS[i],  # Use RS drive instead of the dead drive.
                       gf_mul(gf_drive(3), image3[i]))

    # gf_drive(2) is our dead drive.
    div_result = gf_div(1, gf_drive(2))

    # This will generate the data from the dead D2 drive.
    image2[i] = gf_mul(div_result, partialRS)

    # This will generate the data from the dead PD drive.
    imagePD[i] = gf_add(image1[i], image2[i], image3[i])

dump_table("image2", image2)
dump_table("imagePD", imagePD)
