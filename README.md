# Simple-Distributed-Storage-System
 CE7490

 ## Installation

 * pip install -r requirements

 ## Operating Steps

 * Get into ./Nodes/node_1. node_2, node_3, node_4... as the same (you can only open 1 to 4 for test)

 * 'python ./server.py runserver' (Start the server, different nodes under same 127.0.0.1 with different port from 1 to 13)

 * Go back to master folder ./ and input 'python ./superserver.py runserver' to start the super node_

 * Open browser and get access to 'http://127.0.0.1:5000'

 * click 'Select File' to select file and upload it

 * 'http://127.0.0.1:5000/file/list' can see the file you uploaded and click the needed file to download

 * Or 'http://127.0.0.1:5000/file/download/<filename>' to download

 * 'http://127.0.0.1:5000/file/delete/<filename>' to delete files

 * Open postman and 'http://127.0.0.1:5001/rebuild/<filename+node>' to rebuild node, one request for one file synchronization
