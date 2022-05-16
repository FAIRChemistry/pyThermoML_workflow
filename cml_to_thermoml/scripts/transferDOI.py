import os
import xml.etree.ElementTree as ET

ET.register_namespace("", "http://www.xml-cml.org/schema")
ET.register_namespace("", "http://www.iupac.org/namespaces/ThermoML")
cmlfiles = os.listdir("./cml")
tmlfiles = os.listdir("./thermoml")
DOIs = []
def getDOIofNewXML():
    for file in cmlfiles:
        tree = ET.parse("./cml/" + file)
        root = tree.getroot()
        x = root.findtext('.//{http://www.xml-cml.org/schema}scalar')
        DOIs.append(x)
    
    return DOIs

def removeSubsection(deleteTag, parent):
    for elem in parent.findall('.//{http://www.iupac.org/namespaces/ThermoML}' + deleteTag):
        parent.remove(elem)

def insertDOItoThermoml():
    #gets tree of each file in output
    tree = ET.parse("./output/Gyg2020N,N-diethylethanol ammonium chloride_glycerol_DOI1.xml")
    root = tree.getroot()
    x = []
    for elem in list(root):
        y = elem.findall(".//{http://www.iupac.org/namespaces/ThermoML}nCombExpandUncertValue")
        for uncertainty in y:
            uncertainty.text = str(round(float(uncertainty.text)*1000, 12))
            

    ET.dump(tree)
    tree.write("./output/Gyg2020N,N-diethylethanol ammonium chloride_glycerol_DOI1.xml")
insertDOItoThermoml()



