
import xlrd
import re
import json
from Route import Route

class GeoJson_RNAV:
    def __init__(self):
        pass

    def workbook_open(self, filename):
        wb = xlrd.open_workbook(filename)
        sheets = wb.sheets()
        routes = []
        for sheetname in wb.sheet_names():
            sheet = wb.sheet_by_name(sheetname)
            for y in range(0, sheet.nrows):
                match = re.search(r'Y\d+', str(sheet.cell(y, 0).value))
                if match is not None or '(continued)' in str(sheet.cell(y, 0).value):
                    if '(continued)' in str(sheet.cell(y, 0).value):
                        rt = routes.pop(len(routes) - 1)
                    else:
                        route_name = match.group(0)
                        rt = Route(route_name)
                    route_points = str(sheet.cell(y, 0).value).split('\n')

                    is_lat_lng = False
                    point_name = ""
                    for point in route_points:
                        if '(continued)' in point:
                            continue
                        if route_name in point:
                            continue
                        if '(RNAV5)' in point:
                            continue
                        if 'VOR/DME' in point and 'DME/DME' in point and 'INS' in point and 'IRS' in point and 'GNSS' in point:
                            continue
                        if '(*1)' in point or '(*2)' in point or '(*3)' in point or '(*4)' in point or '(*5)' in point:
                            continue

                        if not is_lat_lng:
                            point_name = point
                            is_lat_lng = True
                        else:
                            rt.add_point(point_name, point)
                            is_lat_lng = False
                    for yy in range(y + 1, sheet.nrows):
                        max_value = str(sheet.cell(yy, 4).value)
                        min_value = str(sheet.cell(yy, 5).value)
                        min_value2 = str(sheet.cell(yy, 6).value)
                        if max_value is not "":
                            rt.max_alt_str.append(max_value)
                        if min_value is not "":
                            rt.min_alt_str.append(min_value)
                        elif min_value2 is not "":
                            rt.min_alt_str.append(min_value2)
                        if max_value is "" and min_value is "" and min_value2 is "":
                            break
                    routes.append(rt)

        print("--------------------")
        features = []
        for rt in routes:
            rt.convert()
            features.append(rt.get_geo_Json_element())
        geoJson = {}
        geoJson["type"] = "FeatureCollection"
        geoJson["features"] = features
        output = open("RNAV_ROUTE.geojson", "w")
        rnavFile = json.dump(geoJson, output)
        print(rnavFile)

        features_wpt = []
        features_wpt_rpt = []
        for rt in routes:
            for pt in rt.points:
                if "\u25b2" in pt.name:
                    features_wpt_rpt.append(pt.get_geo_Json_element())
                else:
                    features_wpt.append(pt.get_geo_Json_element())

        geoJson = {}
        geoJson["type"] = "FeatureCollection"
        geoJson["features"] = features_wpt_rpt
        output = open("RNAV_RPT_WPT.geojson", "w")
        ptfile = json.dump(geoJson, output)
        print(ptfile)

        geoJson["features"] = features_wpt
        output = open("RNAV_WPT.geojson", "w")
        ptfile = json.dump(geoJson, output)
        print(ptfile)


def main():
    geo = GeoJson_RNAV()
    wb = geo.workbook_open("./JP_ENR.xlsx")


if __name__ == '__main__':
    main()
