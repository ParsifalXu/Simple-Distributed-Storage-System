import requests
import json

def send(node, filename):
    server_node = 'http://127.0.0.1:500%s/save' %node

    with open('./node_info.json', 'r') as f:
        data = json.load(f)
    f.close()

    backup_nodes_list = data['node_%s' %node]['backup_node']
    node_str = str(backup_nodes_list[0])
    for i in range(1, len(backup_nodes_list)):
        node_str = node_str + ',' + str(backup_nodes_list[i])
    backup_nodes = {"nodes": ""}
    backup_nodes['nodes'] = node_str

    files = {'file_content': open('./upload/' + filename, 'rb')}
    requests.post(server_node, data = backup_nodes, files = files)
