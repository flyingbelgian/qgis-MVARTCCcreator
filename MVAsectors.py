import csv

coordinates = []
polygon = {}
polygons = []
datalayer = {}
datalayers = []

with open("D:\MVAsectorcoordinates_formatted.csv") as file:
    csvfile = csv.reader(file)
    firstline = True
    secondline = True
    prevlayer = ""
    prevpolygon = ""

    for line in csvfile:
        if firstline:
            firstline = False
            # pass
        else:
            # print(line)
            if line[3] != prevlayer and not secondline:
                # print("Different Layer")
                polygons.append(polygon)
                datalayers.append(datalayer)
                polygons = []
                coordinates = []
            elif line[5] != prevpolygon and not secondline:
                # print("Different Polygon")
                polygons.append(polygon)
                coordinates = []
            secondline = False
            x = float(line[0])
            y = float(line[1])
            elevft = int(line[3][0:4])
            elevm = round(elevft * 0.3048,2)
            z = elevm
            layerID = line[3]
            polygonID = line[5]
            coordinates.append((x,y,z))
            polygon = {"polygon":polygonID, "elevft":elevft, "elevm":elevm, "coordinates":coordinates}
            datalayer = {"layer": layerID, "polygons":polygons}
            # print(polygon)
            prevlayer = line[3]
            prevpolygon = line[5]

polygons.append(polygon)
datalayers.append(datalayer)

layer = QgsVectorLayer('polygon?crs=epsg:4326', 'MVA Sectors', 'memory')
pr = layer.dataProvider()
pr.addAttributes([
    QgsField("Surface Elev (ft)", QVariant.Int),
    QgsField("Surface Elev (m)", QVariant.Double)
])
layer.updateFields()

for datalayer in datalayers:
    # print(datalayer["layer"])
    # for polygon in datalayer["polygons"]:
    #     # print(f"  Polygon {polygon["polygon"]}: Elev ft ({polygon["elevft"]}) Elev m ({polygon["elevm"]})")
    #     for coordinate in polygon["coordinates"]:
    #         print(coordinate)

    polyfeature = QgsFeature()
    # points = [
    #     (528500,6857600,10),
    #     (528500,6857700,100),
    #     (528750,6857700,100),
    #     (528750,6857600,10)]
    polygons = []
    for polygon in datalayer["polygons"]:
        poly = QgsPolygon(QgsLineString([QgsPoint(*p) for p in polygon["coordinates"]]))
        polygons.append(poly)
    multipoly = QgsMultiPolygon(polygons)
    polyfeature.setGeometry(multipoly)
    polyfeature.setAttributes([polygon["elevft"],polygon["elevm"]])
    pr.addFeatures([polyfeature])
    
    
layer.updateExtents()
QgsProject.instance().addMapLayers([layer])