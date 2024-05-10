import os

custom_nodes_dir = os.path.join(os.getcwd(), 'custom_nodes')

node_paths = []
for root, dirs, files in os.walk(custom_nodes_dir):
    for file in files:
        if file == 'node.js':
            relative_path = os.path.relpath(os.path.join(root, file), start=custom_nodes_dir)
            node_paths.append(relative_path)

print(node_paths)