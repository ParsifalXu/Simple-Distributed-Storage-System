#!/usr/bin/env python
# coding=utf-8
from flask import Flask, request, jsonify, Response, render_template as rt
# from apscheduler.schedulers.background import BackgroundScheduler
import os
import sys
import time
import json
import requests


sys.path.append('scripts')
import saveToDisk
import rebuildFromDisk

app = Flask(__name__)

@app.route('/ping', methods = ['GET', 'POST'])
def heartbeat():
    current_time = int(time.time())
    node_info = {
        "node": 'node_3',
        'time': current_time
    }
    return jsonify(node_info)


@app.route('/save', methods = ['GET', 'POST'])
def save():
    data = request.files.get('file_content')
    backup = request.values.get('nodes')
    path = './Storage/buffer/'
    file_name = data.filename
    storage_path = path + file_name
    data.save(storage_path)

    if backup:
        backup_nodes = backup.split(',')
        length = len(backup_nodes)

        with open('./backup.json', 'r') as f:
            data = json.load(f)
        f.close()

        with open('./backup.json', 'w') as fw:
            # change status. 1 represents activate; 0 represents inactivate
            data[file_name] = backup_nodes
            json_str = json.dumps(data)
            fw.write(json_str)
        fw.close()

        for i in range(0, length):
            server_node = server_node = 'http://127.0.0.1:500%s/save' %backup_nodes[i]
            backup = {'node' : ''}
            files = {'file_content': open('./Storage/buffer/' + file_name, 'rb')}
            requests.post(server_node, data = backup, files = files)

    saveToDisk.save_to_disk(file_name)
    return storage_path

@app.route('/download/<filename>', methods = ['GET'])
def rebuild(filename):
    rebuildFromDisk.rebuild_from_disk(filename)
    files = {'file_content': open('./Storage/buffer/' + filename, 'rb')}
    requests.post('http://127.0.0.1:5000/receive', files = files)
    saveToDisk.save_to_disk(filename)


@app.route('/delete/<filename>', methods = ['GET'])
def delete(filename):
    rebuildFromDisk.rebuild_from_disk(filename)
    os.remove('./Storage/buffer/' + filename)
    # files = {'file_content': open('./Storage/buffer/' + filename, 'rb')}
    # requests.post('http://127.0.0.1:5000/receive', files = files)

    with open('./backup.json', 'r') as f:
        data = json.load(f)
    f.close()

    if data[filename]:
        for i in range(0, len(data[filename])):
            backup_nodes = data[filename]
            server_node = 'http://127.0.0.1:500%s/delete/' %backup_nodes[i]
            requests.get(server_node + filename)

        with open('./backup.json', 'w') as fw:
            # change status. 1 represents activate; 0 represents inactivate
            data[filename].remove()
            json_str = json.dumps(data)
            fw.write(json_str)
        fw.close()





if __name__ == '__main__':
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(heartbeat, 'interval', seconds=5)
    # scheduler.start()
    app.run(host = '127.0.0.1', port = 5003, debug = False, threaded = True)
