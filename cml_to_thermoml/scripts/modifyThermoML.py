import os
import xml.etree.ElementTree as ET
import lxml.etree as ETL
files = os.listdir("cml2ThermoML")

namespace = {'ThermoML': 'http://www.iupac.org/namespaces/ThermoML'}
ET.register_namespace("", "http://www.iupac.org/namespaces/ThermoML")

def getSignificantDigits(string1):
    print(string1)
    if string1 == "0":
        return 0
    if string1 == "0.0":
        return 0
    else:
        firstNonZero = 0
        if string1.count(".") >= 1:
            lastNonZero = len(string1)-1
            j = len(string1)-1
        else:
            lastNonZero = len(string1)
            j = len(string1)

        i = 0
        j = len(string1)-1

        while (string1[i] == "0" or string1[i] == "."):
            i += 1
            if string1[i]==".":
                pass
            else:
                firstNonZero += 1
            
        while (string1[j] == "0" or string1[j] == "."):
            j -= 1
            if string1[j]==".":
                pass
            else:
                lastNonZero = lastNonZero -1

        sigDigits = lastNonZero - firstNonZero
        
        return sigDigits

def deleteRedundantDOIs():
    deletefiles = []
    for file in files:
        tree = ET.parse("converted cml to thermoML/" + file)
        root = tree.getroot()
        
        for citation in root.findall('ThermoML:Citation', namespace):
            for sDOI in citation.findall('ThermoML:sDOI', namespace):
                if sDOI.text == "Abdullah and Kadhom (IJERD)":
                    deletefiles.append(file)


    for file in deletefiles:
        os.remove("converted cml to thermoML/" + file)

def correctNumValues():
    files = os.listdir("converted cml to thermoML/")
    for file in files:
        print("\n currently on: " + str(file))
        tree = ET.parse("converted cml to thermoML/" + file)
        root = tree.getroot()
        varValues = []
        sigDigits = []
        propValues = []
        sigDigitsProp = []

        ##variable digits
        for nVarValue in root.iter('{http://www.iupac.org/namespaces/ThermoML}nVarValue'):
            #checks wheter molefraction vs. temperature
            if float(nVarValue.text) < 1.01:
                round(float(nVarValue.text), 2)
                nVarValue.text = str(round(float(nVarValue.text), 2))
            varValues.append(nVarValue.text)
        
        for value in varValues:
            sigDigits.append(getSignificantDigits(value))
        
        digitNumber = 0
        for nVarDigits in root.iter('{http://www.iupac.org/namespaces/ThermoML}nVarDigits'):
            nVarDigits.text = str(sigDigits[digitNumber])
            digitNumber += 1
        

        #property digits
        for nPropValue in root.iter('{http://www.iupac.org/namespaces/ThermoML}nPropValue'):
            propValues.append(nPropValue.text)
        for property in propValues:
            sigDigitsProp.append(getSignificantDigits(property))
        
        digitNumberProp = 0
        for nPropDigits in root.iter('{http://www.iupac.org/namespaces/ThermoML}nPropDigits'):
            nPropDigits.text = str(sigDigitsProp[digitNumberProp])
            digitNumberProp += 1
        
        ET.register_namespace("", "http://www.iupac.org/namespaces/ThermoML")
        #tree.write("converted cml to thermoML/" + file)

def viscToTransportProp():
    for filename in files:
        parser = ET.XMLParser(encoding="utf-8")
        tree = ET.parse("cml2ThermoML/" + filename, parser = parser)
        root = tree.getroot()
        
        for elem in root.iter():
            if elem.tag == "{http://www.iupac.org/namespaces/ThermoML}VolumetricProp":
                elem.tag = "{http://www.iupac.org/namespaces/ThermoML}TransportProp"
        tree.write('./cml2ThermoML/' + filename , xml_declaration=True, method='xml', encoding="utf8")
viscToTransportProp()