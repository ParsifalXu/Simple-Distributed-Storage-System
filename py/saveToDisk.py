import os
from rsFunctions import *

import dataRecover
import readCN


#
def presolve(path):
    # let file can be split into 6 equally
    total_size = os.path.getsize(path)
    fill_up_number = (6 - (total_size % 6)) % 6
    file = open(path, 'ab+')
    file.write(b'\x00' * fill_up_number)
    file.close()


def split(path):
    current_node = os.path.dirname(os.path.dirname(path))
    file_name = os.path.basename(path)
    circle_number = readCN.read_current_circle_number(current_node)

    total_size = os.path.getsize(path)
    part_size = int((total_size) / 6)
    file = open(path, 'rb')

    partArr = []

    # circle write
    for i in range(0, 6):
        order = (i + circle_number) % 8
        temp = open(current_node + '/disk_' + str(order) + '/' + file_name + '_' + str(i + 1) , 'wb')

        # read one part once
        file.seek(part_size * i, 0)
        buffer = file.read(part_size)
        partArr.append(buffer)
        temp.write(buffer)
        temp.close()

    # p_parity
    dataRecover.recover_p(circle_number, current_node, file_name, partArr)
    # q_parity
    dataRecover.recover_q(circle_number, current_node, file_name, partArr)

    readCN.write_circle_number(current_node, file_name, circle_number)
    circle_number = (circle_number + 1) % 8
    readCN.write_current_circle_number(current_node, circle_number)
    os.remove(path)


def save_to_disk(path):
    presolve(path)
    split(path)

path = '../Nodes/node_1/buffer/CE7490_Pre_Analysis of XRP.pdf'
save_to_disk(path)
