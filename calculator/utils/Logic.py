
#from django import utils
"""
Al: Axial length of the eye (in millimeters).
k1: Keratometry Flat Meridian (in diopters)
k2: Keratometry Steep Meridian (in diopters)
average_k: Keratometry, Average corneal power (in diopters)
r: Radius of Curvature (in millimeters)
a_constant: A-constant specific to the lens being used.

V: an empirical constant value (12.0) used in the context of optical calculations.
Na: Refractive index of the aqueous and vitreous humors (1.336).
nc: Refractive index of the cornea (1.333).
Ncml: Conversion factor related to axial length measurement (0.333).
"""

import math
from decimal import Decimal

def calculate_iol_power(al, k1, k2, a_constant):
    try:

        al = Decimal(al)
        k1 = Decimal(k1)
        k2 = Decimal(k2)
        a_constant = Decimal(a_constant)
        # Calculate the average corneal power
        average_k = (k1 + k2) / Decimal(2)
        # Calculate the IOL power using the SRK/T formula
        iol_power = a_constant - (Decimal(2.5) * al) - (Decimal(0.9) * average_k)
        return iol_power
    except Exception as e:
        print(f"Error calculating IOL power: {e}")
        return None

def SRKT_SE(al, k1, k2, a_constant, iol_power, ac_depth):
    # Ensure all inputs are Decimal
    al = Decimal(al)
    k1 = Decimal(k1)
    k2 = Decimal(k2)
    a_constant = Decimal(a_constant)
    iol_power = Decimal(iol_power)
    ac_depth = Decimal(ac_depth)
    
    # Define constants
    average_k = (k1 + k2) / Decimal(2)
    r = Decimal(337.5) / average_k
    V = Decimal(12.0)
    na = Decimal(1.336)
    nc = Decimal(1.333)
    ncml = Decimal(0.333)

    # Calculate ACD Constant
    ACDconst = Decimal(0.62467) * a_constant - Decimal(68.747)
    offset = ACDconst - Decimal(3.336)

    # Calculate LCOR
    if al <= Decimal(24.2):
        LCOR = al
    else:
        LCOR = Decimal(-3.446) + (Decimal(1.715) * al) - (Decimal(0.0237) * (al**2))

    # Calculate Cw
    Cw = Decimal(-5.40948) + (Decimal(0.58412) * LCOR) + (Decimal(0.098) * average_k)

    # Define setH function
    def setH(r, Cw):
        x = r**2 - (Cw**2 / Decimal(4.0))
        if x < 0:
            x = 0
        H = r - Decimal(math.sqrt(x))
        return H

    # Calculate ELP
    H = setH(r, Cw)
    ACDest = H + offset

    # Calculate RETHICK
    RETHICK = Decimal(0.65696) + Decimal(0.02029) * al

    # Calculate LOPT
    LOPT = al + RETHICK

    # Calculate SEpred
    num = Decimal(1000) * na * (na * r - ncml * LOPT) - iol_power * (LOPT - ACDest) * (na * r - ncml * ACDest)
    denum = na * (V * (na * r - ncml * LOPT) + LOPT * r) - Decimal(0.001) * iol_power * (LOPT - ACDest) * (V * (na * r - ncml * ACDest) + ACDest * r)
    SEpred = round(num / denum, 3)

    return SEpred



