import flet as ft
import webbrowser
from flet import Tabs, Tab, Image, Column, Text, ElevatedButton, Row, Container


def main(page: ft.Page):
    page.title = "Police Patrol Optimization Dashboard"
    page.padding = 30  # Padding around the page
    page.scroll = True

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
        # Container(content=Image(src="cluster_density_map.png", width=800, height=500, fit="contain"), padding=15, bgcolor="white"),
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


ft.app(target=main)
