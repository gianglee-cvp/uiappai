from flask import Flask, render_template
import folium
import osmnx as ox
import random

app = Flask(__name__)

@app.route("/")
def home():
    # Load lại đồ thị từ file .graphml
    graph = ox.load_graphml("truc_bach.graphml")
    # Tạo bản đồ Hà Nội
    random_node = random.choice(list(graph.nodes))
    latstart = graph.nodes[random_node]['y']
    lonstart = graph.nodes[random_node]['x']
    map_hanoi = folium.Map(location=[latstart, lonstart], zoom_start=16)
    
    # Thêm các node và edge từ đồ thị vào bản đồ
    for node_id, data in graph.nodes(data=True):
        lat = data['y']
        lon = data['x']
        folium.Marker(
            location=(lat, lon),
            popup=f"Node ID: {node_id}",
            icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(map_hanoi)
        
    for u, v, data in graph.edges(data=True):
        latlon_u = (graph.nodes[u]['y'], graph.nodes[u]['x'])
        latlon_v = (graph.nodes[v]['y'], graph.nodes[v]['x'])
        
        folium.PolyLine(
            locations=[latlon_u, latlon_v],
            color="red",
            weight=3,
            opacity=0.7
    ).add_to(map_hanoi)

    # Chuyển bản đồ thành HTML
    map_html = map_hanoi._repr_html_()

    return render_template("index.html", map_html=map_html)

if __name__ == "__main__":
    app.run(debug=True)
