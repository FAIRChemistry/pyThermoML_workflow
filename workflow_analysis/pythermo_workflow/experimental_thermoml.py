import pandas as pd
from pythermo.thermoml.core import PureOrMixtureData, DataReport, Compound, DataPoint

from pythermo.thermoml.vars.componentcomposition import ComponentCompositionBase
from pythermo.thermoml.vars.temperature import TemperatureBase
from pythermo.thermoml.props.transportproperties import TransportProperty

from pythermo.thermoml.props.volumetricproperties import VolumetricProperty
from pythermo.thermoml.tools.writeTools import ThermoMLWriter
from pythermo.thermoml.tools.readTools import ThermoMLReader

from pydantic import BaseModel

class ExperimentThermoML(BaseModel):
    folder_txt_files: str
    folder_thermoML_files: str

    def readDensGlyc(self, txt_file:str):
        df_dens_glyc = pd.read_csv(f"{self.folder_txt_files}{txt_file}", sep=" ", index_col=False)
        df_dens_glyc = self.__changeValue(df_dens_glyc, value="dens")
        df_dens_glyc = self.__changeToWaterXw(df_dens_glyc)

        title="Volumetric properties of glycerol + water mixtures at several temperatures and correlation with the Jouyban-Acree model"

        authors = {
            "author1": "Diana M. Cristancho",
            "author2": "Daniel R. Delgado",
            "author3": "Fleming Martinez",
            "author4": "Mohammed A. Abolghassemi Fakhree",
            "author5": "Abolghasem Jouyban"
        }

        comp1 = Compound(ID="cw", standardInchI="InChI=1S/H2O/h1H2", standardInchIKey="XLYOFNOQVPJJNP-UHFFFAOYSA-N", smiles="O", commonName="water")
        comp2 = Compound(ID="cc", standardInchI="InChI=1S/C3H8O3/c4-1-3(6)2-5/h3-6H,1-2H2", standardInchIKey="PEDCQBHIVMGVHV-UHFFFAOYSA-N", smiles="C(C(CO)O)O", commonName="glycerol")

        return self.expDFToThermoML(df=df_dens_glyc, authors=authors, title=title, water=comp1, second_compound=comp2, property1="Mass Density")
        
    def readDensMeth(self, txt_file:str):
        df_dens_meth = pd.read_csv(f"{self.folder_txt_files}{txt_file}", sep=" ", index_col=False)
        df_dens_meth = self.__changeValue(df_dens_meth, value="dens")
        df_dens_meth = self.__normalizeMoleFraction(df_dens_meth)
        df_dens_meth = self.__changeToWaterXw(df_dens_meth)

        authors = {
        "author1": "S. Z. Mikhail",
        "author2": "W. R. Kimel"
        }

        title="Densities and Viscosities of Methanol-Water Mixtures."
        DOI = "10.1021/je60011a015"

        comp1 = Compound(ID="cw", standardInchI="InChI=1S/H2O/h1H2", standardInchIKey="XLYOFNOQVPJJNP-UHFFFAOYSA-N", smiles="O", commonName="water")
        comp2 = Compound(ID="cc", standardInchI="InChI=1S/CH4O/c1-2/h2H,1H3", standardInchIKey="OKKJLVBELUTLKV-UHFFFAOYSA-N", smiles="CO", commonName="methanol")


        return self.expDFToThermoML(df=df_dens_meth, authors=authors, title=title, DOI=DOI, water=comp1, second_compound=comp2, property1="Mass Density")

    def readSDiffGlyc(self, txt_file:str):
        df_sdiff_glyc = pd.read_csv(f"{self.folder_txt_files}{txt_file}", sep=" ", index_col=False)
        df_sdiff_glyc = self.__changeValue(df_sdiff_glyc, value="sdiff")
        df_sdiff_glyc = self.__changeToWaterXw(df_sdiff_glyc)


        authors = {
            "author1": "Geradino D'Errico",
            "author2": "Ornellla Ortona",
            "author3": "Fabio Capuano",
            "author4": "Vincenzo Vitagliano"
        }

        title="Diffusion Coefficients for the Binary System Glycerol + Water at 25 °C. A Velocity Correlation Study"
        DOI = "10.1021/je049917u"

        comp1 = Compound(ID="cw", standardInchI="InChI=1S/H2O/h1H2", standardInchIKey="XLYOFNOQVPJJNP-UHFFFAOYSA-N", smiles="O", commonName="water")
        comp2 = Compound(ID="cc", standardInchI="InChI=1S/C3H8O3/c4-1-3(6)2-5/h3-6H,1-2H2", standardInchIKey="PEDCQBHIVMGVHV-UHFFFAOYSA-N", smiles="C(C(CO)O)O", commonName="glycerol")
        
        return self.expDFToThermoML(df=df_sdiff_glyc, authors=authors, title=title, DOI=DOI, water=comp1, second_compound=comp2, property1="Self diffusion coefficient", property2="Self diffusion coefficient")

    def readSDiffMeth(self, txt_file1:str, txt_file2:str):
        df_sdiff_meth1 = pd.read_csv(f"{self.folder_txt_files}{txt_file1}", sep=" ", index_col=False)
        df_sdiff_meth2 = pd.read_csv(f"{self.folder_txt_files}{txt_file2}", sep=" ", index_col=False)
        df_sdiff_meth1 = self.__changeToWaterXw(df_sdiff_meth1)
        df_sdiff_meth2 = self.__changeToWaterXw(df_sdiff_meth2)
        df_sdiff_meth1 = self.__changeValue(df_sdiff_meth1, value="sdiff")
        df_sdiff_meth2 = self.__changeValue(df_sdiff_meth2, value="sdiff")
        authors = {
            "author1": "Z. J. Derlacki",
            "author2": "A. J. Easteal",
            "author3": "A. V. J. Edge",
            "author4": "L. A. Woolf"
        }

        title="Diffusion Coefficients of Methanol and Water and the Mutual Diffusion Coefficient in Methanol-Water Solutions at 278 and 298 K"
        DOI = "10.1021/j100270a039"

        comp1 = Compound(ID="cw", standardInchI="InChI=1S/H2O/h1H2", standardInchIKey="XLYOFNOQVPJJNP-UHFFFAOYSA-N", smiles="O", commonName="water")
        comp2 = Compound(ID="cc", standardInchI="InChI=1S/CH4O/c1-2/h2H,1H3", standardInchIKey="OKKJLVBELUTLKV-UHFFFAOYSA-N", smiles="CO", commonName="methanol")

        return self.expDFToThermoML(df=df_sdiff_meth1, authors=authors, title=title, DOI=DOI, water=comp1, second_compound=comp2, property1="Tracer diffusion coefficient", property2="Tracer diffusion coefficient", df2=df_sdiff_meth2)
    
    def readViscGlyc(self, txt_file: str):
        df_visc_glyc = pd.read_csv(f"{self.folder_txt_files}{txt_file}", sep=" ", index_col=False)
        df_visc_glyc = self.__changeValue(df_visc_glyc, value="visc")
        df_visc_glyc = self.__changeToWaterXw(df_visc_glyc)

        title = "Viscosity of Glycerol and Its Aqueous Solutions"
        DOI = "10.1021/ie50501a040"
    
        authors = {
            "1": "J. B. Segur",
            "2": "Helen E. Oberstar",
        }

        comp1 = Compound(ID="cw", standardInchI="InChI=1S/H2O/h1H2", standardInchIKey="XLYOFNOQVPJJNP-UHFFFAOYSA-N", smiles="O", commonName="water")
        comp2 = Compound(ID="cc", standardInchI="InChI=1S/C3H8O3/c4-1-3(6)2-5/h3-6H,1-2H2", standardInchIKey="PEDCQBHIVMGVHV-UHFFFAOYSA-N", smiles="C(C(CO)O)O", commonName="glycerol")

        return self.expDFToThermoML(df=df_visc_glyc, authors=authors, title=title, DOI=DOI, water=comp1, second_compound=comp2, property1="Viscosity")

    def expDFToThermoML(self, df:pd.DataFrame, authors:dict[str,str], title:str, water:Compound, second_compound:Compound, property1:str, DOI:str=None, property2:str=None, df2:pd.DataFrame=None):
        authors = authors

        data_set = DataReport(title=title, DOI=DOI, authors = authors)
        wat_ID = data_set.addCompound(water)
        second_comp_ID = data_set.addCompound(second_compound)
        comps = [wat_ID, second_comp_ID]
        experiment = PureOrMixtureData(ID="pom1", compiler="Matthias Gueltig", comps = comps)

        temp = TemperatureBase.temperature(ID="v1")
        frac1 = ComponentCompositionBase.moleFraction('v2', wat_ID)
        frac2 = ComponentCompositionBase.moleFraction('v3', second_comp_ID)
        
        tempID = experiment.addVariable(temp)
        frac1ID = experiment.addVariable(frac1)
        frac2ID = experiment.addVariable(frac2)

        if property1 == "Mass Density" and property2 == None:
            dens = VolumetricProperty.massDensity(ID="p1", method="experiment")
            propID = experiment.addProperty(dens)
        elif property1 == "Viscosity" and property2 == None:
            visc = TransportProperty.viscosity(ID="p1", method="experiment")
            propID = experiment.addProperty(visc)
        elif property1 == "Self diffusion coefficient" and property2 == "Self diffusion coefficient":
            sdiffWat = TransportProperty.selfDiffusionCoefficient(ID="p1", method="experiment", compoundID=wat_ID)
            sdiffComp = TransportProperty.selfDiffusionCoefficient(ID="p2", method="experiment", compoundID=second_comp_ID)
            prop1ID = experiment.addProperty(sdiffWat)
            prop2ID = experiment.addProperty(sdiffComp)
            propID = None
        elif property1 == "Tracer diffusion coefficient" and property2 == "Tracer diffusion coefficient":
            sdiffWat = TransportProperty.tracerDiffusionCoefficient(ID="p1", method="experiment", compoundID=wat_ID)
            sdiffComp = TransportProperty.tracerDiffusionCoefficient(ID="p2", method="experiment", compoundID=second_comp_ID)
            prop1ID = experiment.addProperty(sdiffWat)
            prop2ID = experiment.addProperty(sdiffComp)
            propID = None
        else:
            return "Please define an input property name: Mass Density, Viscosity or Self/Tracer diffusion coefficient"
        
        if propID:
            rows = df.shape[0]
            temps = list(df.columns)
            temps.pop(0)

            measCount = 0
            for temp in temps:
                for i in range(rows):
                    measurementID = f"meas{measCount}"
                    propDataPoint = DataPoint(measurementID=measurementID, value=df.at[i,temp], propID =propID)
                    tempDataPoint = DataPoint(measurementID=measurementID, value=temp, varID = tempID)
                    frac1DataPoint = DataPoint(measurementID=measurementID, value=df.at[i, 'xw'], varID = frac1ID)
                    frac2DataPoint = DataPoint(measurementID=measurementID, value=1-df.at[i, 'xw'], varID = frac2ID)
                    measCount = measCount + 1
                    datapoints = [propDataPoint, tempDataPoint, frac1DataPoint, frac2DataPoint]
                    experiment.addMeasurement(dataPoints=datapoints)

            data_set.addPureOrMixtureData(experiment)
            return data_set
        
        elif prop1ID and prop2ID:
            # glycerol case
            if df2 is None:
                rows = df.shape[0]
                for i in range(rows):
                    datapoints = self.__integrateSDiffs(df=df, temp=298.15, dfRowIndex=i, measIndex=i, prop1ID=prop1ID, prop2ID=prop2ID, tempID=tempID, frac1ID=frac1ID, frac2ID=frac2ID)
                    experiment.addMeasurement(dataPoints=datapoints)
                data_set.addPureOrMixtureData(experiment) 
            else:
                rows1 = df.shape[0]
                rows2 = df2.shape[0]
                for i in range(rows1):
                    
                    # Note: temperatures are hard coded because not stored in read .txt files
                    datapoints = self.__integrateSDiffs(df=df, temp=278.15, dfRowIndex=i, measIndex=i, prop1ID=prop1ID, prop2ID=prop2ID, tempID=tempID, frac1ID=frac1ID, frac2ID=frac2ID)
                    experiment.addMeasurement(dataPoints=datapoints)
                for j in range(rows2):
                    # Note: temperatures are hard coded because not stored in read .txt files
                    datapoints = self.__integrateSDiffs(df=df2, temp=298.15, dfRowIndex=j, measIndex=i+j+1, prop1ID=prop1ID, prop2ID=prop2ID, tempID=tempID, frac1ID=frac1ID, frac2ID=frac2ID)
                    experiment.addMeasurement(dataPoints=datapoints)
                
                print(experiment.to_string())
                data_set.addPureOrMixtureData(experiment)
                
            return data_set
    
    def __changeValue(self, df:pd.DataFrame, value:str) -> pd.DataFrame:
        temps = list(df.columns)
        temps.pop(0)
        for temp in temps:
            for i in df.index:
                if value == "dens":
                    df = self.__changeDensUnit(df, temp, i)
                elif value == "visc":
                    df = self.__changeViscUnit(df, temp, i)
                elif value == "sdiff":
                    df = self.__changeSDiffUnit(df, temp, i) 
        return df
    
    def __changeSDiffUnit(self, df:pd.DataFrame, temp:float, i:int) -> pd.DataFrame:
        """changes self-diffusion coefficient unit from 10^9 m^2/s to m^2/s"""
        sdiff = df.at[i, temp]*10**(-9)
        df.at[i,temp] = sdiff
        return df

    def __changeViscUnit(self, df:pd.DataFrame, temp:float, i:int) -> pd.DataFrame:
        """changes viscosity unit from cP to Pa*s"""
        visc = df.at[i, temp]*0.001
        df.at[i, temp] = visc
        return df
    
    def __changeDensUnit(self, df:pd.DataFrame, temp:float, i:int) -> pd.DataFrame:
        """changes density unit from g/cm^3 to kg/m^3"""
        dens = df.at[i, temp]*1000
        df.at[i, temp] = dens
        return df

    def __changeToWaterXw(self, df:pd.DataFrame) -> pd.DataFrame:
        """converts component mole fraction of a .txt file to water mole fraction"""
        for i in df.index:
            xw = 1-df.at[i, "xc"]
            df.at[i, "xc"] = xw
        df.rename(columns={'xc':'xw'}, inplace=True)
        return df

    def __normalizeMoleFraction(self, df:pd.DataFrame) -> pd.DataFrame:
        """converts prozentual mole fraction of .txt to decimal mole fraction"""
        for i in df.index:
            mf = df.at[i, 'xc']/100
            df.at[i, 'xc'] = mf
        return df

    def __integrateSDiffs(self, df: pd.DataFrame, temp:float, dfRowIndex:str, measIndex:float, prop1ID:str, prop2ID:str, tempID:str, frac1ID:str, frac2ID:str) -> list[DataPoint]:
        measurementID=f"meas{measIndex}"

        sdiff1DataPoint = DataPoint(measurementID=measurementID, value=df.at[dfRowIndex, 'Dw'], propID = prop1ID)
        sdiff2DataPoint = DataPoint(measurementID=measurementID, value=df.at[dfRowIndex, 'Dc'], propID = prop2ID)
        tempDataPoint = DataPoint(measurementID=measurementID, value=temp, varID = tempID)
        frac1DataPoint = DataPoint(measurementID=measurementID, value=df.at[dfRowIndex, 'xw'], varID = frac1ID)
        frac2DataPoint = DataPoint(measurementID=measurementID, value=1-df.at[dfRowIndex, 'xw'], varID = frac2ID)
        
        return [sdiff1DataPoint, sdiff2DataPoint, tempDataPoint, frac1DataPoint, frac2DataPoint]

    