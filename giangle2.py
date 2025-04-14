import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import numpy as np
import math
import csv
from matplotlib.widgets import Button

# === Load dữ liệu nodes ===
nodes_df = pd.read_csv(r"C:\Users\ADMIN\Desktop\dsa-pathfinding-project-3-main\nodes.csv")
if not all(col in nodes_df.columns for col in ['node_id', 'x', 'y']):
    raise ValueError("File nodes.csv thiếu các cột bắt buộc: 'node_id', 'x', 'y'")

positions = {
    int(row['node_id']): (float(row['x']) * 10, float(row['y']) * 10)
    for _, row in nodes_df.iterrows()
}

# === Load dữ liệu edges (adjacency list) ===
adj_dict = {}
with open( r"C:\Users\ADMIN\Desktop\dsa-pathfinding-project-3-main\adj_list_with_weights.csv", 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        node = int(row[0])
        neighbors = {}
        try:
            entries = eval(row[1])
            for neighbor, weight in entries:
                neighbors[int(neighbor)] = float(weight)
        except Exception as e:
            print(f"Lỗi parse dòng {node}: {e}")
        adj_dict[node] = neighbors

# === Kiểm tra và làm sạch dữ liệu ===
all_nodes = set(positions.keys()).union(set(adj_dict.keys()))
x_vals = [p[0] for p in positions.values()]
y_vals = [p[1] for p in positions.values()]
x_min, x_max, y_min, y_max = min(x_vals), max(x_vals), min(y_vals), max(y_vals)

# Gán tọa độ ngẫu nhiên nếu thiếu
for node in all_nodes:
    if node not in positions:
        positions[node] = (
            np.random.uniform(x_min, x_max),
            np.random.uniform(y_min, y_max)
        )
    if node not in adj_dict:
        adj_dict[node] = {}

# === Cài đặt giao diện ===
fig, ax = plt.subplots(figsize=(12, 10))
plt.subplots_adjust(bottom=0.15)
ax.set_aspect('equal')
plt.axis('off')

# Vẽ các node
for node_id, (x, y) in positions.items():
    added_value = int(nodes_df.loc[nodes_df['node_id'] == node_id, 'added'].values[0])
    color = (
        'red' if added_value == 1 else
        'blue'
    )
    ax.plot(x, y, 'o', color=color, markersize=8, alpha=0.7)

# Vẽ cạnh
for u, neighbors in adj_dict.items():
    for v in neighbors:
        if u in positions and v in positions:
            x0, y0 = positions[u]
            x1, y1 = positions[v]
            ax.plot([x0, x1], [y0, y1], color='lightgray', linewidth=0.7)

# === A* Pathfinding ===
try:
    from a_star import astar
    a_star_available = True
except:
    a_star_available = False

selected_nodes = []
lines = []
animation_frames = []
animation_running = False
ani = None

def find_nearest_node(x, y):
    return min(positions, key=lambda node: (positions[node][0] - x)**2 + (positions[node][1] - y)**2)

def on_click(event):
    global selected_nodes
    if event.inaxes != ax or len(selected_nodes) >= 2 or animation_running:
        return
    node = find_nearest_node(event.xdata, event.ydata)
    color = 'green' if len(selected_nodes) == 0 else 'red'
    ax.plot(*positions[node], 'o', color=color, markersize=10)
    selected_nodes.append(node)
    status = f"Selected: {selected_nodes}" if len(selected_nodes) < 2 else f"Ready to animate: {selected_nodes}"
    plt.title(status)
    plt.draw()

def update_frame(frame):
    global lines
    for ln in lines:
        if ln in ax.lines:
            ln.remove()
    lines.clear()
    for u, v in animation_frames[frame]:
        if u in positions and v in positions:
            x0, y0 = positions[u]
            x1, y1 = positions[v]
            ln, = ax.plot([x0, x1], [y0, y1], color='red', linewidth=2)
            lines.append(ln)

def run_animation(event):
    global ani, animation_frames, animation_running
    if len(selected_nodes) != 2 or not a_star_available:
        return
    source, dest = selected_nodes
    animation_frames = []
    for step in range(1, 200):
        result = astar(adj_dict, source, dest, step)
        if not isinstance(result, list):
            animation_frames.append([])
            continue
        step_edges = [(node, neighbor) for node in result for neighbor in adj_dict.get(node, {})]
        animation_frames.append(step_edges)
    ani = animation.FuncAnimation(fig, update_frame, frames=len(animation_frames), interval=80)
    animation_running = True
    plt.title(f"A* Path: {source} → {dest}")
    plt.draw()

def reset(event):
    global selected_nodes, lines, animation_frames, ani, animation_running
    selected_nodes.clear()
    for ln in lines:
        if ln in ax.lines:
            ln.remove()
    lines.clear()
    animation_frames.clear()
    if ani:
        ani.event_source.stop()
    animation_running = False
    plt.title("Visualization - Click to select start and end")
    plt.draw()

def save(event):
    if ani and selected_nodes:
        filename = f"astar_{selected_nodes[0]}_{selected_nodes[1]}.mp4"
        ani.save(filename, writer='ffmpeg', fps=10)
        plt.title(f"Lưu thành công: {filename}")
        plt.draw()

# Kết nối sự kiện
fig.canvas.mpl_connect('button_press_event', on_click)
Button(plt.axes([0.15, 0.05, 0.2, 0.05]), "Reset").on_clicked(reset)
Button(plt.axes([0.4, 0.05, 0.2, 0.05]), "Run Animation").on_clicked(run_animation)
Button(plt.axes([0.65, 0.05, 0.2, 0.05]), "Save Animation").on_clicked(save)

plt.title("Visualization - Click to select start and end")
plt.show()