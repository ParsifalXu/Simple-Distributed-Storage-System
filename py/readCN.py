import os
import json

def read_current_circle_number(path):
    cn_path = path + '/buffer/circleNumber.json'
    with open(cn_path, 'r') as f:
        data = json.load(f)
    return data['current_circle_number']
    f.close()

def write_current_circle_number(path, circle_number):
    cn_path = path + '/buffer/circleNumber.json'
    with open(cn_path, 'r') as f:
        data = json.load(f)
    f.close()
    with open(cn_path, 'w') as fw:
            data['current_circle_number'] = circle_number
            json_str = json.dumps(data)
            fw.write(json_str)
    fw.close()

def read_circle_number(path, file_name):
    cn_path = path + '/buffer/circleNumber.json'
    with open(cn_path, 'r') as f:
        data = json.load(f)

    if file_name in data:
        return data[file_name]
    else:
        return 0

    f.close()

def write_circle_number(path, file_name, circle_number):
    cn_path = path + '/buffer/circleNumber.json'
    with open(cn_path, 'r') as f:
        data = json.load(f)
    f.close()
    with open(cn_path, 'w') as fw:
            data[file_name] = circle_number
            json_str = json.dumps(data)
            fw.write(json_str)
    fw.close()

def delete_circle_number(path, file_name):
    cn_path = path + '/buffer/circleNumber.json'
    with open(cn_path, 'r') as f:
        data = json.load(f)
    f.close()
    with open(cn_path, 'w') as fw:
        del data[file_name]
        json_str = json.dumps(data)
        fw.write(json_str)
    fw.close()
