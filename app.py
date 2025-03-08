import flet as ft
import webbrowser
import pandas as pd
import requests
from geopy.distance import great_circle
from flet import Tabs, Tab, Image, Column, Text, ElevatedButton, Row, Container, TextField, AlertDialog
import heapq
import atexit
import folium
from folium.plugins import MarkerCluster
from math import radians, sin, cos, sqrt, atan2
from auth import validate_login
from rate_limiter import is_rate_limited
from performance_model import performance_model_tab 

performance_tab = performance_model_tab()

# Load crime data
crime_data = pd.read_csv("data/processed_data.csv") 
junctions_data = pd.read_csv("data/junctions.csv")  

# Google Maps API key
API_KEY = "AIzaSyDIvbFbGFjCZDclBFL4GGyk0pVRHXoWyFI"

# Global variable to store optimized route
optimized_route = []

# Function to fetch roads data using Google Maps API
def fetch_roads_data(lat, long, radius=5000):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{long}&radius={radius}&type=route&key={API_KEY}"
    response = requests.get(url).json()
    roads = []
    for result in response.get("results", []):
        roads.append({
            "name": result["name"],
            "lat": result["geometry"]["location"]["lat"],
            "long": result["geometry"]["location"]["lng"]
        })
    return roads

# Function to calculate distance between two points using Haversine formula
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in kilometers
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# A* Algorithm to find the shortest path
def a_star(start, goal, graph):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph}
    f_score[start] = haversine(start[0], start[1], goal[0], goal[1])

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for neighbor in graph[current]:
            tentative_g_score = g_score[current] + haversine(current[0], current[1], neighbor[0], neighbor[1])
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + haversine(neighbor[0], neighbor[1], goal[0], goal[1])
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None

# Create a graph from junctions
def create_graph(junctions):
    graph = {}
    for i, row in junctions.iterrows():
        graph[(row["Lat"], row["Long"])] = []
        for j, neighbor in junctions.iterrows():
            if i != j:
                graph[(row["Lat"], row["Long"])].append((neighbor["Lat"], neighbor["Long"]))
    return graph

