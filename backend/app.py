from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# MapmyIndia API credentials (replace with your actual credentials)
CLIENT_ID = "96dHZVzsAuu3SM87eXKedKLubwalQUSRwYl4MpDBxiQ3KIH7NuNWPZnu4Jk621sERbKzo3k9Nn3flLhWUsPOjQ=="
CLIENT_SECRET = "lrFxI-iSEg8pJyQYia5pH4Y_-JSDJiCj5q40cePPqO_RrjM3QVRrxwd1Rt5jHUn4lrZmXybsY6VyLMH3DhzQ7aRJnlXrOz9C"

# ✅ Default route to check if Flask is running
@app.route("/", methods=["GET"])
def home():
    return "Flask API is running!", 200

# ✅ Get Access Token from MapmyIndia API
def get_access_token():
    url = "https://outpost.mapmyindia.com/api/security/oauth/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(url, data=data)
    response_json = response.json()
    
    if "access_token" in response_json:
        return response_json["access_token"]
    else:
        raise Exception("Failed to get access token: " + str(response_json))

# ✅ Geocode addresses using MapmyIndia API
def get_coordinates(address):
    access_token = get_access_token()
    url = "https://atlas.mapmyindia.com/api/places/geocode"
    params = {"address": address}
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# ✅ Solve Travelling Salesman Problem (TSP)
def solve_tsp(distance_matrix):
    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    solution = routing.SolveWithParameters(search_params)

    if solution:
        route = []
        index = routing.Start(0)
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))
        return route
    else:
        return None

# ✅ Optimize Route API Endpoint
@app.route("/optimize-route", methods=["POST"])
def optimize_route():
    data = request.json
    addresses = data.get("addresses", [])

    if not addresses:
        return jsonify({"error": "No addresses provided"}), 400

    coordinates = []
    for address in addresses:
        geo_data = get_coordinates(address)
        if "copResults" in geo_data and len(geo_data["copResults"]) > 0:
            location = geo_data["copResults"][0]
            coordinates.append((location["latitude"], location["longitude"]))
        else:
            return jsonify({"error": f"Could not fetch coordinates for {address}"}), 400

    # Example: Generating a simple distance matrix (Replace with actual distance API)
    distance_matrix = [[0 if i == j else abs(i - j) * 10 for j in range(len(coordinates))] for i in range(len(coordinates))]

    optimal_order = solve_tsp(distance_matrix)

    return jsonify({"optimized_order": optimal_order})

if __name__ == "__main__":
    app.run(debug=True)
