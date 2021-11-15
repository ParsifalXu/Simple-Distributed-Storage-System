import os
import readCN

def rebuild_from_disk(node ,file_name):
    node_path = '../Nodes/' + node
    circle_number = readCN.read_circle_number(node_path, file_name)

    buffer = bytes()
    for i in range(0, 8):
        order = (i + circle_number) % 8
        if i == 6:
            os.remove(node_path + '/disk_' + str(order) + '/' + file_name + '_p')
        elif i == 7:
            os.remove(node_path + '/disk_' + str(order) + '/' + file_name + '_q')
        else:
            temp = open(node_path + '/disk_' + str(order) + '/' + file_name + '_' + str(i + 1) , 'rb')
            buffer += temp.read()
            temp.close()
            os.remove(node_path + '/disk_' + str(order) + '/' + file_name + '_' + str(i + 1))


    file = open(node_path + '/buffer/' + file_name, 'wb')
    file.write(buffer)
    file.close()
    readCN.delete_circle_number(node_path, file_name)

# path = '../Nodes/node_1/buffer/CE7490_Pre_Analysis of XRP.pdf'

path = '../Nodes/node_1'
rebuild_from_disk(path, 'CE7490_Pre_Analysis of XRP.pdf')
