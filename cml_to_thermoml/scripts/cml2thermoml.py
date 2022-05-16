import xml.etree.ElementTree as ET
import lxml.etree as etree

#This is a preliminary script to transform chemical markup language (CML) documents
#to ThermoML. Since ThermoML provides way more information and has a different data structure,
#a lot of tags wont be constructed

#used lxml.etree to include xsi schema
def create_xml_subelement_with_list(parent,name,list):
    child = etree.SubElement(parent, name)
    list.append(child)
    return child
    
def getNumberOfDigits(value):
    if value.isalnum():
        return str(len(value))
    else:
        return str(len(value)-1)

def create_version_info(DataReport):
    Version = etree.SubElement(DataReport, 'Version')
    nVersionMajor = etree.SubElement(Version, "nVersionMajor")
    nVersionMajor.text = "2"
    nVersionMinor = etree.SubElement(Version, "nVersionMinor")
    nVersionMinor.text = "0"

    return Version
def create_citation(docTitle, docDOI, DataReport, authors):    
    Elements = []
    Citation = create_xml_subelement_with_list(DataReport, 'Citation',Elements)
    for i in range(len(authors)):
        sAuthor = create_xml_subelement_with_list(Citation,"sAuthor",Elements)
        sAuthor.text = authors[i]
    sTitle = create_xml_subelement_with_list(Citation,"sTitle",Elements)
    sTitle.text = docTitle
    sDOI = create_xml_subelement_with_list(Citation,"sDOI",Elements)
    sDOI.text = docDOI
    return Citation

def create_multipleCompound(docComponents, DataReport):
    for i in range(len(docComponents)):
        create_compound(docComponents, i, DataReport)
        
def create_compound(docComponents, i, DataReport):
    #compound_csv , ncommon_names, nsamples = preproc_compound(compound_csv)
    #print("Creating compound " +str(i))
    
    Elements = []
    empty = [] #used for elements which shall not be filled out
    
    #createCompounds
    Compound = etree.SubElement(DataReport, 'Compound')
    RegNum = create_xml_subelement_with_list(Compound,"RegNum",empty)
    nOrgNum = create_xml_subelement_with_list(RegNum,"nOrgNum",Elements)
    nOrgNum.text = str(i+1)    
    sStandardInChI = create_xml_subelement_with_list(Compound,"sStandardInChI",Elements)
    sStandardInChI.text = str(docComponents[i][0])
    sStandardInChIKey = create_xml_subelement_with_list(Compound,"sStandardInChIKey",Elements)
    sStandardInChIKey.text = str(docComponents[i][1])
    sCommonName = create_xml_subelement_with_list(Compound,"sCommonName",Elements)
    sCommonName.text = str(docComponents[i][2])
    sSmiles = create_xml_subelement_with_list(Compound,"sSmiles",Elements)
    sSmiles.text = str(docComponents[i][3])
        
    return Compound

