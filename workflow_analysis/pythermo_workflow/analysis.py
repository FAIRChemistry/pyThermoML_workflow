# @File          :   thermoml_analysis.py
# @Last modified :   2022/04/28 21:08:15
# @Author        :   Matthias Gueltig, Jan Range
# @Version       :   1.0
# @License       :   BSD-2-Clause License
# @Copyright (C) :   2022 Institute of Biochemistry and Technical Biochemistry Stuttgart

from pythermo.thermoml.core import DataReport
from pythermo.thermoml.tools.readTools import ThermoMLReader
from pythermo.thermoml.tools.writeTools import ThermoMLWriter
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
from pydantic import BaseModel

class Analysis(BaseModel):

    molarmass: dict[str, float] = {
        'water': 18.01528,
        'methanol': 32.04,
        'glycerol': 92.09382
    }
    
    R: float = 0.00831446261816324 

    def createDataFrame(self, dataReport:DataReport) -> pd.DataFrame:
        """creates pandas data Frame of current datareport object
        
        This method is used to simplificate analyzation.
        """
        for keyPom, pom in dataReport.pureOrMixtureData.items():
            
            df = pd.DataFrame()
            
            for key, prop in pom.properties.items():
                df[key] = ""

            for key, var in pom.variables.items():
                df[key] = ""
        
            for i, meas in enumerate(pom.measurements.values()):
                datarow = []
                for elem in df.columns:
                    if elem.startswith("p"):
                        datarow.append(meas.properties[elem].value)
                    elif elem.startswith("v"):
                        datarow.append(meas.variables[elem].value)
                df.loc[i] = datarow
            
            df["method"] = pom.properties["p1"].method

        for propID, prop in pom.properties.items():
            if "Self diffusion coefficient" == prop.propName or "Tracer diffusion coefficient" == prop.propName:
                nameNew = f"Sdiff{prop.compoundID}"
            else:
                nameNew = prop.propName
            df = df.rename(columns={propID: nameNew})

        for varID, var in pom.variables.items():
            if "Mole fraction" == var.varName:
                nameNew = f"Mf{var.compoundID}"
            else:
                nameNew = var.varName
            df = df.rename(columns={varID: nameNew})
            
        return df
    
    def calcMolarVolumeCompWat(self, dataReport: DataReport, pomID: str, compound:str) -> pd.DataFrame:
        """calculates molar volume for each density measurement of compound water mixture
        
        returns datframe with new column ln(V)
        """
        # density in [kg/m^3]

        df = self.createDataFrame(dataReport=dataReport)
        pom = dataReport.pureOrMixtureData[pomID]
        
        molarVolumePure = list()

        for index, row in df.iterrows():
            # molar mass in [g/mole]
            if row['Mfcw'] == 1.0:
                molarVolumePure.append(self.molarmass['water']*0.001/row['Mass density'])
            elif row['Mfcc'] == 1.0:
                molarVolumePure.append(self.molarmass[f'{compound}']*0.001/row['Mass density'])
            else:
                molarVolumePure.append(None)
        df['molarVolumePure'] = molarVolumePure
        # molarVolumePure in [m^3/mole]

        molarVolumeReal = list()
        molarVolumeIdeal = list()
        lnMolarVolumeReal = list()
        for index, row in df.iterrows():
            volReal = ((row['Mfcw'])*self.molarmass['water']*0.001 + (1-(row['Mfcw']))*self.molarmass[f'{compound}']*0.001)/row['Mass density']
            molarVolumeReal.append(volReal)
            lnMolarVolumeReal.append(np.log(volReal))

            vwater = df.loc[(df['Temperature'] == row['Temperature']) & (df['Mfcw'] == 1.0)]['molarVolumePure'].values[0]
            vcomp = df.loc[(df['Temperature'] == row['Temperature']) & (df['Mfcc'] == 1.0)]['molarVolumePure'].values[0]
            volIdeal = row['Mfcw']*vwater + row['Mfcc']*vcomp
            molarVolumeIdeal.append(volIdeal)
        
        df = df.drop(labels="molarVolumePure", axis=1)
        # Vreal in [m^3/mole]
        # ln(Vreal) in [m^3/mole]
        # Videal in [m^3/mole]
        df['Vreal'] = molarVolumeReal
        df['ln(Vreal)'] = lnMolarVolumeReal
        df['Videal'] = molarVolumeIdeal
        
        # excess volume
        volumemixexcess = list()
        for index, rows in df.iterrows():
            volumemixexcess.append(rows['Vreal'] - rows['Videal'])

        # excess volume in [m^3/mole]
        df['Vexcess'] = volumemixexcess
        return df
        
    
    def arrheniusDens(self, df):
        # list with dataframes that have same glycerol/water mole fractions
        dataframes = list()
        moleFractions = df["Mfcw"].unique()
        for moleFrac in moleFractions:
            dfSameFrac = df[df['Mfcw']==moleFrac]
            dataframes.append(dfSameFrac)

        # real
        dataLinReg = list()
        for dfSameFrac in dataframes:
            
            x = dfSameFrac[['Temperature']]
            y = dfSameFrac[['ln(Vreal)']]
        
            regressor = LinearRegression()
            regressor.fit(x,y)
            
            dfSameFrac = dfSameFrac.drop(['Temperature', 'Mass density', 'ln(Vreal)'], axis=1)
            dfSameFrac = dfSameFrac.drop_duplicates(subset=['Mfcw'])
            
            dfSameFrac['gammareal'] = regressor.coef_
            dfSameFrac['ln(V0)'] = regressor.intercept_
            dfSameFrac['Tempmin'] = x['Temperature'].min()
            dfSameFrac['Tempmax'] = x['Temperature'].max()

            dataLinReg.append(dfSameFrac)
        
        result = pd.concat(dataLinReg)

        # ideal
        gammawater = result.loc[result['Mfcw'] == 1.0]['gammareal'].values[0]
        gammacomp = result.loc[result['Mfcc'] == 1.0]['gammareal'].values[0]
        v0water = result.loc[result['Mfcw'] == 1.0]['ln(V0)'].values[0]
        v0comp = result.loc[result[f'Mfcc'] == 1.0]['ln(V0)'].values[0]

        
        gammamixideal = list()
        for dfsame in dataframes:
            vmix0 = dfsame['Mfcw'].values[0]*v0water + dfsame[f'Mfcc'].values[0]*v0comp
            zaehler = dfsame['Mfcw'].values[0]*v0water*gammawater+dfsame['Mfcc'].values[0]*v0comp*gammacomp
            gammamixideal.append(zaehler/vmix0)
        result['gammaideal'] = gammamixideal
        
        # excess values
        gammaexcess = list()
        for index, rows in result.iterrows():
            gammaexcess.append(rows['gammareal'] - rows['gammaideal'])
        result['gammaexcess'] = gammaexcess
    
        return result
    
    def arrheniusVisc(self, df):
        modViscs = list()
        modTemps = list()
        modlnviscs = list()
        for index, row in df.iterrows():
            modTemps.append(1/(self.R*row['Temperature']))
            modViscs.append(row['Viscosity']*1000)

            # change unit of viscosity in cP
            modlnviscs.append(np.log(row['Viscosity']*1000))
        
        df['Viscosity'] = modViscs
        df['1/RT'] = modTemps
        df['ln(eta)'] = modlnviscs
        
        # list with dataframes that have same compound/water mole fractions
        dataframes = list()
        moleFractions = df["Mfcw"].unique()

        for moleFrac in moleFractions:
            dfSameFrac = df[df['Mfcw'] == moleFrac]
            dataframes.append(dfSameFrac)
        
        # real
        dataLinReg = list()
        for dfSameFrac in dataframes:
            x = dfSameFrac[['1/RT']]
            y = dfSameFrac[['ln(eta)']]

            regressor = LinearRegression()
            regressor.fit(x,y)

            dfSameFrac = dfSameFrac.drop(['Temperature', '1/RT', 'ln(eta)', 'Viscosity'], axis=1)
            dfSameFrac = dfSameFrac.drop_duplicates(subset=['Mfcw'])

            dfSameFrac['Eetareal'] = regressor.coef_
            dfSameFrac['ln(eta0)'] = regressor.intercept_
            dfSameFrac['tempmin'] = x['1/RT'].min()
            dfSameFrac['tempmax'] = x['1/RT'].max()

            dataLinReg.append(dfSameFrac)
        result = pd.concat(dataLinReg)
        
        # ideal
        eetawater = result.loc[result['Mfcw'] == 1.0]['Eetareal'].values[0]
        eetacomp = result.loc[result[f'Mfcc'] == 1.0]['Eetareal'].values[0]
        lneta0water = result.loc[result['Mfcw'] == 1.0]['ln(eta0)'].values[0]
        lneta0comp = result.loc[result['Mfcc'] == 1.0]['ln(eta0)'].values[0]

        eetamixideal = list()
        lneta0mixideal = list()
        for dfsame in dataframes:
            eetamix = dfsame['Mfcw'].values[0]*eetawater + dfsame[f'Mfcc'].values[0]*eetacomp
            lneta0mix = dfsame['Mfcw'].values[0]*lneta0water + dfsame['Mfcc'].values[0]*lneta0comp
            eetamixideal.append(eetamix)
            lneta0mixideal.append(lneta0mix)
        result['Eetaideal'] = eetamixideal

        # eta excess
        eetamixexcess = list()
        for index, rows in result.iterrows():
            eetamixexcess.append(rows['Eetareal'] - rows['Eetaideal'])
        result['Eetaexcess'] = eetamixexcess

        return result