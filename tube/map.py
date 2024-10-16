import json
from .components import Station, Line, Connection

class TubeMap:
    """
    Task 1: Complete the definition of the TubeMap class by:
    - completing the "import_from_json()" method

    Don't hesitate to divide your code into several sub-methods, if needed.

    As a minimum, the TubeMap class must contain these three member attributes:
    - stations: a dictionary that indexes Station instances by their id 
      (key=id (str), value=Station)
    - lines: a dictionary that indexes Line instances by their id 
      (key=id, value=Line)
    - connections: a list of Connection instances for the TubeMap 
      (list of Connections)
    """


    def __init__(self):
        self.stations = {}  # key: id (str), value: Station instance
        self.lines = {}  # key: id (str), value: Line instance
        self.connections = []  # list of Connection instances


    def load_json(self, filepath):
        try:
            with open(filepath, "r") as jsonfile:
                data = json.load(jsonfile)
            return data
        except FileNotFoundError:
            
            return None


    def form_station_dict(self, data):

        station_ls = data.get("stations")
        for station in station_ls:

            zone = station.get("zone")
            zone_set = set()
            
            if "." in zone:
                ind = zone.find(".")
                zone_set.add(int(zone[:ind]))
                zone_set.add(int(zone[:ind])+1)
            else:
                zone_set.add(int(zone))

            #print("Zoneset", zone_set)

            self.stations[station.get("id")] = Station(station.get("id"), station.get("name"), zone_set)


    def form_lines_dict(self, data):

        line_ls = data.get("lines")

        for line in line_ls:
            self.lines[line.get("line")] = Line(line.get("line"), line.get("name"))

    
    def form_connections_list(self, data):
        connection_ls = data.get("connections")

        for connection in connection_ls:

            station_set = set()
            station_set.add(self.stations.get(connection.get("station1")))
            station_set.add(self.stations.get(connection.get("station2")))

            self.connections.append(Connection(station_set,
                                 self.lines.get(connection.get("line")),
                                 int(connection.get("time")))
                                 )

    def import_from_json(self, filepath):
        """ Import tube map information from a JSON file.
        
        During the import process, the `stations`, `lines` and `connections` 
        attributes should be updated.

        You can use the `json` python package to easily load the JSON file at 
        `filepath`

        Note: when the indicated zone is not an integer (for instance: "2.5"), 
            it means that the station belongs to two zones. 
            For example, if the zone of a station is "2.5", 
            it means that the station is in both zones 2 and 3.

        Args:
            filepath (str) : relative or absolute path to the JSON file 
                containing all the information about the tube map graph to 
                import. If filepath is invalid, no attribute should be updated, 
                and no error should be raised.

        Returns:
            None
        """
        # TODO: Complete this method

        data = self.load_json(filepath)
        #print("data", data)

        if data is None:
            return

            # for station
        station_ls = data.get("stations")

        self.form_station_dict(data)

        self.form_lines_dict(data)

        self.form_connections_list(data)

        return


def test_import():
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")
    
    # view one example Station
    print(tubemap.stations[list(tubemap.stations)[0]])

    print("list", list(tubemap.stations)[0])
    
    # view one example Line
    print(tubemap.lines[list(tubemap.lines)[0]])
    
    # view the first Connection
    print(tubemap.connections[0])
    
    # view stations for the first Connection
    print([station for station in tubemap.connections[0].stations])


if __name__ == "__main__":
    test_import()
