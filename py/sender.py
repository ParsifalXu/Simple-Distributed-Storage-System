import shutil
import sys
import os
import time

import nodeChoose
# import fileSender

def transfer_file(file_path, target_path):
    file_name = os.path.basename(file_path)
    target_folder_name = os.path.basename(target_path)
    shutil.move(file_path, target_path)
    # print('%s has been sent to %s' %(file_name, target_folder_name))
    print('file sent completed')

def copy_file(file_path, target_path):
    file_name = os.path.basename(file_path)
    target_folder_name = os.path.basename(target_path)
    shutil.copyfile(file_path, target_path)
    # print('%s has been sent to %s as backups' %(file_name, target_folder_name))
    print('backup completed')



def sender(file_name):
    node_list = nodeChoose.nodeChoose()

    # File will be sent to main node first, then to backup node.
    transfer_file('../upload/' + file_name, '../Nodes/' + node_list[0] + '/buffer')

    # if file has been transferred to main node, then copy it three time as backups
    if os.path.exists('../Nodes/' + node_list[0] + '/buffer/' + file_name):
        for i in range(1, 4):
            copy_file('../Nodes/' + node_list[0] + '/buffer/' + file_name, '../Nodes/' + node_list[i] + '/buffer/' + file_name)

    # return info

sender('xrp.pdf')
