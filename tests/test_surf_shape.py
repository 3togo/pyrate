"""
Pyrate - Optical raytracing based on Python

Copyright (C) 2014 Moritz Esslinger <moritz.esslinger@web.de>
               and Johannes Hartung <j.hartung@gmx.net>
               and     Uwe Lippmann <uwe.lippmann@web.de>
               and    Thomas Heinze <t.heinze@fn.de>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA  02110-1301, USA.
"""

import math
from hypothesis import given
from hypothesis.strategies import floats
from hypothesis.extra.numpy import arrays
import numpy as np
from core.surfShape import Conic, Asphere, Biconic, XYPolynomials
from core.localcoordinates import LocalCoordinates

# pylint: disable=no-value-for-parameter
@given(test_vector=arrays(np.float, (2, 10), elements=floats(0, 1)))
def test_sag(test_vector):
    """
    Tests for computation of sag.
    """
    conic_sag(test_vector)
    asphere_sag(test_vector)
    biconic_sag(test_vector)
    #xypolynomials_sag(test_vector)

def conic_sag(test_vector):
    """
    Computation of conic sag equals explicit calculation.
    """
    coordinate_system = LocalCoordinates(name="root")
    radius = 10.0
    conic_constant = -1.5
    curvature = 1./radius
    maxradius = (math.sqrt(1./((1+conic_constant)*curvature**2))
                 if conic_constant > -1 else radius)
    values = (2*test_vector-1.)*maxradius
    x_coordinate = values[0]
    y_coordinate = values[1]
    shape = Conic(coordinate_system, curv=curvature, cc=conic_constant)
    sag = shape.getSag(x_coordinate, y_coordinate)
    # comparison with explicitly entered formula
    assert np.allclose(sag,
                       (curvature*(x_coordinate**2+y_coordinate**2)/
                        (1.+np.sqrt(1.-(1.+conic_constant)
                                    *curvature**2
                                    *(x_coordinate**2+y_coordinate**2)))))

def asphere_sag(test_vector):
    """
    Computation of asphere sag equals explicit calculation.
    """
    coordinate_system = LocalCoordinates(name="root")
    radius = 10.0
    conic_constant = -1.5
    curvature = 1./radius
    alpha2 = 1e-3
    alpha4 = -1e-6
    alpha6 = 1e-8
    maxradius = (math.sqrt(1./((1+conic_constant)*curvature**2))
                 if conic_constant > -1 else radius)
    values = (2*test_vector-1.)*maxradius
    x_coordinate = values[0]
    y_coordinate = values[1]
    shape = Asphere(coordinate_system, curv=curvature, cc=conic_constant,
                    coefficients=[alpha2, alpha4, alpha6])
    sag = shape.getSag(x_coordinate, y_coordinate)
    # comparison with explicitly entered formula
    comparison = (curvature*(x_coordinate**2+y_coordinate**2)/
                  (1.+ np.sqrt(1.-(1.+conic_constant)
                               *curvature**2
                               *(x_coordinate**2+y_coordinate**2)))
                  +alpha2*(x_coordinate**2+y_coordinate**2)
                  +alpha4*(x_coordinate**2+y_coordinate**2)**2
                  +alpha6*(x_coordinate**2+y_coordinate**2)**3)
    assert np.allclose(sag, comparison)
    
def biconic_sag(test_vector):
    """
    Computation of biconic sag equals explicit calculation
    """
    coordinate_system = LocalCoordinates(name="root")

    radiusx = 100.0
    radiusy = 120.0
    conic_constantx = -0.5
    conic_constanty = -1.7
    
    cx = 1./radiusx
    cy = 1./radiusy
    
    alpha2 = 1e-3
    alpha4 = -1e-6
    alpha6 = 1e-8
    
    beta2 = 0.1
    beta4 = -0.6
    beta6 = 0.2
    
    maxradiusx = (math.sqrt(1./((1+conic_constantx)*cx**2))
                 if conic_constantx > -1 else radiusx)
    maxradiusy = (math.sqrt(1./((1+conic_constanty)*cy**2))
                 if conic_constanty > -1 else radiusy)
                     
    maxradius = min([maxradiusx, maxradiusy]) # choose minimal radius
    
    values = (2*test_vector - 1)*maxradius
    x_coordinate = values[0]
    y_coordinate = values[1]
    
    shape = Biconic(coordinate_system, curvx=cx, curvy=cy, ccx=conic_constantx, ccy=conic_constanty,
                    coefficients=[(alpha2, beta2), (alpha4, beta4), (alpha6, beta6)])
    sag = shape.getSag(x_coordinate, y_coordinate)
    # comparison with explicitly entered formula
    comparison = ((cx*x_coordinate**2+cy*y_coordinate**2)/
                  (1.+ np.sqrt(1.-(1.+conic_constantx)*cx**2*x_coordinate**2
                                 -(1.+conic_constanty)*cy**2*y_coordinate**2))
                  +alpha2*(x_coordinate**2+y_coordinate**2 
                      - beta2*(x_coordinate**2 - y_coordinate**2))
                  +alpha4*(x_coordinate**2+y_coordinate**2
                      - beta4*(x_coordinate**2 - y_coordinate**2))**2
                  +alpha6*(x_coordinate**2+y_coordinate**2
                      - beta6*(x_coordinate**2 - y_coordinate**2))**3)
    assert np.allclose(sag, comparison)

def xypolynomials_sag(test_vector):
    """
    Computation of biconic sag equals explicit calculation
    """

    pass    
    
