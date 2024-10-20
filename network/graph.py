import sys
import os 
#print(sys.path)

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tube.map import TubeMap

class NeighbourGraphBuilder:
    """
    Task 2: Complete the definition of the NeighbourGraphBuilder class by:
    - completing the "build" method below (don't hesitate to divide your code 
      into several sub-methods, if needed)
    """


    def __init__(self):
        pass


    def get_station_ids(self, tubemap):
        """ Get ids of all the Station instances present in the TubeMap

        Args:
            tubemap (obj) : An instance of the TubeMap class

        Returns:
            List: ids of all the Station intances
        """ 

        return list(tubemap.stations)


    def is_same_station_name(self, station_id, name_id):
        """ Check wether the given id is same as the id of the Station instance from the Connections object

        Args:
            station_id (str) : id of the current station node
            name_id (str): id of the station in the Connections object

        Returns:
            bool : Wether both the ids are same or not
        """ 

        return station_id == name_id


    def get_neighbours_for_connections(self, station_id, connections):
        """ To find the neighbours (connections associated with the current station node) of the current station node
        Args:
            station_id (str) : id of the current station node
            connections (list): A list of Connection object

        Returns:
            dict 
        """ 

        neighbours = {} #to store neighbouring stations

        for connect in connections: # Iterates on each connection obj

            station_ls = [station for station in connect.stations] #converts the station set into list

            if self.is_same_station_name(station_id, station_ls[0].id): 

                if neighbours.get(station_ls[1].id):
                    neighbours[station_ls[1].id].append(connect)
                else:
                    neighbours[station_ls[1].id] = [connect]
            
            if self.is_same_station_name(station_id, station_ls[1].id):

                if neighbours.get(station_ls[0].id):
                    neighbours[station_ls[0].id].append(connect)
                else:
                    neighbours[station_ls[0].id] = [connect]
            
        return neighbours
    
    def build(self, tubemap):
        """ Builds a graph encoding neighbouring connections between stations.

        ----------------------------------------------

        The returned graph should be a dictionary having the following form:
        {
            "station_A_id": {
                "neighbour_station_1_id": [
                                connection_1 (instance of Connection),
                                connection_2 (instance of Connection),
                                ...],

                "neighbour_station_2_id": [
                                connection_1 (instance of Connection),
                                connection_2 (instance of Connection),
                                ...],
                ...
            }

            "station_B_id": {
                ...
            }

            ...

        }

        ----------------------------------------------

        For instance, knowing that the id of "Hammersmith" station is "110",
        graph['110'] should be equal to:
        {
            '17': [
                Connection(Hammersmith<->Barons Court, District Line, 1),
                Connection(Hammersmith<->Barons Court, Piccadilly Line, 2)
                ],

            '209': [
                Connection(Hammersmith<->Ravenscourt Park, District Line, 2)
                ],

            '101': [
                Connection(Goldhawk Road<->Hammersmith, Hammersmith & City Line, 2)
                ],

            '265': [
                Connection(Hammersmith<->Turnham Green, Piccadilly Line, 2)
                ]
        }

        ----------------------------------------------

        Args:
            tubemap (TubeMap) : tube map serving as a reference for building 
                the graph.

        Returns:
            graph (dict) : as described above. 
                If the input data (tubemap) is invalid, 
                the method should return an empty dict.
        """
        # TODO: Complete this method
       

        if not isinstance(tubemap, TubeMap): # Check wether the tubemap object is a valid object or not
            return {}
        
        graph = {}

        for station_id in self.get_station_ids(tubemap):  
                
            graph[station_id] = self.get_neighbours_for_connections(station_id, 
                                                                tubemap.connections)
            
        return graph


def test_graph():
    from tube.map import TubeMap
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")

    graph_builder = NeighbourGraphBuilder()
    graph = graph_builder.build(tubemap)

    print(graph["11"]["163"])

    print(graph["163"]["11"])


if __name__ == "__main__":
    test_graph()