def create_data_entry(cmldata, docComponents, DataReport):
    Elements = []
    empty = [] #used for elements which shall not be filled out
    PureOrMixtureData = etree.SubElement(DataReport, 'PureOrMixtureData')
    
    #Info about the Dataframe
    nPureOrMixtureDataNumber = create_xml_subelement_with_list(PureOrMixtureData,"nPureOrMixtureDataNumber",Elements)
    nPureOrMixtureDataNumber.text = "1"

    for n in range(len(docComponents)): #CML probably provides only 2 compounds
        Component = create_xml_subelement_with_list(PureOrMixtureData,"Component",empty)
        RegNum = create_xml_subelement_with_list(Component,"RegNum",empty)
        nOrgNum = create_xml_subelement_with_list(RegNum,"nOrgNum",Elements)
        nOrgNum.text = str(n+1)
        #nSampleNm = create_xml_subelement_with_list(Component,"nSampleNm",Elements)

    #eExpPurpose = create_xml_subelement_with_list(PureOrMixtureData,"eExpPurpose",Elements)
    sCompiler = create_xml_subelement_with_list(PureOrMixtureData,"sCompiler",Elements)
    sCompiler.text = "Matthias Gueltig"
    #sContributor = create_xml_subelement_with_list(PureOrMixtureData,"sContributor",Elements)
    #dateDateAdded = create_xml_subelement_with_list(PureOrMixtureData,"dateDateAdded",Elements)
    
    #Info about the measured property
    Property =  create_xml_subelement_with_list(PureOrMixtureData,"Property",empty)
    nPropNumber =  create_xml_subelement_with_list(Property,"nPropNumber",Elements)
    nPropNumber.text = "1"
    PropertyMethodID =  create_xml_subelement_with_list(Property,"Property-MethodID",empty)
    PropertyGroup =  create_xml_subelement_with_list(PropertyMethodID,"PropertyGroup",empty) 
    TransportProp  =  create_xml_subelement_with_list(PropertyGroup,"VolumetricProp",empty) 
    ePropName  =  create_xml_subelement_with_list(TransportProp,"ePropName",Elements) 
    ePropName.text = "Viscosity, Pa*s"
    #eMethodName  =  create_xml_subelement_with_list(TransportProp,"eMethodName",Elements) 
    #PropPhaseID =  create_xml_subelement_with_list(Property,"PropPhaseID",empty)
    #ePropPhase = create_xml_subelement_with_list(PropPhaseID,"ePropPhase",Elements)
    #ePropPhase.text = 
    #ePresentation = create_xml_subelement_with_list(Property,"ePresentation",Elements)
    
    #Uncertainty of the property
    CombinedUncertainty = create_xml_subelement_with_list(Property,"CombinedUncertainty",empty)
    nCombUncertAssessNum = create_xml_subelement_with_list(CombinedUncertainty,"nCombUncertAssessNum",Elements)
    nCombUncertAssessNum.text = "1"
    #sCombUncertEvaluator = create_xml_subelement_with_list(CombinedUncertainty,"sCombUncertEvaluator",Elements)
    #eCombUncertEvalMethod = create_xml_subelement_with_list(CombinedUncertainty,"eCombUncertEvalMethod",Elements)
    #nCombUncertLevOfConfid = create_xml_subelement_with_list(CombinedUncertainty,"nCombUncertLevOfConfid",Elements)
    
    #Phase info
    #PhaseID = create_xml_subelement_with_list(PureOrMixtureData,"PhaseID",empty)
    #ePhase = create_xml_subelement_with_list(PhaseID,"ePhase",Elements)
    
    #Constraints
    #Constraint = create_xml_subelement_with_list(PureOrMixtureData,"Constraint",empty) 
    #nConstraintNumber = create_xml_subelement_with_list(Constraint,"nConstraintNumber",Elements) 
    #ConstraintID = create_xml_subelement_with_list(Constraint,"ConstraintID",empty) 
    #ConstraintType = create_xml_subelement_with_list(ConstraintID,"ConstraintType",empty) 
    
    #ePressure = create_xml_subelement_with_list(ConstraintType,"ePressure",Elements) 
    #ConstraintPhaseID = create_xml_subelement_with_list(Constraint,"ConstraintPhaseID",empty)  
    #eConstraintPhase = create_xml_subelement_with_list(ConstraintPhaseID,"eConstraintPhase",Elements)  
    #nConstraintValue = create_xml_subelement_with_list(Constraint,"nConstraintValue",Elements)
    #nConstrDigits = create_xml_subelement_with_list(Constraint,"nConstrDigits",Elements)
    
    #Variable declaration
    Variable = create_xml_subelement_with_list(PureOrMixtureData,"Variable",empty)
    nVarNumber = create_xml_subelement_with_list(Variable,"nVarNumber",Elements)
    nVarNumber.text = "1"
    VariableID = create_xml_subelement_with_list(Variable,"VariableID",empty)
    VariableType = create_xml_subelement_with_list(VariableID,"VariableType",empty)
    eTemperature = create_xml_subelement_with_list(VariableType,"eTemperature",Elements)
    eTemperature.text =  "Temperature, K"

    for i in range(len(docComponents)):
        Variable = create_xml_subelement_with_list(PureOrMixtureData,"Variable",empty)
        nVarNumber = create_xml_subelement_with_list(Variable,"nVarNumber",Elements)
        nVarNumber.text = str(i+2)
        VariableID = create_xml_subelement_with_list(Variable,"VariableID",empty)
        VariableType = create_xml_subelement_with_list(VariableID,"VariableType",empty)
        eComponentComposition = create_xml_subelement_with_list(VariableType,"eComponentComposition",Elements)
        eComponentComposition.text = "Mole fraction"
        RegNum = create_xml_subelement_with_list(VariableID,"RegNum",empty) 
        nOrgNum = create_xml_subelement_with_list(RegNum,"nOrgNum",Elements)
        nOrgNum.text = str(i+1)
        
    #Phase info again - wh? needed?
    #VarPhaseID = create_xml_subelement_with_list(Variable,"VarPhaseID",empty)
    #eVarPhase = create_xml_subelement_with_list(VarPhaseID,"eVarPhase",Elements)    
    #eVarPhase.text = "liquid"

    nDatapoints = len(cmldata)

    for i in range(nDatapoints):
        NumValues = create_xml_subelement_with_list(PureOrMixtureData,"NumValues",empty)

        #Temperature
        VariableValue = create_xml_subelement_with_list(NumValues,"VariableValue",empty)
        nVarNumber = create_xml_subelement_with_list(VariableValue,"nVarNumber",Elements)
        #temp is always one
        nVarNumber.text = str(1)
        nVarValue = create_xml_subelement_with_list(VariableValue,"nVarValue",Elements)
        nVarValue.text = str(cmldata[i][-1])
        nVarDigits = create_xml_subelement_with_list(VariableValue,"nVarDigits",Elements)
        nVarDigits.text = getNumberOfDigits(str(cmldata[i][-1]))
        #docComponents order is 0: water 1: first compound in filename, 2: second compound in filename...
        #just water
        if len(docComponents) == 1:               
            #water molfraction is always given
            molFracWater = cmldata[i][5]
            #create Molfraction of Water entry
            VariableValue = create_xml_subelement_with_list(NumValues,"VariableValue",empty)
            nVarNumber = create_xml_subelement_with_list(VariableValue,"nVarNumber",Elements)
            #first mole fraction (water) has varNumber 2
            nVarNumber.text = str(2)
            nVarValue = create_xml_subelement_with_list(VariableValue,"nVarValue",Elements)
            nVarValue.text = str(molFracWater)
            nVarDigits = create_xml_subelement_with_list(VariableValue,"nVarDigits",Elements)
            nVarDigits.text = getNumberOfDigits(str(molFracWater))

        #water + comp 1  
        if len(docComponents) == 2:
        #water molfraction is always given
            molFracWater = cmldata[i][5]
            #create Molfraction of Water entry
            VariableValue = create_xml_subelement_with_list(NumValues,"VariableValue",empty)
            nVarNumber = create_xml_subelement_with_list(VariableValue,"nVarNumber",Elements)
            #first mole fraction (water) has varNumber 2
            nVarNumber.text = str(2)
            nVarValue = create_xml_subelement_with_list(VariableValue,"nVarValue",Elements)
            nVarValue.text = str(molFracWater)
            nVarDigits = create_xml_subelement_with_list(VariableValue,"nVarDigits",Elements)
            nVarDigits.text = getNumberOfDigits(str(molFracWater))
            restFrac = 1-float(cmldata[i][5])
            
            VariableValue = create_xml_subelement_with_list(NumValues,"VariableValue",empty)
            nVarNumber = create_xml_subelement_with_list(VariableValue,"nVarNumber",Elements)
            #first mole fraction (water) has varNumber 2
            nVarNumber.text = str(3)
            nVarValue = create_xml_subelement_with_list(VariableValue,"nVarValue",Elements)
            
            roundedRestFrac = round(restFrac, 10)
            nVarValue.text = str(roundedRestFrac)
            nVarDigits = create_xml_subelement_with_list(VariableValue,"nVarDigits",Elements)
            nVarDigits.text = getNumberOfDigits((str(roundedRestFrac)))
            
        #two additional components (water + comp1 + comp2)
        if len(docComponents) == 3:
            restFrac = 1-float(cmldata[i][5])
            partComp1, partComp2 = float(cmldata[i][4]).as_integer_ratio()
            sumParts = partComp1 + partComp2
            partfrac1 = partComp1/sumParts
            partfrac2 = partComp2/sumParts
            fracComp1 = partfrac1 * restFrac
            fracComp2 = partfrac2 * restFrac
            roundedFracComp1 = round(fracComp1, 10)
            roundedFracComp2 = round(fracComp2, 10)
            #water molfraction is always given
            molFracWater = cmldata[i][5]
            #create Molfraction of Water entry
            VariableValue = create_xml_subelement_with_list(NumValues,"VariableValue",empty)
            nVarNumber = create_xml_subelement_with_list(VariableValue,"nVarNumber",Elements)
            #first mole fraction (water) has varNumber 2
            nVarNumber.text = str(2)
            nVarValue = create_xml_subelement_with_list(VariableValue,"nVarValue",Elements)
            nVarValue.text = str(molFracWater)
            nVarDigits = create_xml_subelement_with_list(VariableValue,"nVarDigits",Elements)
            nVarDigits.text = getNumberOfDigits(str(molFracWater))
            
            #comp1
            VariableValue = create_xml_subelement_with_list(NumValues,"VariableValue",empty)
            nVarNumber = create_xml_subelement_with_list(VariableValue,"nVarNumber",Elements)
            nVarNumber.text = str(3)
            nVarValue = create_xml_subelement_with_list(VariableValue,"nVarValue",Elements)
            nVarValue.text = str(roundedFracComp1)
            nVarDigits = create_xml_subelement_with_list(VariableValue,"nVarDigits",Elements)
            nVarDigits.text = getNumberOfDigits(str(roundedFracComp1))

            #comp2
            VariableValue = create_xml_subelement_with_list(NumValues,"VariableValue",empty)
            nVarNumber = create_xml_subelement_with_list(VariableValue,"nVarNumber",Elements)
            #first mole fraction (water) has varNumber 2
            nVarNumber.text = str(4)
            nVarValue = create_xml_subelement_with_list(VariableValue,"nVarValue",Elements)
            nVarValue.text = str(roundedFracComp2)
            nVarDigits = create_xml_subelement_with_list(VariableValue,"nVarDigits",Elements)
            nVarDigits.text = getNumberOfDigits(str(roundedFracComp2))
                
        #once per datapoint add property value
        PropertyValue = create_xml_subelement_with_list(NumValues,"PropertyValue",empty)
        nPropNumber = create_xml_subelement_with_list(PropertyValue,"nPropNumber",Elements)
        nPropNumber.text = str(1)
        nPropValue = create_xml_subelement_with_list(PropertyValue,"nPropValue",Elements)
        propertyInPaS = str(round((float(cmldata[i][2])/1000), 12))
        nPropValue.text = propertyInPaS

        nPropDigits = create_xml_subelement_with_list(PropertyValue,"nPropDigits",Elements)
        nPropDigits.text = getNumberOfDigits(propertyInPaS)
        CombinedUncertainty = create_xml_subelement_with_list(PropertyValue,"CombinedUncertainty",empty)
        nCombUncertAssessNum = create_xml_subelement_with_list(CombinedUncertainty,"nCombUncertAssessNum",Elements)
        nCombUncertAssessNum.text = str(1)
        nCombExpandUncertValue = create_xml_subelement_with_list(CombinedUncertainty,"nCombExpandUncertValue",Elements)
        if str(cmldata[i][3]) != "NG":
            propertyErrorRoundedinPaS = str(round((float(cmldata[i][3])/1000), 12))
            nCombExpandUncertValue.text = propertyErrorRoundedinPaS
        else:
            nCombExpandUncertValue.text = "NG"

    return PureOrMixtureData

