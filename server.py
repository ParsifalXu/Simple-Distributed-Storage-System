#!/usr/bin/env python
# coding=utf-8
from flask import Flask, request, jsonify, Response, render_template as rt
from apscheduler.schedulers.background import BackgroundScheduler
import os
import sys
import time
import json
import requests

import sender
import nodeUpdate

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return rt('./index.html')

# upload files
@app.route('/file/upload', methods=['POST'])
def upload_part():  # receive an uploaded chunk
    task = request.form.get('task_id')  # obtain unique id
    chunk = request.form.get('chunk', 0)  # obatin chunk order
    filename = '%s%s' % (task, chunk)  # struct unique chunk
    upload_file = request.files['file']
    upload_file.save('./upload/%s' % filename)
    return rt('./index.html')

# merge files
@app.route('/file/merge', methods=['GET'])
def upload_success():  # read chunk content and write into new file
    target_filename = request.args.get('filename')  # get uploaded file name
    task = request.args.get('task_id')  # obatin unique id
    chunk = 0  # chunk order
    with open('./upload/%s' % target_filename, 'wb') as target_file:  # build a new file
        while True:
            try:
                filename = './upload/%s%d' % (task, chunk)
                source_file = open(filename, 'rb')  # read each chunk in order
                target_file.write(source_file.read())  # read content of each chunk and write into new file
                source_file.close()
            except Exception:
                break
            chunk += 1
            os.remove(filename)  # delete chunk to save space

    print('%s has been upload successfully' %target_filename)

    node_num = nodeUpdate.node_choose()
    print('node_num is %s' %node_num)
    sender.send(node_num, target_filename)

    nodeUpdate.resource_update(node_num, target_filename, 1)


    os.remove('./upload/' + target_filename)
    return rt('./index.html')

# get file list
@app.route('/file/list', methods=['GET'])
def file_list():
    with open('./chunk.json', 'r') as f:
        data = json.load(f)
    f.close()
    files = data['file_list']
    files = map(lambda x: x if isinstance(x, str) else x.encode(), files)  # Note encode and decode
    return rt('./list.html', files=files)

# download files
@app.route('/file/download/<filename>', methods=['GET'])
def file_download(filename):
    res = requests.get('http://127.0.0.1:5001/download/' + filename)

    def send_chunk():  # stream read
        # Add a node to read
        store_path = './upload/%s' % filename
        with open(store_path, 'rb') as target_file:
            while True:
                chunk = target_file.read(20 * 1024 * 1024)
                if not chunk:
                    break
                yield chunk

    return Response(send_chunk(), content_type='application/octet-stream')

# delete files
@app.route('/file/delete/<filename>', methods=['GET'])
def file_delete(filename):
    res = requests.get('http://127.0.0.1:5001/delete/' + filename)
    print('%s has been deleted' %filename)

    file_size = nodeUpdate.get_file_size(filename)
    # test case
    node_num = 1
    nodeUpdate.resource_update(node_num, filename, 0)

    return rt('./index.html')

# receive files from nodes
@app.route('/receive', methods = ['GET', 'POST'])
def receive():
    data = request.files.get('file_content')
    path = './upload/'
    file_name = data.filename
    storage_path = path + file_name
    data.save(storage_path)
    return storage_path


# periodically ping each nodes
error_times = 0 # global variables   the times of error happened
def ping():
    for i in range(1, 5):
        try:
            res = requests.post('http://127.0.0.1:500%s/ping' %(i))
            res_temp = json.loads(res.text)
            node = res_temp['node']
            time = res_temp['time']

            with open('./node_info.json', 'r') as f:
                data = json.load(f)
            f.close()

            with open('./node_info.json', 'w') as fw:
                    data[node]['heartbeat'] = time
                    json_str = json.dumps(data)
                    fw.write(json_str)
            fw.close()
        except Exception:
            global error_times
            error_times += 1
            if error_times >= 3:
                print('node_%s is dead' %i)
                if is_master_node(i):
                    node_for_rebuild, saved_file_list, node_for_send = change_master_node(i)

                    # rebuild
                    for x in range(0, len(saved_file_list)):
                        filenamenode = saved_file_list[i] + '+' + str(node_for_rebuild)
                        rebuild_link = 'http://127.0.0.1:500%s/rebuild/' %node_for_send
                        requests.get(rebuild_link + filenamenode)


                else:
                    with open('./node_info.json', 'r') as f:
                        data = json.load(f)
                    f.close()

                    with open('./node_info.json', 'w') as fw:
                        # change status. 1 represents activate; 0 represents inactivate
                        data['node_%s' %i]['status'] = 0
                        saved_file_list = data['node_%s' %i]['saved_file']
                        for n in range(1, 14):
                            if data['node_%s' %n]['status'] == 2:
                                node_for_rebuild = n

                        # find this i belongs to which master node
                        for x in range(0, 3):
                            t = data['master_node'][x]
                            if i in data['node_%s' %t]:
                                node_for_send = t

                        # rebuild
                        for x in range(0, len(saved_file_list)):
                            filenamenode = saved_file_list[i] + '+' + str(node_for_rebuild)
                            rebuild_link = 'http://127.0.0.1:500%s/rebuild/' %node_for_send
                            requests.get(rebuild_link + filenamenode)


                        json_str = json.dumps(data)
                        fw.write(json_str)
                    fw.close()
                    # will not influence current service, do alarm
                    print('node_%s is backup_node, please recover it quickly' %i)
                error_times = 0
            continue


# whether the node is master node
def is_master_node(num):
    with open('./node_info.json', 'r') as f:
        data = json.load(f)
    f.close()

    if num in data['master_node']:
        return 1
    else:
        return 0

# change master node
def change_master_node(num):
    with open('./node_info.json', 'r') as f:
        data = json.load(f)
    f.close()

    print(data['node_%s' %num]['backup_node'])

    if data['node_%s' %num]['backup_node']:
        with open('./node_info.json', 'w') as fw:
            # change status. 1 represents activate; 0 represents inactivate; 2 represents unused
            data['node_%s' %num]['status'] = 0
            file_list = data['node_%s' %num]['saved_file']
            print(file_list)
            print('1')
            data['node_%s' %num]['saved_file'] = []
            print('2')
            backup_num = data['node_%s' %num]['backup_node'][0]
            print('3')
            data['node_%s' %num]['backup_node'].remove(backup_num)
            data['master_node'].remove(num)
            data['master_node'].append(backup_num)
            print('4')
            for n in range(1, 14):
                if data['node_%s' %n]['status'] == 2:
                    node_for_rebuild = n

            saved_file_list = data['node_%s' %num]['saved_file']

            print('5')
            data['node_%s' %backup_num]['backup_node'].append(node_for_rebuild)
            print('6')
            json_str = json.dumps(data)
            fw.write(json_str)
        fw.close()
        print('success')
        return node_for_rebuild, saved_file_list, backup_num
    else:
        print('node_%s is damaged' %num)


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(ping, 'interval', seconds=5)
    scheduler.start()
    app.run(debug=False, threaded=True)
