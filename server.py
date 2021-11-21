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


@app.route('/file/upload', methods=['POST'])
def upload_part():  # receive an uploaded chunk
    task = request.form.get('task_id')  # obtain unique id
    chunk = request.form.get('chunk', 0)  # obatin chunk order
    filename = '%s%s' % (task, chunk)  # struct unique chunk
    upload_file = request.files['file']
    upload_file.save('./upload/%s' % filename)
    return rt('./index.html')


@app.route('/file/merge', methods=['GET'])
def upload_success():  # 按序读出分片内容，并写入新文件

    target_filename = request.args.get('filename')  # 获取上传文件的文件名
    task = request.args.get('task_id')  # 获取文件的唯一标识符
    chunk = 0  # 分片序号
    with open('./upload/%s' % target_filename, 'wb') as target_file:  # 创建新文件
        while True:
            try:
                filename = './upload/%s%d' % (task, chunk)
                source_file = open(filename, 'rb')  # 按序打开每个分片
                target_file.write(source_file.read())  # 读取分片内容写入新文件
                source_file.close()
            except Exception:
                break
            chunk += 1
            os.remove(filename)  # 删除该分片，节约空间

    print('%s has been upload successfully' %target_filename)

    # file_size = os.path.getsize('./upload/' + target_filename)

    node_num = nodeUpdate.node_choose()
    sender.send(node_num, target_filename)
    nodeUpdate.resource_update(node_num, target_filename, 1)


    os.remove('./upload/' + target_filename)
    # node_thread(info)
    return rt('./index.html')


@app.route('/file/list', methods=['GET'])
def file_list():
    # files = os.listdir('./upload/')  # 获取文件目录
    with open('./chunk.json', 'r') as f:
        data = json.load(f)
    f.close()
    files = data['file_list']
    files = map(lambda x: x if isinstance(x, str) else x.encode(), files)  # 注意编码
    return rt('./list.html', files=files)


@app.route('/file/download/<filename>', methods=['GET'])
def file_download(filename):
    res = requests.get('http://127.0.0.1:5001/download/' + filename)

    def send_chunk():  # 流式读取
        # 添加一个节点读取
        store_path = './upload/%s' % filename
        with open(store_path, 'rb') as target_file:
            while True:
                chunk = target_file.read(20 * 1024 * 1024)
                if not chunk:
                    break
                yield chunk

    return Response(send_chunk(), content_type='application/octet-stream')


@app.route('/file/delete/<filename>', methods=['GET'])
def file_delete(filename):
    res = requests.get('http://127.0.0.1:5001/delete/' + filename)
    print('%s has been deleted' %filename)

    file_size = nodeUpdate.get_file_size()

    nodeUpdate.resource_update(node_num, file_size, 0)


@app.route('/receive', methods = ['GET', 'POST'])
def receive():
    data = request.files.get('file_content')
    path = './upload/'
    file_name = data.filename
    storage_path = path + file_name
    data.save(storage_path)
    return storage_path


error_times = 0

def ping():
    for i in range(1, 3):
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
                        node_for_rebuild = find_free_node()

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

    # print(data['node_%s' %num]['backup_node'])

    if data['node_%s' %num]['backup_node']:
        with open('./node_info.json', 'w') as fw:
            # change status. 1 represents activate; 0 represents inactivate; 2 represents unused
            data['node_%s' %num]['status'] = 0
            file_list = data['node_%s' %num]['saved_file']
            data['node_%s' %num]['saved_file'] = []
            backup_num = data['node_%s' %num]['backup_node'][0]
            data['node_%s' %num]['backup_node'].remove(backup_num)
            data['master_node'].remove(num)
            data['master_node'].append(backup_num)
            node_for_rebuild = find_free_node()
            data['node_%s' %backup_num]['backup_node'].append(node_for_rebuild)
            json_str = json.dumps(data)
            fw.write(json_str)
        fw.close()
        return node_for_rebuild, saved_file_list, backup_num
    else:
        print('node_%s is damaged' %num)


# find free node
def find_free_node():
    with open('./node_info.json', 'r') as f:
        data = json.load(f)
    f.close()

    for i in range(1, 14):
        if data['node_%s' %i]['status'] = 2:
            return i



if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(ping, 'interval', seconds=5)
    scheduler.start()
    app.run(debug=False, threaded=True)
