# @File          :   access_mixturemm.py
# @Last modified :   2022/04/24 15:05:36
# @Author        :   Matthias Gueltig, Jan Range
# @Version       :   1.0
# @License       :   BSD-2-Clause License
# @Copyright (C) :   2022 Institute of Biochemistry and Technical Biochemistry Stuttgart

from pydantic import BaseModel
from pythermo.thermoml.core import DataReport, Compound, PureOrMixtureData, DataPoint
from pythermo.thermoml.vars.componentcomposition import ComponentCompositionBase
from pythermo.thermoml.vars.temperature import TemperatureBase
from pythermo.thermoml.props.volumetricproperties import VolumetricProperty
from pythermo.thermoml.props.transportproperties import TransportProperty
import json
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt



class MixtureMMThermoML(BaseModel):
    """Class providing conversion tools for the JSON files of MixturemMM workflow of Benjamin Schmitz to 
        pyThermoML data report objects. Needed for workflow described in the paper:

        "Analysis of simulated and experimental thermophysical properties of aqueous mixtures: data integration by ThermoML"

    Note:
        Only use for aqueous water mixtures. 
    Args:
        BaseModel (_type_): _description_

    Returns:
        _type_: _description_
    """
    folder_mixtureMM_files: str
    folder_thermoML_files: str

    def read_density(self, json_file: str) -> DataReport:

        # load density data
        json_data = json.load(open(f"{self.folder_mixtureMM_files}{json_file}"))
        
        # create data report
        title = "Integration of simulated and experimentally determined thermophysical properties of aqueous mixtures by ThermoML"
        authors = {
            "author1": "Matthias Gueltig",
            "author2": "Jan Range",
            "author3": "Benjamin Schmitz",
            "author4": "Juergen Pleiss"
        } 
        data_set = DataReport(title=title, authors=authors)
        data_set = self.__addCompounds(json_data=json_data, data_set=data_set)
        data_set = self.__addExperiment(json_data=json_data, data_set=data_set)
        
        return data_set

    def __addCompounds(self, json_data: dict, data_set: DataReport) -> DataReport:
        # Note: The first compound should be water
        
        for molecule_name, molecule_infos in json_data["molecules"].items():
            if molecule_name=="Water":
                comp1 = Compound(ID=f"cw", standardInchI=molecule_infos["inchi_key"], smiles=molecule_infos["smiles_code"], commonName=molecule_name)
                data_set.addCompound(comp1)
            elif molecule_name=="Methanol" or molecule_name=="Glycerol":
                comp1 = Compound(ID=f"cc", standardInchI=molecule_infos["inchi_key"], smiles=molecule_infos["smiles_code"], commonName=molecule_name)
                data_set.addCompound(comp1)
        return data_set

    def __addExperiment(self, json_data:dict, data_set: DataReport) -> DataReport:
        comps = data_set.getCompoundIDs()

        experiment = PureOrMixtureData(ID="pom1", compiler="Matthias Gueltig", comps=comps)

        experiment.addVariable(TemperatureBase.temperature(ID="v1"))
        experiment.addVariable(ComponentCompositionBase.moleFraction('v2', comps[0]))
        experiment.addVariable(ComponentCompositionBase.moleFraction('v3', comps[1]))
        experiment.addProperty(VolumetricProperty.massDensity("p1", method="simulation"))
        
        for index, meas in enumerate(json_data["averaged densities"]):
            data_points = self.__getDataPoints(index, experiment, meas)
            experiment.addMeasurement(dataPoints=data_points)
        
        data_set.addPureOrMixtureData(experiment)
        return data_set

    def __getDataPoints(self, index: str, experiment: PureOrMixtureData, meas:dict) -> list[DataPoint]:
        measurementID = f"meas{index}"
        tempDataPoint = DataPoint(measurementID=measurementID, value=meas["temperature"], varID = "v1")
        frac1DataPoint = DataPoint(measurementID=measurementID, value=meas["chi_water"], varID = "v2")
        frac2DataPoint = DataPoint(measurementID=measurementID, value=1-meas["chi_water"], varID = "v3")
        densDataPoint = DataPoint(measurementID=measurementID, value=meas["average_density"]*1000, uncertainty=meas["stdev_density"]*1000, propID = "p1")
        
        return [tempDataPoint, frac1DataPoint, frac2DataPoint, densDataPoint]
    
    def read_transport(self, json_file:str):
        """reads in self diffusion coefficient .json output of MixtureMM workflow

        Args:
            json_file (str): Output file of MixtureMM workflow
        """

        # load self-diffusion data
        json_data = json.load(open(f"{self.folder_mixtureMM_files}{json_file}"))
        df = self.extract_sdiff_to_dataframe(json_data=json_data)
        result_df = self.regression(df)
        self.vis_regression(df, result_df, 298.15, 0.5)
    
    def create_data_report(self, result_df:pd.DataFrame) -> DataReport:
        """integrates generated data frame into DataReport object

        Args:
            result_df (pd.DataFrame): pandas dataframe with self-diffusion coefficient data and viscosity data

        Returns:
            DataReport: DataReport object representation of pandas dataframe. Due to less replica number viscosities won't be integrated
        """
        title = "Integration of simulated and experimentally determined thermophysical properties of aqueous mixtures by ThermoML"
        authors = {
            "author1": "Matthias Gueltig",
            "author2": "Jan Range",
            "author3": "Benjamin Schmitz",
            "author4": "Juergen Pleiss"
        } 

        dataReport = DataReport(title=title, authors=authors)
        comp1 = Compound(ID="cw", standardInchI="InChI=1S/H2O/h1H2", standardInchIKey="XLYOFNOQVPJJNP-UHFFFAOYSA-N", smiles="O", commonName="water")
        comp2 = Compound(ID="cc", standardInchI="InChI=1S/CH4O/c1-2/h2H,1H3", standardInchIKey="OKKJLVBELUTLKV-UHFFFAOYSA-N", smiles="CO", commonName="methanol")

        comp1ID = dataReport.addCompound(comp1)
        comp2ID = dataReport.addCompound(comp2)

        comps = [comp1ID, comp2ID]

        experiment = PureOrMixtureData(ID="pom1", compiler="Matthias Gueltig", comps=comps)
            
        temp = TemperatureBase.temperature(ID="v1")
        frac1 = ComponentCompositionBase.moleFraction('v2', comp1ID)
        frac2 = ComponentCompositionBase.moleFraction('v3', comp2ID)
        sdiffWat = TransportProperty.selfDiffusionCoefficient(ID="p1", method="simulation", compoundID=comp1ID)
        sdiffMet = TransportProperty.selfDiffusionCoefficient(ID="p2", method="simulation", compoundID=comp2ID)
        #visc = TransportProperty.viscosity(ID = "p3", method="simulation")

        sdiffWatID = experiment.addProperty(sdiffWat)
        sdiffMetID = experiment.addProperty(sdiffMet)
        #viscID = experiment.addProperty(visc)

        tempID = experiment.addVariable(temp)
        frac1ID = experiment.addVariable(frac1)
        frac2ID = experiment.addVariable(frac2)

        for counter, (index, rows) in enumerate(result_df.iterrows()):
            measurementID = f"meas{counter}"
            sdiffWatDataPoint = DataPoint(measurementID=measurementID, value=rows["sdiffWat"], propID = sdiffWatID)
            sdiffMetDataPoint = DataPoint(measurementID = measurementID, value=rows["sdiffComp"], propID = sdiffMetID)
            #viscDataPoint = DataPoint(measurementID=measurementID, value= rows["visc"], propID = viscID)
            tempDataPoint = DataPoint(measurementID=measurementID, value=rows["temp"], varID = tempID)
            frac1DataPoint = DataPoint(measurementID=measurementID, value=rows["xw"], varID = frac1ID)
            frac2DataPoint = DataPoint(measurementID=measurementID, value=1-rows["xw"], varID = frac2ID)
            datapoints = [sdiffWatDataPoint, sdiffMetDataPoint, tempDataPoint, frac1DataPoint, frac2DataPoint]
            experiment.addMeasurement(dataPoints=datapoints)

        dataReport.addPureOrMixtureData(experiment)
        return dataReport

    def vis_regression(self, df:pd.DataFrame, df_result: pd.DataFrame, temp: float, xw: float):
        
        dftest = df.loc[(df['temp'] == temp) & (df['moleFrac'] == xw)]
        dfWat = dftest[["moleFrac", "temp", "boxsize", "sdiffWat"]].dropna()
        dfComp = dftest[["moleFrac", "temp", "boxsize", "sdiffComp"]].dropna()


        dfComp["boxsize"] = 1/dfComp["boxsize"]
        dfWat["boxsize"] = 1/dfWat["boxsize"]

        
        fig, ax = plt.subplots(1,1)
        xwat = pd.to_numeric(dfWat['boxsize'])
        ywat = pd.to_numeric(dfWat['sdiffWat'])
        
        xcomp = pd.to_numeric(dfComp['boxsize'])
        ycomp = pd.to_numeric(dfComp['sdiffComp'])
        
        ax.scatter(xwat, ywat, label="sdiff water", color ="blue")
        ax.scatter(xcomp, ycomp, label=f"sdiff compound", color="orange")
        
        x = 1/1000 * np.arange(0,300)
        regressed_solution = df_result.loc[(df_result['temp'] == temp) & (df_result['xw'] == xw)]
        visc = regressed_solution.visc.values[0]
        sdiff1 = regressed_solution.sdiffWat.values[0]
        sdiff2 = regressed_solution.sdiffComp.values[0]
        
        # constants
        kb = 1.380649*10**(-23)
        xi = 2.837297
        slope = (-kb*temp*xi)/(10**(-9) *visc* np.pi*6)
        
        
        ax.plot(x,slope*x + sdiff1, label="regressed water", color="blue")
        ax.plot(x,slope*x + sdiff2, label=f"regressed compound", color="orange")
        ax.legend()
        ax.grid()
        ax.set_title(f"Analysis self-diffusion coefficients ($\chi_{{w}} = {xw}, T = {temp} K$)")
        ax.set_xlabel("inverse boxsize $\dfrac{{1}}{{L}}$ [$\dfrac{{1}}{{nm}}$]", fontsize=18)
        ax.set_ylabel(f"self-diffusion coefficient [$\dfrac{{m^2}}{{s}}$]", fontsize=18)
        fig.set_size_inches(13,10)
        fig.savefig(f"plots/regression_{temp}_{xw}.jpg")
        
    def regression(self, df: pd.DataFrame) -> pd.DataFrame:
        temps = df['temp'].unique()
        xws = df['moleFrac'].unique()
        result_data = list()

        # constants
        kb = 1.380649*10**(-23)
        xi = 2.837297

        for temp in temps:
            for xw in xws:
                dftest = df.loc[(df['temp'] == temp) & (df['moleFrac'] == xw)]
                
                # no conditioned regression needed
                if xw == 0.0 or xw == 1.0:
                    pd.options.mode.chained_assignment = None
                    dftest["boxsize"] = 1/dftest["boxsize"]
                    inversBoxSize = dftest[["boxsize"]]
                    if xw == 0.0:
                        sdiff = dftest[["sdiffComp"]]
                    elif xw == 1.0:
                        sdiff = dftest[["sdiffWat"]]
                    reg = LinearRegression()
                    reg.fit(inversBoxSize, sdiff)
                    visc = -kb*temp*xi/(reg.coef_[0][0]*np.pi*6*(10**(-9)))
                    if xw == 0.0:
                        result_data.append((xw, temp, None, reg.intercept_[0], visc))
                    elif xw == 1.0:
                        result_data.append((xw, temp, reg.intercept_[0], None, visc))

                # lines of the regression should have the same slope -> conditioned regression
                else:
                    dfWat = dftest[["moleFrac", "temp", "boxsize", "sdiffWat"]].dropna()
                    dfComp = dftest[["moleFrac", "temp", "boxsize", "sdiffComp"]].dropna()
                    dfComp["moleFrac"] = 1-dfComp["moleFrac"]
                    dfComp["boxsize"] = 1/dfComp["boxsize"]
                    dfWat["boxsize"] = 1/dfWat["boxsize"]
                    if dfWat.shape[0] != dfComp.shape[0]:
                        raise "please enter same number of comp and water diffs"
                    else:
                        A = np.zeros((3*dfWat.shape[0], 3))
                        b = np.zeros((3*dfWat.shape[0], 1))

                        for i in range(dfWat.shape[0]):
                            A[i,0] = 2
                            A[i,1] = 2*dfWat['boxsize'].values[i]
                            b[i,0] = 2*dfWat['sdiffWat'].values[i]
                        
                        for i in range(dfWat.shape[0]):
                            A[i+1*dfWat.shape[0],1] = 2*dfComp['boxsize'].values[i]
                            A[i+1*dfWat.shape[0],2] = 2
                            b[i+1+dfWat.shape[0],0] = 2*dfComp['sdiffComp'].values[i]
                        
                        for i in range(dfWat.shape[0]):
                            A[i+2*dfWat.shape[0],0] = 2* dfWat['boxsize'].values[i]
                            A[i+2*dfWat.shape[0],1] = 2*(dfWat['boxsize'].values[i])**2 + 2*(dfComp['boxsize'].values[i])**2
                            A[i+2*dfWat.shape[0],2] = 2 *dfComp['boxsize'].values[i]
                            b[i+2*dfWat.shape[0],0] = 2*dfWat['sdiffWat'].values[i]*dfWat['boxsize'].values[i] + 2*dfComp['sdiffComp'].values[i]*dfComp['boxsize'].values[i]


                    q, r = np.linalg.qr(A)
                    rightSide = np.dot(q.T, b)
                    sol = np.linalg.solve(r,rightSide)
                    visc = (-kb*temp*xi/(10**(-9)))/(sol[1][0]*np.pi*6)
                    result_data.append((xw, temp, sol[0][0], sol[2][0], visc))

        return pd.DataFrame(result_data, columns=["xw", "temp", "sdiffWat", "sdiffComp", "visc"])

    def extract_sdiff_to_dataframe(self, json_data:dict) -> pd.DataFrame:
        data = list()
        # volume in nm^3
        # sdiff in m^2/s
        for point in json_data["self diffusion coefficients"]:
            if point['abbreviation'] == "Me" or point["abbreviation"] == "Gl":
                data.append((point["chi_water"], point["temperature"], point["volume"]**(1/3), None, point["self_diffusion_coefficient"]))
            elif point['abbreviation'] == "HOH":
                data.append((point["chi_water"], point["temperature"], point["volume"]**(1/3), point["self_diffusion_coefficient"], None))
        
        return pd.DataFrame(data, columns = ["moleFrac", "temp", "boxsize", "sdiffWat", "sdiffComp"])
   