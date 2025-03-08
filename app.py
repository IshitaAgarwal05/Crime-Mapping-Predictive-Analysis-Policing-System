import flet as ft
from flet import Tabs, Tab, Image, Column, Text


def main(page: ft.Page):
    page.title = "Crime Mapping & Predictive Policing System"
    page.scroll = True

    # Load saved images
    stats_images = [
        "incident_distribution.png",
        "cluster_density_map.png",
        "time_series_trend.png",
    ]

    # Statistics tab
    stats_tab = Column([
        Text("Incident Statistics & Visualizations", size=20, weight="bold")
    ] + [Image(src=img, width=600) for img in stats_images])

    # Predictive Map tab
    predictive_map_tab = Column([
        Text("Predictive Crime Hotspots", size=20, weight="bold"),
        Image(src="cluster_density_map.png", width=800)
    ])

    # Patrol Route tab
    patrol_route_tab = Column([
        Text("Optimized Patrol Route", size=20, weight="bold"),
        Image(src="optimized_patrol_route.png", width=800)
    ])

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