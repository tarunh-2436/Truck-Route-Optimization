import requests
import json
from ortools.constraint_solver import routing_enums_pb2, pywrapcp

API_KEY = "5b3ce3597851110001cf6248373813f428a84f8fa02d0c2693de0d44"

def get_coordinates(location):
    url = f"https://api.openrouteservice.org/geocode/search?api_key={API_KEY}&text={location}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if "features" in data and len(data["features"]) > 0:
            lon, lat = data["features"][0]["geometry"]["coordinates"]
            return float(lat), float(lon)
    
    print(f"❌ No coordinates found for {location}")
    return None

def get_distance_matrix(locations):
    coords = [[lon, lat] for lat, lon in locations]  
    url = "https://api.openrouteservice.org/v2/matrix/driving-car"
    
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "locations": coords,
        "metrics": ["distance"]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        data = response.json()
        if "distances" in data:
            return [[int(dist) if dist is not None else 999999 for dist in row] for row in data["distances"]]
        else:
            print("❌ Distance matrix missing in response")
            print("Response:", data)  
    else:
        print(f"❌ Error in distance API: {response.status_code}")
        print("Response:", response.text) 
    
    return None

def solve_tsp(distance_matrix):
    num_locations = len(distance_matrix)
    
    manager = pywrapcp.RoutingIndexManager(num_locations, 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    
    solution = routing.SolveWithParameters(search_parameters)
    
    if solution:
        route = []
        index = routing.Start(0)
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))
        return route
    return None

def main():
    num_locations = int(input("Enter number of locations: "))
    locations = []
    coordinates = []
    
    for i in range(num_locations):
        place = input(f"Enter location {i+1}: ")
        coord = get_coordinates(place)
        if coord:
            coordinates.append(coord)
            locations.append(place)

    if len(coordinates) < 2:
        print("❌ Not enough valid locations to proceed!")
        return
    
    distance_matrix = get_distance_matrix(coordinates)
    
    if not distance_matrix:
        print("❌ Unable to get distance matrix. Exiting.")
        return

    route = solve_tsp(distance_matrix)
    
    if route:
        print("\n🚀 Optimal Delivery Route:")
        for i in route:
            print(f"{i+1}. {locations[i]}")
    else:
        print("❌ Could not solve TSP.")

if __name__ == "__main__":
    main()
