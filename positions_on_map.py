import os
import json
import matplotlib.pyplot as plt
import contextily as cx

"""
Plot positions of pictures on a map
"""

# Open all jsons to get locations
database_folder = "database_presentation/"
locations = []
for location in os.listdir(database_folder):
    with open(database_folder + location + "/informations.json", "r") as f:
        informations = json.load(f)
        longitude, latitude = informations["location"]["longitude"], informations["location"]["latitude"]
        locations.append((longitude,latitude))

# Plot locations on map
fig, ax = plt.subplots()
ax.scatter([x[0] for x in locations], [x[1] for x in locations])
cx.add_basemap(ax, crs="epsg:4326")
plt.savefig("images_readme/positions_on_map.png")
plt.show()