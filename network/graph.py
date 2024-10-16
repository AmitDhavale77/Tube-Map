import sys
import os 
#print(sys.path)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tube.map import TubeMap

class NeighbourGraphBuilder:
    """
    Task 2: Complete the definition of the NeighbourGraphBuilder class by:
    - completing the "build" method below (don't hesitate to divide your code 
      into several sub-methods, if needed)
    """

    def __init__(self):
        pass

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
        graph = {}

        #station_ls = [station for station in tubemap.connections[0].stations]



        for station_id in list(tubemap.stations): #contains list of all station ids , get_station_ids
            
            neighbours = {} #to store neighbouring stations
            for connect in tubemap.connections: # Iterates on each connection obj
                station_ls = [station for station in connect.stations] #converts the station set into list

                curr_stat_id = [stat.id for stat in station_ls]
                
                if station_id == station_ls[0].id:

                    if neighbours.get(station_ls[1].id):
                        neighbours[station_ls[1].id].append(connect)
                    else:
                        neighbours[station_ls[1].id] = [connect]
                
                if station_id == station_ls[1].id:

                    if neighbours.get(station_ls[0].id):
                        neighbours[station_ls[0].id].append(connect)
                    else:
                        neighbours[station_ls[0].id] = [connect]
                
            graph[station_id] = neighbours
            
        return graph


def test_graph():
    from tube.map import TubeMap
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")

    graph_builder = NeighbourGraphBuilder()
    graph = graph_builder.build(tubemap)

    print(graph["110"])


if __name__ == "__main__":
    test_graph()
