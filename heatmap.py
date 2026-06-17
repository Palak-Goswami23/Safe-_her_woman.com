import folium

m = folium.Map(
    location=[26.85, 80.95],
    zoom_start=12
)

folium.CircleMarker(
    [26.85, 80.95],
    radius=15,
    popup="High Risk Area",
    color="red",
    fill=True
).add_to(m)

folium.CircleMarker(
    [26.87, 80.98],
    radius=15,
    popup="Moderate Risk Area",
    color="orange",
    fill=True
).add_to(m)

folium.CircleMarker(
    [26.89, 81.00],
    radius=15,
    popup="Safe Area",
    color="green",
    fill=True
).add_to(m)

m.save("templates/heatmap.html")

print("Heatmap Created")