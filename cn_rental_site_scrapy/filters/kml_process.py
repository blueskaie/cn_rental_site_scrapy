from fastkml import kml
from xml import etree

in_kml = 'gadm36_CHN_3.kml'
out_kml = 'gadm36_CHN_3_out.kml'
print(in_kml)

with open(in_kml, 'rt', encoding="utf-8") as myfile:
    doc = myfile.read()
    k = kml.KML()
    k.from_string(doc)
    document = list(k.features())
    placemarks = list(document[0].features())
    for placemark in placemarks:
        extended_data = placemark.extended_data.elements
        placemark.name=placemark.name + ', ' + extended_data[2].value

    with open(out_kml, 'w', encoding="utf-8") as outfile:
        outfile.write(k.to_string(prettyprint=True))