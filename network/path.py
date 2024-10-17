import sys
import os 
from heapq import heapify, heappop, heappush

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

        station_ls = list(self.tubemap.stations.values())
        #print(set(station_ls))

        for station in station_ls:   #get id from station
            if start_station_name == station.name:
                start_id = station.id
            if end_station_name == station.name:
                end_id = station.id
        
        distances = {node: float("inf") for node in self.graph} #create distances dict
        distances[start_id] = 0  # Set the source value to 0

        pq = [(0, start_id)]   #find min_distances
        heapify(pq)

       # Create a set to hold visited nodes
        visited = set()

        while pq:  # While the priority queue isn't empty  
            current_distance, current_node = heappop(pq)

            if current_node in visited:  #check visited
                continue 
            visited.add(current_node)

            self.graph[current_node].items()

            for neighbor, weight in self.graph[current_node].items():  #Calculate from neighbours
                # Calculate the distance from current_node to the neighbor
                min_weight = min([int(connection.time) for connection in weight])

                tentative_distance = current_distance + min_weight
                if tentative_distance < distances[neighbor]:
                    distances[neighbor] = tentative_distance
                    heappush(pq, (tentative_distance, neighbor))

        print(distances)

        predecessors = {node: None for node in self.graph}

        for node, distance in distances.items():
            for neighbor, weight in self.graph[node].items():
                min_weight = min([int(connection.time) for connection in weight])
                if distances[neighbor] == distance + min_weight:
                    predecessors[neighbor] = node

        #_, predecessors = self.shortest_distances(source)

        path = []
        current_node = end_id

        # Backtrack from the target node using predecessors
        while current_node:
            path.append(self.tubemap.stations.get(current_node))
            current_node = predecessors[current_node]

        # Reverse the path and return it
        path.reverse()

        #print(path)


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
