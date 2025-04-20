
import folium

def create_map(tasks):
    m = folium.Map(location=[39.0, 35.0], zoom_start=6)
    for task in tasks:
        lat, lon = task["lat"], task["lon"]
        color = "blue" if task["durum"] == "beklemede" else "green"
        popup = f"{task['gorev_adi']}<br>{task['sehir']}<br>{task['durum']}"
        folium.Marker([lat, lon], popup=popup, icon=folium.Icon(color=color)).add_to(m)
    return m
