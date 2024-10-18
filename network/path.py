import sys
import os 
import heapq

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
        """Returns the station ID given the station name."""
        for station in self.tubemap.stations.values():
            if station.name == station_name:
                return station.id
        return None  # Return None if station not found

    def initialize_distances(self, start_id):
        """Initializes the distance dictionary for Dijkstra's algorithm."""
        distances = {node: float("inf") for node in self.graph}
        distances[start_id] = 0  # Set the start station distance to 0
        return distances

    def dijkstra_shortest_path(self, start_id):
        """Executes Dijkstra's algorithm to compute shortest paths from start_id."""
        distances = self.initialize_distances(start_id)
        pq = [(0, start_id)]  # Priority queue to hold (distance, station_id)
        heapq.heapify(pq)
        visited = set()

        while pq:
            current_distance, current_node = heapq.heappop(pq)

            if current_node in visited:
                continue
            visited.add(current_node)

            for neighbor, weight in self.graph[current_node].items():
                min_weight = min([int(connection.time) for connection in weight])
                tentative_distance = current_distance + min_weight

                if tentative_distance < distances[neighbor]:
                    distances[neighbor] = tentative_distance
                    heapq.heappush(pq, (tentative_distance, neighbor))

        return distances

    def compute_predecessors(self, distances):
        """Creates the predecessors dictionary to reconstruct the shortest path."""
        predecessors = {node: None for node in self.graph}
        for node, distance in distances.items():
            for neighbor, weight in self.graph[node].items():
                min_weight = min([int(connection.time) for connection in weight])
                if distances[neighbor] == distance + min_weight:
                    predecessors[neighbor] = node
        return predecessors

    def reconstruct_path(self, end_id, predecessors):
        """Reconstructs the shortest path from end_id using the predecessors."""
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

        # Step 1: Run Dijkstra's algorithm to find shortest distances
        distances = self.dijkstra_shortest_path(start_id)

        # Step 2: Compute predecessors to reconstruct the shortest path
        predecessors = self.compute_predecessors(distances)

        # Step 3: Reconstruct the shortest path from the start to the end station
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
