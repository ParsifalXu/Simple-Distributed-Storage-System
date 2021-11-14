import os
from rsFunctions import *

import dataRecover

#
def presolve(path):
    # let file can be split into 6 equally
    total_size = os.path.getsize(path)
    fill_up_number = (6 - (total_size % 6)) % 6
    file = open(path, 'ab+')
    file.write(b'\x00' * fill_up_number)
    file.close()


def read_circle_number(path):
    cn_path = os.path.dirname(path) + '/circleNumber.txt'
    if os.path.exists(cn_path):
        cn = open(cn_path, 'r')
        circle_number = int(cn.read())
        cn.close()
        return circle_number
    else:
        cn = open(cn_path, 'w')
        cn.write('0')
        cn.close()
        return 0

def write_circle_number(path, circle_number):
    cn_path = os.path.dirname(path) + '/circleNumber.txt'
    cn = open(cn_path, 'w')
    cn.write(str(circle_number))
    cn.close()



def split(path):
    circle_number = read_circle_number(path)
    current_node = os.path.dirname(os.path.dirname(path))
    file_name = os.path.basename(path)

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

    # circle_number++
    circle_number = (circle_number + 1) % 8
    write_circle_number(path, circle_number)



path = '../Nodes/node_1/buffer/xrp.pdf'
split(path)

def save_to_disk(path):
    presolve(path)
    split(path)
