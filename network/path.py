import sys
import os 
import heapq # To determine the smallest weighted node in the Djikistra's algorithm

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from network.graph import NeighbourGraphBuilder

class PathFinder:
    """
    Task 3: Complete the definition of the PathFinder class by:
    - completing the definition of the __init__() method (if needed)
    - completing the "get_shortest_path()" method (don't hesitate to divide 
      your code into several sub-methods)
    """


    def __init__(self, tubemap):
        """
        Args:
            tubemap (TubeMap) : The TubeMap to use.
        """
        self.tubemap = tubemap

        graph_builder = NeighbourGraphBuilder()
        self.graph = graph_builder.build(self.tubemap)
        
        # Feel free to add anything else needed here.


    def get_station_id(self, station_name):
        """ To find the id of the given station name
        Args:
            station_name (str) : Name of the given station

        Returns:
            str : station id of the name is found else None
        """ 

        for station in self.tubemap.stations.values():

            if station.name == station_name:
                return station.id

        return None  # Return None if station not found


    def initialize_distances(self, start_id):
        """ Initializes the distance dictionary for Dijkstra's algorithm.
        Args:
            start_id (str) : The id of the station in the starting point

        Returns:
            dict : Dictionary where each node is assigned a value of inf except the start node 
        """ 

        distances = {node: float("inf") for node in self.graph}
        distances[start_id] = 0  # Set the start station distance to 0

        return distances


    def find_dijkstra_shortest_path(self, start_id):
        """ Executes Dijkstra's algorithm to compute shortest paths from start_id
        Args:
            start_id (str) : The id of the station in the starting point

        Returns:
            dict : Dictionary where each node is assigned their updated values 
        """ 
        distances = self.initialize_distances(start_id) 

        pq = [(0, start_id)]  # Priority queue to hold (distance, station_id)

        heapq.heapify(pq) # Add the tuple to the priority queue 
        
        visited = set() # Create a set of visited nodes

        while pq:
            current_distance, current_node = heapq.heappop(pq) # Remove an element from the priority queue

            if current_node in visited: # Check wether the node is visited or not
                continue

            visited.add(current_node) # If not then add it to the visited section

            for neighbor, weight in self.graph[current_node].items(): # neighbor = Station id, weight = list of Connections objects

                min_weight = min([int(connection.time) for connection in weight])

                tentative_distance = current_distance + min_weight

                if tentative_distance < distances[neighbor]: #\

                    distances[neighbor] = tentative_distance
                    heapq.heappush(pq, (tentative_distance, neighbor))

        return distances


    def compute_predecessors(self, distances):
        """ Creating a dictionary of predecessors to rebuild the shortest path
        Args:
            distances (dict) : Dictionary where each node is assigned their updated values

        Returns:
            dict 
        """ 

        predecessors = {node: None for node in self.graph}

        for node, distance in distances.items(): # Check each neighbor of the current node

            for neighbor, weight in self.graph[node].items():

                min_weight = min([int(connection.time) for connection in weight])

                if distances[neighbor] == distance + min_weight:
                    predecessors[neighbor] = node

        return predecessors

    def reconstruct_path(self, end_id, predecessors):
        """ Reconstructs the shortest path from end_id using the predecessors.
        Args:
            end_id (str) : The id of the terminal station
            predecessors (dict) : A dictionary mapping each node to its predecessor node on the shortest path

        Returns:
            list : A list containing all the stations visited while traversing through the shortest path 
        """ 
        path = []
        current_node = end_id

        # Backtrack from the target node using predecessors
        while current_node:
            path.append(self.tubemap.stations.get(current_node))
            current_node = predecessors[current_node]

        # Reverse the path to get the correct order
        path.reverse()
        return path

    def get_shortest_path(self, start_station_name, end_station_name):
        """ Find ONE shortest path from start_station_name to end_station_name.
        
        The shortest path is the path that takes the least amount of time.

        For instance, get_shortest_path('Stockwell', 'South Kensington') 
        should return the list:
        [Station(245, Stockwell, {2}), 
         Station(272, Vauxhall, {1, 2}), 
         Station(198, Pimlico, {1}), 
         Station(273, Victoria, {1}), 
         Station(229, Sloane Square, {1}), 
         Station(236, South Kensington, {1})
        ]

        If start_station_name or end_station_name does not exist, return None.
        
        You can use the Dijkstra algorithm to find the shortest path from
        start_station_name to end_station_name.

        Find a tutorial on YouTube to understand how the algorithm works, 
        e.g. https://www.youtube.com/watch?v=GazC3A4OQTE
        
        Alternatively, find the pseudocode on Wikipedia: https://en.wikipedia.org/wiki/Dijkstra's_algorithm#Pseudocode

        Args:
            start_station_name (str): name of the starting station
            end_station_name (str): name of the ending station

        Returns:
            list[Station] : list of Station objects corresponding to ONE 
                shortest path from start_station_name to end_station_name.
                Returns None if start_station_name or end_station_name does not 
                exist.
                Returns a list with one Station object (the station itself) if 
                start_station_name and end_station_name are the same.
        """
        # TODO: Complete this method

        start_id = self.get_station_id(start_station_name)
        end_id = self.get_station_id(end_station_name)

        if start_id is None or end_id is None:
            return None  # Return None if either station does not exist

        if start_id == end_id:
            return [self.tubemap.stations.get(start_id)]  # Return single station if same

        distances = self.find_dijkstra_shortest_path(start_id)

        predecessors = self.compute_predecessors(distances)

        path = self.reconstruct_path(end_id, predecessors)

        return path


def test_shortest_path():
    from tube.map import TubeMap
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")
    
    path_finder = PathFinder(tubemap)
    stations = path_finder.get_shortest_path("Covent Garden", "Green Park")
    print(stations)
    
    station_names = [station.name for station in stations]
    expected = ["Covent Garden", "Leicester Square", "Piccadilly Circus", 
                "Green Park"]
    assert station_names == expected


if __name__ == "__main__":
    test_shortest_path()
