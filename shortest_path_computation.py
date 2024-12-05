import json
from flask import Flask, render_template, request, redirect, url_for
import googlemaps
from datetime import datetime
import os
import sys
from heapq import heapify, heappush, heappop

app = Flask(__name__)

# Setup GMAP API Client
with open('config.json', 'r') as f:
    config = json.load(f)
    google_api_key = config['googleApiKey']
gmap_client= googlemaps.Client(key= google_api_key)

class Dijkstra:
    def __init__(self, graph):
        self.graph = graph
        self.inf = sys.maxsize

    def shortest_path(self, src, dest):
        # Initialize the data structure to store shortest time and path
        node_data = {node: {'time': self.inf, 'path': []} for node in self.graph}
        node_data[src]['time'] = 0

        # Create a priority queue (min-heap)
        min_heap = [(0, src)]  # (time, node)
        visited = set()  # Set to track visited nodes

        while min_heap:
            # Pop the node with the smallest time
            current_time, temp = heappop(min_heap)

            # If the destination node is found, stop early
            if temp == dest:
                break

            if temp in visited:
                continue

            visited.add(temp)

            # Iterate through adjacent nodes of the current node
            for adj, time in self.graph[temp].items():
                if adj not in visited:
                    new_time = current_time + time
                    # Update the time and path if a shorter time is found
                    if new_time < node_data[adj]['time']:
                        node_data[adj]['time'] = new_time
                        node_data[adj]['path'] = node_data[temp]['path'] + [temp]
                        heappush(min_heap, (new_time, adj))

        # After the loop, check if we found a path to the destination
        if node_data[dest]['time'] == self.inf:
            return float('inf'), []  # No path found

        # Return the shortest time and the complete path
        return node_data[dest]['time'], node_data[dest]['path'] + [dest]

def shorten_and_bidirect_graph(distance_matrix_graph):
    # Instead of having a graph that is fully connexted, let's only have the graph with a node connected only to closest 2 nodes
    distance_matrix_graph_shorten = {}
    for src in distance_matrix_graph.keys():
        dest = list(distance_matrix_graph[src].keys())
        dist = list(distance_matrix_graph[src].values())

        # Create a list of tuples combining destination and distance, Sort the pairs by distance (ascending order) and Take shortest 2
        dest_dist_pairs = list(zip(dest, dist))
        sorted_dest_dist_pairs = sorted(dest_dist_pairs, key=lambda x: x[1])
        shortest_dest = [pair[0] for pair in sorted_dest_dist_pairs[:2]]
        shortest_dist = [pair[1] for pair in sorted_dest_dist_pairs[:2]]

        # Store them in the shortened graph dictionary
        distance_matrix_graph_shorten[src] = dict(zip(shortest_dest, shortest_dist))

    # Now let's make it bidirectonal (rever the soruce and destination) as well
    distance_matrix_graph_bidirectional = {}
    for src, destinations in distance_matrix_graph_shorten.items():
        for dest, dist in destinations.items():
            # Current source-destination pair
            if src not in distance_matrix_graph_bidirectional:
                distance_matrix_graph_bidirectional[src] = {}
            distance_matrix_graph_bidirectional[src][dest] = dist
            # Reverse destination-source pair if not already present
            if dest not in distance_matrix_graph_bidirectional:
                distance_matrix_graph_bidirectional[dest] = {}
            if src not in distance_matrix_graph_bidirectional[dest]:
                distance_matrix_graph_bidirectional[dest][src] = dist
    return distance_matrix_graph_bidirectional

def compute_shortest_path(selected_cities_list, user_choices):
    # Calculate distance and shortest path
    curr_time = datetime.now()
    distance_matrix_graph = {}

    print("Fetching driving duration from Google Maps API...")
    for i, src in enumerate(selected_cities_list):
        distances = {}
        for dest in selected_cities_list[i + 1 :]:
            direction_result = gmap_client.directions(
                src,
                dest,
                mode="driving",
                avoid="ferries",
                departure_time=curr_time,
                traffic_model="pessimistic",
                units="imperial",
            )
            if user_choices['traffic_type']=='Current':
                distances[dest] = direction_result[0]["legs"][0]["duration"]["value"]
            else:
                distances[dest] = direction_result[0]["legs"][0]["duration_in_traffic"]["value"]
        distance_matrix_graph[src] = distances

    print("Calcuating Duration Matrix...")
    # Shorten and birdirect the graph
    duration_matrix_graph_bidirectional= shorten_and_bidirect_graph(distance_matrix_graph)
    print("\nDuration Matrix Ready:")
    for i in duration_matrix_graph_bidirectional.keys():
        print(i,":")
        print("    ",duration_matrix_graph_bidirectional[i], '\n')
    
    print("\n Finding Shortest Path Using Dijkstra Algorithm...")
    # Pass the distance_matrix_graph to Dijkstra algorithm
    dijkstra = Dijkstra(duration_matrix_graph_bidirectional)
    shortest_time, shortest_path_result = dijkstra.shortest_path(
        user_choices["source"], user_choices["destination"]
    )
    print("Shortest Path Ready")
    print(shortest_path_result)


    # Get coordinates for all cities
    print("Collecting Coordinates Of All Cities")
    shortest_path_result_coordinates=[]
    city_coordinates = {}
    for city in selected_cities_list:
        geocode_result = gmap_client.geocode(city)
        if geocode_result:
            location = geocode_result[0]["geometry"]["location"]
            city_coordinates[city] = {"lat": location["lat"], "lng": location["lng"]}
            if city in shortest_path_result:
                shortest_path_result_coordinates.append({"lat": location["lat"], "lng": location["lng"]})


    # All possible connections (example)
    all_connectors = []
    for src in duration_matrix_graph_bidirectional.keys():
        for dest in duration_matrix_graph_bidirectional[src].keys():
            all_connectors.append(
                    {
                        "source": city_coordinates[src],
                        "destination": city_coordinates[dest],
                    }
            )
    #print("all_connectors:")
    #print(all_connectors)
    return shortest_time, shortest_path_result, shortest_path_result_coordinates, all_connectors


if __name__ == "__main__":
    app.run(debug=True)
