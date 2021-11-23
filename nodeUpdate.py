import os
import json

# choose node which has the most resouce
def node_choose():

    with open('./node_info.json', 'r') as f:
        data = json.load(f)
    f.close()

    master_node = data['master_node']

    max_resource = 0
    index = 0
    for i in range(0, len(master_node)):
        temp_resource = data['node_%s' %master_node[i]]['resource']
        if temp_resource > max_resource:
            max_resource = temp_resource
            index = i

    return data['master_node'][index]

# status: 1 represents save files, take up resources; 0 represents delete files, release resources
def resource_update(node_num, filename, status):
    with open('./node_info.json', 'r') as f:
        data = json.load(f)
    f.close()
    print('==========')
    print(filename)
    size = os.path.getsize('./upload/' + filename)

    with open('./node_info.json', 'w') as fw:
        if status == 1:
            data['node_%s' %node_num]['saved_file'].append(filename)
            temp_resource = data['node_%s' %node_num]['resource'] - size
        elif status == 0:
            data['node_%s' %node_num]['saved_file'].remove(filename)
            temp_resource = data['node_%s' %node_num]['resource'] + size

        data['node_%s' %node_num]['resource'] = temp_resource
        backup_nodes = data['node_%s' %node_num]['backup_node']
        for i in range(0, len(backup_nodes)):
            data['node_%s' %backup_nodes[i]]['resource'] = temp_resource

        json_str = json.dumps(data)
        fw.write(json_str)
    fw.close()

    # update chunk
    with open('./chunk.json', 'r') as fc:
        chunk = json.load(fc)
    fc.close()

    if status == 1:
        chunk['file_list'].append(filename)
        chunk[filename] = {
            "master_node": node_num,
            "size": size,
            "backup_nodes": backup_nodes
        }
    elif status == 0:
        chunk['file_list'].remove(filename)
        del chunk[filename]


    with open('./chunk.json', 'w') as fcw:
        json_str = json.dumps(chunk)
        fcw.write(json_str)
    fcw.close()




# obtain file size
def get_file_size(filename):
    with open('./chunk.json', 'r') as f:
        data = json.load(f)
    f.close()



    if filename in data['file_list']:
        return data[filename]['size']
    else:
        return 0
