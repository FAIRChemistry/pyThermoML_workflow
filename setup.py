# @File          :   setup.py
# @Last modified :   2022/05/05 20:32:39
# @Author        :   Matthias Gueltig
# @Version       :   1.0
# @License       :   BSD-2-Clause License
# @Copyright (C) :   2022 Institute of Biochemistry and Technical Biochemistry Stuttgart

import setuptools
from setuptools import setup

setup(
    name='pyThermoML_work',
    version='1.0.0',
    description='Analysis of ThermoML files',
    url = 'https://github.com/ThermoPyML/pyThermoML_work',
    author='Gueltig, Matthias',
    packages=setuptools.find_packages(),
    install_requires=['matplotlib', 'numpy', 'pandas', 'pydantic', 'sklearn']
)