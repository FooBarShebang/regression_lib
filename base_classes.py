#usr/bin/python3
"""
Module regression_lib.base_classes

Implements the (abstract) base classes for the library.
"""

__version__= '0.1.0.0'
__date__ = '15-10-2026'
__status__ = 'Development'

#imports

#+ standard library

import sys
import os

from typing import Union

#+ other libraries

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(MODULE_PATH)
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

from phyqus_lib.base_classes import MeasuredValue as TMF

from statistics_lib.data_classes import Statistics2D

#globals

#+ types

TReal = Union[int, float]

#classes

class TUniVarLinRegressionResult:
    """
    Storage (data) class for the results of linear univariant regression.

    Attributes:
        N: int
        Slope: phyqus_lib.base_classes.MeasuredValue
        Intercept: phyqus_lib.base_classes.MeasuredValue
        Slope_CI: float
        Intercept_CI: float
        R2: float
        GF: float
        RMSD: float
    
    Properties:
        N_Predictors: int
        N_Estimators: int
        Results: tuple(phyqus_lib.base_classes.MeasuredValue OR float)
        Results_CI: tuple(float)
    
    Version 1.0.0.0
    """

    #class variables, which actual values will be set at the instance level
    #+ default None value in instance means that it was not (yet) assigned

    N: int | None = None #number of data points used
    Slope: TMF | None = None #mean + SE stored in MeasuredValue instance
    Intercept: TMF | None = None #mean + SE stored in MeasuredValue instance
    Slope_CI: float | None = None #SE corrected with t-value
    Intercept_CI: float | None = None #SE corrected with t-value
    R2: float | None = None #coefficient of determination in predictor
    #+ error-free (vertical distance) definition
    GF: float | None = None #generalized 'goodness of fit' as 1 - RMSD^2 / Stot,
    #+ where RMSD^2 is the mean squared distance from data point to the fit line
    #+ and Stot is the total data set variance, defined as mean squared distance
    #+ form the center of gravity to each data point
    RMSD: float | None = None

    @property
    def N_Predictors(self) -> int:
        """
        Read-only (getter) property returning the number of independent
        variables in the regression model. Fixed to 1 for univariant models.
        """
        return 1

    @property
    def N_Estimators(self) -> int:
        """
        Read-only (getter) property returning the number of estimators in the
        used regression model. Fixed to 2 for univariant linear models.
        """
        return 2

    @property
    def Results(self) -> tuple[TMF, TMF, float, float, float, int]:
        """
        Read-only (getter) property returning the aggregated fit results in a
        single tuple of:
        * Slope: MeasuredValue instance (with uncertainty - SE)
        * Intercept: MeasuredValue instance (with uncertainty - SE)
        * R2: float as a measure of y-only 'goodness of fit'
        * GF: float as a measure of xy-orthogonal 'goodness of fit'
        * RMSD: float as 'average' distance between the data points and fit line
        * N: int - number of data points used in the model
        """
        return (self.Slope, self.Intercept, self.R2, self.GF, self.RMSD, self.N)

    @property
    def Results_CI(self) -> tuple[float, float, float, float]:
        """
        Read-only (getter) property returning as a single tuple
        * Slope: float
        * Intercept: float
        * Slope_CI: float (SE of the estimator times t-correction)
        * Intercept_CI: float (SE of the estimator times t-correction)

        This 'light' version is designed specifically for calculations of the
        actual Confidence Intervals of the fit.
        """
        return (self.Slope.Value, self.Intercept.Value, self.Slope_CI,
                self.Intercept_CI)