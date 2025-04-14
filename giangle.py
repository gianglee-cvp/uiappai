import matplotlib.pyplot as plt
import csv
import ast

# Đọc toạ độ nodes
positions = {}
added_status = {}

with open(r'C:\Users\Admin\Desktop\đạt brain\nodes.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            node_id = int(row['node_id'])
            x = float(row['x'])
            y = float(row['y'])
            added = int(row['added'])
            positions[node_id] = (x, y)
            added_status[node_id] = added
        except ValueError as e:
            print(f"Lỗi đọc dữ liệu: {row} - {e}")

# Đọc danh sách kề (adj_list)
edges = []
with open(r'C:\Users\Admin\Desktop\đạt brain\adj_list.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            print('2')
            node_id = int(row['node_index'])
            neighbors = ast.literal_eval(row['neighbors_indices'])  # chuyển chuỗi "[1, 2]" thành list [1, 2]
            for neighbor in neighbors:
                edges.append((node_id, neighbor))
        except Exception as e:
            print(f"Lỗi khi đọc dòng: {row} - {e}")

# Vẽ đồ thị
fig, ax = plt.subplots(figsize=(10, 10))

# Vẽ cạnh trước để không đè lên node
for u, v in edges:
    if u in positions and v in positions:
        x1, y1 = positions[u]
        x2, y2 = positions[v]
        ax.plot([x1, x2], [y1, y2], color='gray', linewidth=0.5, alpha=0.5)

# Vẽ node
for node_id, (x, y) in positions.items():
    added = added_status.get(node_id, 0)
    if added == 1:
        color = 'red'  # Node nội suy
    elif added == 2:
        color = 'blue'  # Node đầu mút cạnh nội suy
    else:
        color = 'green'  # Node gốc
    ax.plot(x, y, 'o', color=color, markersize=4, alpha=0.8)

ax.set_title("Đồ thị từ nodes.csv & adj_list.csv (hiển thị cả node & cạnh)")
ax.set_xlabel("Normalized X")
ax.set_ylabel("Normalized Y")
plt.axis('equal')
plt.grid(True)
plt.show()
