class RoutePoint:
    def __init__(self, name, latlng):
        self.name = name
        self.latlng = latlng
        self.latitude = 0.0
        self.longitude = 0.0

    def convert_coordinate(self):
        tmp = self.latlng.replace("E", "").replace("N", "").split(" ")
        lat_str = tmp[0]
        lng_str = tmp[1]
        self.latitude = self.convert_degminsec_to_deg(lat_str[:2], lat_str[2:])
        self.longitude = self.convert_degminsec_to_deg(lng_str[:3], lng_str[3:])

    def convert_degminsec_to_deg(self, deg_str, minsec_str):
        min = float(minsec_str[:2])
        sec = float(minsec_str[2:])
        deg = float(deg_str)
        deg = deg + (min / 60.0) + (sec / 3600.0)
        return deg

    def get_geo_Json_element(self):
        geojson = {}
        coordinates_list = []
        geometry = {}
        properties = {}

        geometry["type"] = "Point"
        geometry["coordinates"] = [self.longitude, self.latitude]
        properties["title"] = self.name

        geojson["type"] = "Feature"
        geojson["geometry"] = geometry
        geojson["properties"] = properties
        return geojson
