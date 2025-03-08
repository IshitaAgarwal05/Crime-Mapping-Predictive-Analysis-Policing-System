# Crime Analysis in Toronto: Data Processing, Clustering, and Visualization

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import silhouette_score
import folium
from folium.plugins import HeatMap

# Load the dataset (assuming you have it)
file_path = 'toronto_crime_data.csv'
crime_df = pd.read_csv(file_path)

# Data Cleaning and Preprocessing
crime_df.dropna(inplace=True)
crime_df.drop_duplicates(inplace=True)

# Encode categorical features
encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
categorical_cols = ['Crime Type', 'Neighborhood']
encoded_features = encoder.fit_transform(crime_df[categorical_cols])

encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(categorical_cols))
crime_df = pd.concat([crime_df, encoded_df], axis=1).drop(columns=categorical_cols)

# Feature Scaling
scaler = StandardScaler()
scaled_features = scaler.fit_transform(crime_df[['Latitude', 'Longitude'] + list(encoded_df.columns)])

# KMeans Clustering
kmeans = KMeans(n_clusters=5, random_state=42)
crime_df['Cluster'] = kmeans.fit_predict(scaled_features)

# Silhouette Score
silhouette_avg = silhouette_score(scaled_features, crime_df['Cluster'])
print(f'Silhouette Score: {silhouette_avg:.2f}')

# Visualization: Crime Clusters
plt.figure(figsize=(10, 6))
sns.scatterplot(x=crime_df['Longitude'], y=crime_df['Latitude'], hue=crime_df['Cluster'], palette='tab10')
plt.title('Crime Clusters in Toronto')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.savefig('crime_clusters.png')

# Heatmap of Crime Incidents
crime_map = folium.Map(location=[crime_df['Latitude'].mean(), crime_df['Longitude'].mean()], zoom_start=12)
heat_data = crime_df[['Latitude', 'Longitude']].values.tolist()
HeatMap(heat_data).add_to(crime_map)
crime_map.save('crime_heatmap.html')

# Save Visualizations
plt.figure(figsize=(10, 6))
sns.countplot(x='Cluster', data=crime_df)
plt.title('Crime Count per Cluster')
plt.savefig('crime_count_per_cluster.png')

# Next step: Flet-based UI 🚀

# I’ll now create the UI with tabs for statistics, the predictive map, and the optimized patrol route. Let me draft that out! ✨
