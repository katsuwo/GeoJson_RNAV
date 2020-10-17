from RoutePoint import RoutePoint
import re
import json

class Route:
    def __init__(self, name):
        self.name = name
        self.points = []
        self.min_alt_str = []
        self.max_alt_str = []
        self.min_alt = []
        self.max_alt = []
    def add_point(self, name, latlng):
        new_point = RoutePoint(name,latlng)
        self.points.append(new_point)

    def convert(self):
        for pt in self.points:
            pt.convert_coordinate()

        for alt in self.max_alt_str:
            self.max_alt.append(alt.split("\n")[0])

        try:
            for altstr in self.min_alt_str:
                if altstr == "↓":
                    alt = old
                else:
                    alt = altstr
                alt_val = alt.replace("\n", "").split("[")
                match = re.search(r'FL\d+', str(alt_val[0]))
                if match is not None:
                    alt_val2 = alt_val[0].replace("FL", "")
                    self.min_alt.append(int(alt_val2) * 100)
                else:
                    self.min_alt.append(int(alt_val[0]))
                old = alt
        except Exception as e:
            print(e)

    def get_geo_Json_element(self):
        geojson = {}
        coordinates_list = []
        geometry = {}
        properties = {}

        for pt in self.points:
            coordinates_list.append([ pt.longitude, pt.latitude])

        geometry["type"] = "LineString"
        geometry["coordinates"] = coordinates_list
        properties["title"] = self.name

        geojson["type"] = "Feature"
        geojson["geometry"] = geometry
        geojson["properties"] = properties
        return geojson

