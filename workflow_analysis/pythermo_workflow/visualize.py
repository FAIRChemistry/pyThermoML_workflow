# @File          :   visualize.py
# @Last modified :   2022/04/28 22:08:37
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

import matplotlib.colors as mcol
import matplotlib.cm as cm
import math

class Visualize(BaseModel):
    folder_images: str

    def __visArr(self, xAx, yAx, ax, dfs, labelname):
        for df in dfs:
            df = df.sort_values(by=xAx, ascending=True)
            x = pd.to_numeric(df[xAx])
            y = pd.to_numeric(df[yAx])
            
            if df["method"].values[0] == "experiment":
                ax.scatter(x, y, alpha=1.0, label=f"{labelname} - experiment", marker='^',color="blue")
                ax.plot(x, y, linestyle="dotted", alpha=1.0, color="blue")
            elif df["method"].values[0] == "simulation":
                ax.scatter(x, y, alpha=1.0, label=f"{labelname} - simulation", marker="o",color="orange")
                ax.plot(x,y, color="orange")

    def plotDataFrame(self, dfs:pd.DataFrame, xAx:str, yAx:str, compound:str, log:bool = False):
        
        fig, ax = plt.subplots(1,1, figsize=(13,4), dpi=300)
        
        if yAx == "gammareal":
            labelname = "$\gamma_{{real}}$"
            self.__visArr(xAx,yAx,ax,dfs,labelname)
        elif yAx == "gammaexcess":
            labelname = "$\gamma_{{mix}}^{{excess}}$"
            self.__visArr(xAx,yAx,ax,dfs,labelname)
        elif yAx == "ln(eta0)":
            labelname = "$ln(\eta_{{0}})$"
            self.__visArr(xAx,yAx,ax,dfs,labelname)
        elif yAx == "Eetareal":
            labelname = "$E_{{\eta}}$"
            self.__visArr(xAx,yAx,ax,dfs,labelname)
        elif yAx == "Eetaexcess":
            labelname = "$E_{{\eta}}^{{excess}}$"
            self.__visArr(xAx,yAx,ax,dfs,labelname)


        else:
            cpick = self.__colorgradient(dfs)
            for df in dfs:
                df = df.sort_values(by=xAx, ascending=True)
                temperatures = np.unique(df[['Temperature']].values)
                
                for temp in temperatures:  
                    dfTemp = df.loc[df['Temperature'] == temp]
                    x = pd.to_numeric(dfTemp[xAx])
                    y = pd.to_numeric(dfTemp[yAx])

                    if df['method'].values[0] == 'experiment':

                        color = cpick.to_rgba(temp)
                        alpha = 1.0
                        ax.scatter(x,y, alpha=alpha, label=f"{temp} K - experiment", marker='^', color=color)
                        ax.plot(x, y, linestyle="dotted", c=color, alpha=alpha)
                        if log:
                            ax.set_yscale('log')
                            
                    elif df['method'].values[0] == 'simulation':

                        ax.scatter(x,y, alpha=1.0, label=f"{temp} K - simulation", marker="o", color=cpick.to_rgba(temp))
                        ax.plot(x,y, c=cpick.to_rgba(temp))
                        if log:
                            ax.set_yscale('log')
        labelfontsize = 18
        if xAx == "Mfcw":
            xAxmod = f"$\\chi_w$"
            ax.set_xlabel(xAxmod, fontsize=labelfontsize)
        else:
            ax.set_xlabel(xAx, fontsize=labelfontsize)
            xAxmod = xAx
        if yAx == "Vexcess":
            yAxmod = f"$V_{{mix}}^{{excess}}    [\dfrac{{m^3}}{{mole}}]$"
            ax.set_ylabel(yAxmod, fontsize=labelfontsize)
            propFileName = "vexcess"
        elif yAx == "Mass density":
            yAxmod = f"$\\rho_{{mix}}$ [$\dfrac{{kg}}{{m^3}}$]"
            ax.set_ylabel(yAxmod, fontsize=labelfontsize)
            propFileName = "dens"
        elif yAx == "gammaexcess":
            yAxmod = f"$\\gamma_{{mix}}^{{excess}}    [\dfrac{{1}}{{K}}]$"
            ax.set_ylabel(yAxmod, fontsize=labelfontsize)
            propFileName = yAx
        elif yAx == "Vreal":
            yAxmod = f"$V_{{mix}}^{{molar}}    [\dfrac{{m^3}}{{mole}}]$"
            ax.set_ylabel(yAxmod, fontsize=labelfontsize)
            propFileName = "molVol"
        elif yAx == "gammareal":
            yAxmod = f"$\gamma_{{real}}$  $[\\frac{{1}}{{K}}]$"
            propFileName=yAx
            ax.set_ylabel(yAxmod, fontsize=labelfontsize)
        elif yAx == "ln(eta0)":
            yAxmod = f"$ln(\eta_{{0}})$ $[cP]$"
            ax.set_ylabel(yAxmod, fontsize=labelfontsize)
            propFileName = "lneta0"
        elif yAx == "Eetareal":
            yAxmod = f"$E_{{\eta}}$ $[\\frac{{kJ}}{{mole}}]$"
            ax.set_ylabel(yAxmod, fontsize=labelfontsize)
            propFileName = "eetareal"
        elif yAx == "Eetaexcess":
            yAxmod = f"$E_{{\eta}}^{{excess}}$ $[\\frac{{kJ}}{{mole}}]$"
            ax.set_ylabel(yAxmod, fontsize=labelfontsize)
            propFileName = "eetaexcess"
        elif yAx == "Viscosity":
            yAxmod = f"$\eta$  $[Pa*s]$"
            ax.set_ylabel(yAxmod, fontsize=labelfontsize)
            yAxmod = "Viscosity"
            propFileName = "visc"
        elif yAx == "Sdiffcw":
            yAxmod = f"$D_{{inf}}    [\dfrac{{m^2}}{{s}}]$"
            ax.set_ylabel(yAxmod, fontsize=labelfontsize)
            propFileName="sdiffwater"
        elif yAx == "Sdiffcc":
            yAxmod = f"$D_{{inf}}    [\dfrac{{m^2}}{{s}}]$"
            ax.set_ylabel(yAxmod, fontsize=labelfontsize)
            propFileName=f"sdiff{compound}"
        else:
            yAxmod = yAx
            ax.set_ylabel(yAx, fontsize=labelfontsize)
            propFileName="unknown"
            
        ax.legend(loc="best", bbox_transform=fig.transFigure, fontsize=15)
        ax.grid()
        fig.set_size_inches(13,10)
        
        if yAx == "Sdiffcw":
            ax.set_title(f"{yAxmod} of water {compound} mixture - water", pad=25, fontsize=20)
        elif yAx == "Sdiffcc":
            ax.set_title(f"{yAxmod} of water {compound} mixture - {compound}", pad=25, fontsize=20)
        elif yAx == "Vexcess":
            ax.set_title(f"{yAxmod} of water {compound} mixture - molar excess volume", pad=25, fontsize=20)
        else:
            ax.set_title(f"{yAxmod} of aqueous {compound} mixture", pad=25, fontsize=20)
        
        if compound == "methanol":
            compFileName = "meth"
        elif compound == "glycerol":
            compFileName = "glyc"

        ax.tick_params(labelsize=18)
        if yAx == "ln(eta0)" or yAx == "Eetareal" or yAx == "Eetaexcess" or yAx == "Viscosity" or yAx == "Sdiffcw" or yAx == "Sdiffcc":
            if log:
                fig.savefig(f"{self.folder_images}transport/" + f"{propFileName}_{compFileName}_log.jpg", bbox_inches="tight", dpi=300)
            else:
                fig.savefig(f"{self.folder_images}transport/" + f"{propFileName}_{compFileName}.jpg", bbox_inches="tight", dpi=300)
        else:
            fig.savefig(f"{self.folder_images}densities/" + f"{propFileName}_{compFileName}.jpg", bbox_inches="tight", dpi=300)

    
    def plotArrheniusDens(self, df:pd.DataFrame, df_arrhenius:pd.DataFrame, compound:str):
        xws = df["Mfcw"].unique()
        fig, ax = plt.subplots(1,1)
        for xw in xws:
            # visualize points
            temps = df["Temperature"].unique()
            values = list()
            for temp in temps:
                values.append(df.loc[(df['Temperature'] == temp) & (df['Mfcw'] == xw)]['ln(Vreal)'].values[0])
            ax.scatter(temps, values, label=f"$ln(V_{{real}})$ at $\chi_w = {{{xw}}}$")
            
            # visualize lines
            x = np.arange(min(temps), max(temps)+1)
            ax.plot(x,df_arrhenius.loc[df_arrhenius["Mfcw"] == xw]["gammareal"].values[0]*x + df_arrhenius.loc[df_arrhenius["Mfcw"] == xw]["ln(V0)"].values[0])
        
        ax.tick_params(labelsize=18)
        ax.legend(loc="best")
        ax.grid()
        method = df["method"].unique()[0]    
        ax.set_title(f"Arrhenius analysis of aqueous {compound} mixture - {method}", pad=25, fontsize=20)
        ax.set_xlabel("Temperature [K]", fontsize=18)
        ax.set_ylabel(f"$ln(V_{{real}})$", fontsize=18)
        fig.set_size_inches(13,10)
        if compound == "methanol":
            compFileName = "meth"
        elif compound == "glycerol":
            compFileName = "glyc"
        if method == "simulation":
            method = "sim"
        elif method == "experiment":
            method = "exp"
        fig.savefig(f"{self.folder_images}densities/" + f"arrhenius_{method}_dens_{compFileName}.jpg")

    
    def plotArrheniuslnetaRT(self, df:pd.DataFrame, df_arrhenius:pd.DataFrame, compound:str):
        fig, ax = plt.subplots(1,1)

        for xw in df["Mfcw"].unique():
        
            temps = df["1/RT"].unique()
            values = list()
            for temp in temps:
                values.append(df.loc[(df['1/RT'] == temp) & (df['Mfcw'] == xw)]['ln(eta)'].values[0])
            ax.scatter(temps, values, label=f"$ln(\eta_{{real}})$ at $\chi_w = {{{xw}}}$")
            x = 1/10000 * np.arange(min(temps)*10000, max(temps)*10000, 0.001)
            ax.plot(x,df_arrhenius.loc[df_arrhenius["Mfcw"] == xw]["Eetareal"].values[0]*x + df_arrhenius.loc[df_arrhenius["Mfcw"] == xw]["ln(eta0)"].values[0])
        ax.tick_params(labelsize=18)
        ax.legend(loc="best")
        ax.grid()
        method = df["method"].unique()[0]    
        ax.set_title(f"Arrhenius of aqueous {compound} mixture - {method}", pad=25, fontsize=20)
        ax.set_xlabel("$\\frac{{1}}{{RT}}\:[\\frac{{mole}}{{KJ}}]$", fontsize=18)
        ax.set_ylabel(f"$ln(\eta)$  $[cP]$" , fontsize=18)
        fig.set_size_inches(13,10)
        if compound == "methanol":
            compFileName = "meth"
        elif compound == "glycerol":
            compFileName = "glyc"
        if method == "simulation":
            method = "sim"
        elif method == "experiment":
            method = "exp"
        fig.savefig(f"{self.folder_images}transport/" + f"arrhenius_{method}_visc_{compFileName}.jpg")


    def __colorgradient(self, dfs):
        dfmin = 5000000
        dfmax = 0
        for df in dfs:
            if df["Temperature"].min() < dfmin:
                dfmin = df["Temperature"].min()
            if df["Temperature"].max() > dfmax:
                dfmax = df["Temperature"].max()
        
        tim = range(math.floor(dfmin), math.ceil(dfmax))
        cm1 = mcol.LinearSegmentedColormap.from_list("ColorGradient",["b","r"])
        cnorm = mcol.Normalize(vmin=min(tim),vmax=max(tim))
        cpick = cm.ScalarMappable(norm=cnorm,cmap=cm1)
        cpick.set_array([])
        return cpick