def create_thermoml(cmlfile,cmldata):
    #namespace stuff
    attr_qname = etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
    nsmap = {None: 'http://www.iupac.org/namespaces/ThermoML', 'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}

    
    DataReport = etree.Element("DataReport", {attr_qname: "http://www.iupac.org/namespaces/ThermoML ThermoML.xsd"}, nsmap=nsmap)
    docTitle = "Density, dynamic viscosity, and derived properties of binary mixtures of methanol or ethanol with water, ethyl acetate, and methyl acetate at T = (293.15, 298.15, and 303.15) K"
    docDOI = str(cmldata[0][0])
    docComponents = [[],[]]
    docAuthors = []
    docAuthors.append("Begona Gonzalez")
    docAuthors.append("Noelia Calvar")
    docAuthors.append("Elena Gomez")
    docAuthors.append("Angeles Dominiguez")

    #water
    #inchi
    docComponents[0].append("InChI=1S/H2O/h1H2")
    #inchiKey
    docComponents[0].append("XLYOFNOQVPJJNP-UHFFFAOYSA-N")
    #commonName
    docComponents[0].append("water")
    #Smiles
    docComponents[0].append("H20")

    #comp1 Urea
    #docComponents[2].append("InChI=1S/CH4N2O/c2-1(3)4/h(H4,2,3,4)")
    #docComponents[2].append("XSQUKJJJFZCRTK-UHFFFAOYSA-N")
    #docComponents[2].append("urea")
    #docComponents[2].append("C(=O)(N)N")
    
    #comp 1 N,Ndietylethanol ammonim chlorid
    #docComponents[1].append("InChI=1S/C6H16NO.ClH/c1-4-6(3,5-2)8-7;/h4-5H2,1-3,7H3;1H/q+1;/p-1")
    #docComponents[1].append("NIYUVINFVZDPMK-UHFFFAOYSA-M")
    #docComponents[1].append("N,N-Diethylethanolammonium chloride")
    #docComponents[1].append("(C2H5)2NCH2CH2OHHCl")
    

    #comp  ethylene glycol
    #docComponents[1].append("InChI=1S/C2H6O2/c3-1-2-4/h3-4H,1-2H2")
    #docComponents[1].append("LYCAIKOWRPUZTN-UHFFFAOYSA-N")
    #docComponents[1].append("ethylene glycol")
    #docComponents[1].append("C(CO)O")
    
    #comp1 ChCL
    #inchi
    #docComponents[1].append("InChI=1S/C5H14NO.ClH/c1-6(2,3)4-5-7;/h7H,4-5H2,1-3H3;1H/q+1;/p-1")
    #inchiKey
    #docComponents[1].append("SGMZJAMFUVOLNK-UHFFFAOYSA-M")
    ##commonName
    #docComponents[1].append("choline choloride")
    #Smiles
    #docComponents[1].append("C[N+](C)(C)CCO.[Cl-]")

    #comp glycerol
    #inchi
    #docComponents[2].append("InChI=1S/C3H8O3/c4-1-3(6)2-5/h3-6H,1-2H2")
    #inchiKey
    #docComponents[2].append("PEDCQBHIVMGVHV-UHFFFAOYSA-N")
    #commonName
    #docComponents[2].append("glycerol")
    #Smiles
    #docComponents[2].append("C(C(CO)O)O")

    #comp methanol
    #inchi
    docComponents[1].append("InChI=1S/CH4O/c1-2/h2H,1H3")
    #inchiKey
    docComponents[1].append("OKKJLVBELUTLKV-UHFFFAOYSA-N")
    #commonName
    docComponents[1].append("methanol")
    #Smiles
    docComponents[1].append("CO")

    version_info = create_version_info(DataReport)
    citation = create_citation(docTitle, docDOI, DataReport, docAuthors)
    all_compounds = create_multipleCompound(docComponents, DataReport)
    all_datapoints = create_data_entry(cmldata, docComponents, DataReport)
    
    final_name = cmlfile + ".xml"
    convertedString = etree.tostring(DataReport, pretty_print=True, xml_declaration=True, encoding="utf-8")
    file = open(final_name, "wb")
    file.write(convertedString)
    file.close()

if __name__ == "__main__":
    
    tree = ET.parse('./cml/methanol_DOI2.xml')
    root = tree.getroot()

    cmldata = []

    for exp in root[0][0]:

        DOI = exp[0][0][0].text #this is just for consistency, no need to read in the DOI each time
        ID = exp[0][1][0].text #the datapoint number, starts with 1
        val_viscosity = exp[0][2][0].text #the solvent viscosity
        val_error = exp[0][3][0].text #the corresponsing error
        
        mol_DES = exp[1][0][0].text #the molar ratio of the DES
        mol_water = exp[1][1][0].text #the molar ratio of water
        T = exp[1][2][0].text #temperature in K
        
        cmldata.append([DOI,ID,val_viscosity,str(val_error),mol_DES,mol_water,T]) #eventually this could be a class
    
    create_thermoml("./thermoml/methanol_DOI2__",cmldata)