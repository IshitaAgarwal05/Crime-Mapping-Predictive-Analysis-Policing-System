import flet as ft
import webbrowser
import pandas as pd
from flet import Tabs, Tab, Image, Column, Text, ElevatedButton, Row, Container, TextField


# Function to validate user login
def validate_login(username, password):
    try:
        credentials = pd.read_csv("credentials.csv")  # Load CSV file
        for _, row in credentials.iterrows():
            if row["user_id"] == username and row["pwd"] == password:
                return True  # Login successful
    except Exception as e:
        print("Error reading CSV:", e)
    return False  # Login failed


# Main function
def main(page: ft.Page):
    page.title = "Login - Police Patrol Optimization"
    page.padding = 30
    page.scroll = True

    # Function to show the dashboard after successful login
    def show_dashboard():
        page.clean()  # Clear the login page
        page.title = "Police Patrol Optimization Dashboard"

        image_folder = "images/"

        # Load images
        stats_images = [
            image_folder + "Assault_crimes_in_Toronto.png",
            image_folder + "Crime_Indicator.png",
            image_folder + "Crime_Types_by_Hour_of_Day_in_Toronto.png",
            image_folder + "Elbow_Method_For_Optimal_k_2015.png",
            image_folder + "Major_Crime_Indicators_by_Month.png",
            image_folder + "Number_of_Major_Crimes_Reported_in_Toronto_in_2015.png",
            image_folder + "Toronto_Crime.png",
        ]

        # Function to open the crime map
        def open_crime_map(e):
            webbrowser.open("crime_map.html")

        # Arrange images in a 3-column grid
        stats_grid = []
        row_images = []
        for i, img in enumerate(stats_images):
            row_images.append(
                Container(
                    content=Image(src=img, width=350, height=280, fit="contain"),
                    bgcolor="white",
                    padding=10,
                    border_radius=10,
                )
            )
            if (i + 1) % 3 == 0 or i == len(stats_images) - 1:
                stats_grid.append(Row(row_images, alignment="center", spacing=15))
                row_images = []

        # Statistics tab
        stats_tab = Column([
            Text("Incident Statistics & Visualizations", size=22, weight="bold"),
            *stats_grid
        ], spacing=20)

        # Predictive Map tab
        predictive_map_tab = Column([
            Text("Predictive Crime Hotspots", size=22, weight="bold"),
            ElevatedButton("Show Crime Map", on_click=open_crime_map)
        ], spacing=20)

        # Patrol Route tab
        patrol_route_tab = Column([
            Text("Optimized Patrol Route", size=22, weight="bold"),
            Container(content=Image(src="optimized_patrol_route.png", width=800, height=500, fit="contain"), padding=15, bgcolor="white")
        ], spacing=20)

        # Tabs
        tabs = Tabs(
            selected_index=0,
            tabs=[
                Tab(text="Statistics", content=stats_tab),
                Tab(text="Predictive Map", content=predictive_map_tab),
                Tab(text="Patrol Route", content=patrol_route_tab)
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


ft.app(target=main)
