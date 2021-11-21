import os
import json

def read_current_circle_number():
    with open('./Storage/buffer/circleNumber.json', 'r') as f:
        data = json.load(f)
    return data['current_circle_number']
    f.close()

def write_current_circle_number(circle_number):
    with open('./Storage/buffer/circleNumber.json', 'r') as f:
        data = json.load(f)
    f.close()
    with open('./Storage/buffer/circleNumber.json', 'w') as fw:
            data['current_circle_number'] = circle_number
            json_str = json.dumps(data)
            fw.write(json_str)
    fw.close()

def read_file_circle_number(file_name):
    with open('./Storage/buffer/circleNumber.json', 'r') as f:
        data = json.load(f)

    if file_name in data:
        return data[file_name]
    else:
        return 0

    f.close()

def write_file_circle_number(file_name, circle_number):
    with open('./Storage/buffer/circleNumber.json', 'r') as f:
        data = json.load(f)
    f.close()
    with open('./Storage/buffer/circleNumber.json', 'w') as fw:
            data[file_name] = circle_number
            json_str = json.dumps(data)
            fw.write(json_str)
    fw.close()

def delete_file_circle_number(file_name):
    with open('./Storage/buffer/circleNumber.json', 'r') as f:
        data = json.load(f)
    f.close()
    with open('./Storage/buffer/circleNumber.json', 'w') as fw:
        del data[file_name]
        json_str = json.dumps(data)
        fw.write(json_str)
    fw.close()