# Function to generate the optimized patrol route map
def generate_patrol_route_map(police_station_lat, police_station_long, start_time, end_time):
    global optimized_route  # Use the global variable

    # Filter crime data for the given time duration
    filtered_crimes = crime_data[
        (crime_data["occurrencedate"] >= start_time) & (crime_data["occurrencedate"] <= end_time)
    ]

    # Get top crime hotspots (e.g., top 5 locations with most crimes)
    hotspots = filtered_crimes.groupby(["Lat", "Long"]).size().nlargest(5).reset_index()

    # Create a base map centered around the police station
    crime_map = folium.Map(location=[police_station_lat, police_station_long], zoom_start=13)

    # Add Marker Clustering
    marker_cluster = MarkerCluster().add_to(crime_map)

    # Add junctions to the map
    for _, row in junctions_data.iterrows():
        folium.Marker(
            location=[row["Lat"], row["Long"]],
            popup=f"Junction {row['Junction_ID']}",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(marker_cluster)

    # Create graph from junctions
    graph = create_graph(junctions_data)

    # Calculate optimized route using A* algorithm
    start = (police_station_lat, police_station_long)
    goal = (hotspots.iloc[0]["Lat"], hotspots.iloc[0]["Long"])  # First hotspot as goal
    optimized_route = a_star(start, goal, graph)

    # Add optimized route to the map
    if optimized_route:
        folium.PolyLine(
            locations=optimized_route,
            color="red",
            weight=5,
            opacity=0.7,
            popup="Optimized Patrol Route"
        ).add_to(crime_map)

    # Save the map
    crime_map.save("optimized_patrol_route.html")
    print("Optimized patrol route map generated! Open 'optimized_patrol_route.html' in your browser.")

# Main app
def main(page: ft.Page):
    page.title = "Login - Police Patrol Optimization"
    page.padding = 30  # Padding around the page
    page.scroll = True

    def show_dashboard():
        page.clean()  # Clear the login page
        page.title = "Police Patrol Optimization Dashboard"

        image_folder = "images/"

        # Load saved images
        stats_images = [
            image_folder + "Assault_crimes_in_Toronto.png",
            image_folder + "Crime_Indicator.png",
            image_folder + "Crime_Types_by_Hour_of_Day_in_Toronto.png",
            image_folder + "Elbow_Method_For_Optimal_k_2015.png",
            image_folder + "Major_Crime_Indicators_by_Month.png",
            image_folder + "Number_of_Major_Crimes_Reported_in_Toronto_in_2015.png",
        ]

        # Function to open the crime map
        def open_crime_map(e):
            webbrowser.open("crime_map.html")

        # Arrange images in a 3-column grid without cropping
        stats_grid = []
        row_images = []

        for i, img in enumerate(stats_images):
            row_images.append(
                Container(
                    content=Image(src=img, width=350, height=280, fit="contain"),  # Wrapped Image inside Container
                    bgcolor="white",  # Background color for visibility
                    padding=10,  # Spacing inside the container
                    border_radius=10,  # Rounded corners for a cleaner look
                )
            )

            if (i + 1) % 3 == 0 or i == len(stats_images) - 1:
                stats_grid.append(Row(row_images, alignment="center", spacing=15))  # Space between images
                row_images = []

        # Statistics tab with grid layout
        stats_tab = Column([
            Text("Incident Statistics & Visualizations", size=22, weight="bold"),
            *stats_grid  # Unpacking rows into the column
        ], spacing=20)

        # Predictive Map tab
        predictive_map_tab = Column([
            Text("Predictive Crime Hotspots", size=22, weight="bold"),
            ElevatedButton("Show Crime Map", on_click=open_crime_map)
        ], spacing=20)

        # Patrol Route tab
        police_station_lat = TextField(label="Police Station Latitude")
        police_station_long = TextField(label="Police Station Longitude")
        start_time = TextField(label="Patrol Start Time (YYYY-MM-DD HH:MM:SS)")
        end_time = TextField(label="Patrol End Time (YYYY-MM-DD HH:MM:SS)")
        optimized_route_output = Text()
        
        show_map_button = ft.Ref[ft.ElevatedButton]() 
        show_map_button.current = ft.ElevatedButton(
            text="Show Optimized Route on Map",
            on_click=lambda e: webbrowser.open("optimized_patrol_route.html"),
            visible=False
        )

        def calculate_route(e):
            global optimized_route  
            try:
                generate_patrol_route_map(
                    float(police_station_lat.value),
                    float(police_station_long.value),
                    start_time.value,
                    end_time.value
                )
                optimized_route_output.value = "Optimized route map generated! Click 'Show Optimized Route on Map' to view."
                show_map_button.current.visible = True
            except Exception as ex:
                optimized_route_output.value = f"Error: {str(ex)}"
                show_map_button.current.visible = False 
            page.update() 

        patrol_route_tab = Column([
            Text("Optimized Patrol Route", size=22, weight="bold"),
            police_station_lat,
            police_station_long,
            start_time,
            end_time,
            ElevatedButton("Calculate Route", on_click=calculate_route),
            optimized_route_output,
            show_map_button.current
        ], spacing=20)

        # Tabs
        tabs = Tabs(
            selected_index=0,
            tabs=[
                Tab(text="Statistics", content=stats_tab),
                Tab(text="Predictive Map", content=predictive_map_tab),
                Tab(text="Patrol Route", content=patrol_route_tab),
                Tab(text="Performance Model", content=performance_tab) 
            ],
        )

        page.add(tabs)

    # Login Page UI
    username_field = TextField(label="Username", width=300)
    password_field = TextField(label="Password", width=300, password=True, can_reveal_password=True)
    error_text = Text("", color="red")

    def handle_login(e):
        username = username_field.value.strip()
        password = password_field.value.strip()

        # Check if user is rate-limited
        if is_rate_limited(username):
            error_text.value = "Too many attempts! Try again later."
            page.update()
            
            return

        if validate_login(username, password):
            show_dashboard()  # Load dashboard on successful login
        else:
            error_text.value = "Invalid username or password!"
            page.update()

    login_button = ElevatedButton("Login", on_click=handle_login)

    # Center the login form
    login_page = Container(
        content=Column([
            Text("Police Patrol Optimization System", size=24, weight="bold"),
            username_field,
            password_field,
            login_button,
            error_text
        ], alignment="center", spacing=20, horizontal_alignment="center"),
        alignment=ft.alignment.center,
        expand=True  # Ensures full visibility
    )

    page.add(login_page)
    atexit.register(lambda: page.window_close())

# Run the app
ft.app(target=main)