import xml.etree.ElementTree as ET
from shutil import copyfile
import os

#returns each DOI stored in an .xml file as array
def getDOIs(root):
    DOIs = []
    for elem in root[0][0]:
        if elem[0][0][0].text not in DOIs:
            DOIs.append(elem[0][0][0].text)
    return DOIs

#creates as many XML files as different DOIs exist
def createCopysWithDeletedDOI(DOIs, filename):
    print(DOIs)
    for i in range(len(DOIs)):
        #create file as copy of mixed .xml file
        #syntax "oldfilename_DOIx.xml" where x is number of contained DOI
        tempName = "temp_" + str(i) + ".xml"
        copyfile(filename, tempName)
        
        #read copied .xml file
        tree = ET.parse(tempName)
        root = tree.getroot()
        for parent in root.findall('{http://www.xml-cml.org/schema}module/{http://www.xml-cml.org/schema}module'):
            for exp in parent.findall(".//{http://www.xml-cml.org/schema}module"):
                #removes each "<module dictRef="des:experiment"> tag if tag unequal to current DOI
                if exp.findtext('.//{http://www.xml-cml.org/schema}scalar') != DOIs[i]:
                    parent.remove(exp)

        begFilename = filename[:-4]
        tree.write(begFilename + "_DOI" + str(i+1) + ".xml")
        
        os.remove(tempName)


if __name__ == "__main__":
    ET.register_namespace("des", "https://fairdomhub.org/data_files/3045?version=4")
    ET.register_namespace("units", "http://www.xml-cml.org/units/units")
    ET.register_namespace("xsd", "http://www.w3.org/2001/XMLSchema")
    ET.register_namespace("cmlx", "http://www.xml-cml.org/schema/cmlx")
    ET.register_namespace("convention", "http://www.xml-cml.org/convention/")
    ET.register_namespace("", "http://www.xml-cml.org/schema")

    
        
    filename = 'cml_multiple_dois/methanol.xml'
    tree = ET.parse(filename)
    root = tree.getroot()
    createCopysWithDeletedDOI(getDOIs(root), filename)