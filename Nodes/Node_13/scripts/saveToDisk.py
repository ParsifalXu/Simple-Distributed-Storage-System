import os
from rsFunctions import *

import dataRecover
import readCN


def presolve(file_name):
    # let file can be split into 6 equally
    storage_path = './Storage/buffer/' + file_name
    total_size = os.path.getsize(storage_path)
    fill_up_number = (6 - (total_size % 6)) % 6
    file = open(storage_path, 'ab+')
    file.write(b'\x00' * fill_up_number)
    file.close()

# path = './Storage/buffer/requirements'

def split(file_name):
    storage_path = './Storage/buffer/' + file_name
    circle_number = readCN.read_current_circle_number()

    total_size = os.path.getsize(storage_path)
    part_size = int((total_size) / 6)
    file = open(storage_path, 'rb')

    partArr = []

    # circle write
    for i in range(0, 6):
        order = (i + circle_number) % 8
        temp = open('./Storage/disk_' + str(order) + '/' + file_name + '_' + str(i + 1) , 'wb')

        # read one part once
        file.seek(part_size * i, 0)
        buffer = file.read(part_size)
        partArr.append(buffer)
        temp.write(buffer)
        temp.close()

    # p_parity
    dataRecover.recover_p(circle_number, file_name, partArr)
    # q_parity
    dataRecover.recover_q(circle_number, file_name, partArr)

    readCN.write_file_circle_number(file_name, circle_number)
    circle_number = (circle_number + 1) % 8
    readCN.write_current_circle_number(circle_number)
    os.remove(storage_path)


def save_to_disk(filename):
    presolve(filename)
    split(filename)

# filename = 'requirements'
# save_to_disk(filename)
