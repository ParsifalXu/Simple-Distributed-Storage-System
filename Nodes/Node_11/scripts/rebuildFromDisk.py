import os
import readCN

def rebuild_from_disk(file_name):
    circle_number = readCN.read_file_circle_number(file_name)

    buffer = bytes()
    for i in range(0, 8):
        order = (i + circle_number) % 8
        if i == 6:
            os.remove('./Storage/disk_' + str(order) + '/' + file_name + '_p')
        elif i == 7:
            os.remove('./Storage/disk_' + str(order) + '/' + file_name + '_q')
        else:
            temp = open('./Storage/disk_' + str(order) + '/' + file_name + '_' + str(i + 1) , 'rb')
            buffer += temp.read()
            temp.close()
            os.remove('./Storage/disk_' + str(order) + '/' + file_name + '_' + str(i + 1))


    file = open('./Storage/buffer/' + file_name, 'wb')
    file.write(buffer)
    file.close()
    readCN.delete_file_circle_number(file_name)

# path = './Nodes/node_1/buffer/CE7490_Pre_Analysis of XRP.pdf'

# path = '../Nodes/node_1'
# rebuild_from_disk('requirements')
