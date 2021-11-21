import json


b = {
    "master_node": 1,
    "size": 1,
    "backup_nodes": [2, 3, 4]
}

with open('./chunk.json', 'r') as fc:
    chunk = json.load(fc)
fc.close()



with open('./chunk.json', 'w') as fw:
    # chunk['file_list'].append('x')
    del chunk['box']

    json_str = json.dumps(chunk)
    fw.write(json_str)
fw.close()
