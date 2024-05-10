from concurrent.futures import ThreadPoolExecutor
import time
import uuid
import os
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
import inspect

from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_socketio import SocketIO


app = Flask(__name__)
socketio = SocketIO(app)

executor = ThreadPoolExecutor(max_workers=1)
tasks = {}
classes_dict = {}
NODE_DIR='custom_nodes'

def js_list(parent_dir):
    js_dir = os.path.join(os.getcwd(), parent_dir)
    node_paths = []
    for root, dirs, files in os.walk(js_dir):
        for file in files:
            if file == 'node.js':
                relpath = os.path.relpath(os.path.join(root, file), start=js_dir)
                node_paths.append(relpath)
    return node_paths

def load_nodes(parent_dir):
    base_dir = Path(__file__).parent
    nodes_dir = base_dir / parent_dir
    for node_path in nodes_dir.glob('**/node.py'):
        module_name = node_path.stem
        package = node_path.parent.name  
        module_full_name = f'{parent_dir}.{package}.{module_name}'
        spec = spec_from_file_location(module_full_name, node_path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ == module.__name__:
                print(f'Found class: {name} in {module_full_name}')
                classes_dict[name] = obj
    
def background_task(task_name):
    if task_name not in classes_dict:
        for i in range(1, 11):
            time.sleep(1)
            percentage = i * 10
            socketio.emit('progress', {'progress': percentage})
        return f"{task_name} completed."
    running_class = classes_dict[task_name]
    class_inst = running_class()
    ret = class_inst.execute()
    time.sleep(5)
    return f"{task_name} {ret} completed."

@app.route('/')
def home():
    script_list = js_list(NODE_DIR)
    return render_template('editor.html', script_list=script_list)

@app.route(f'/{NODE_DIR}/<path:filename>')
def custom_nodes(filename):
    return send_from_directory('custom_nodes', filename)

@app.route('/start_task/<task_name>', methods=['GET'])
def start_task(task_name):
    if not task_name:
        return jsonify({'error': 'Missing task_name'}), 400
    
    task_id = str(uuid.uuid4())
    future = executor.submit(background_task, task_name)
    tasks[task_id] = future
    return jsonify({'task_id': task_id}), 202

@app.route('/task/<task_id>', methods=['GET'])
def get_task(task_id):
    task = tasks.get(task_id)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    
    if task.done():
        return jsonify({'status': 'completed', 'result': task.result()})
    else:
        return jsonify({'status': 'in progress'}), 202

if __name__ == '__main__':
    load_nodes(NODE_DIR)
    socketio.run(app, debug=True)
