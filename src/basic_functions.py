import numpy as np
from src.config import Config as C

d = C.diameter
g = C.g
vapor_pressure = C.vapor_pressure
roughness = C.roughness
def find_V(Q):
  return 4*Q/(np.pi*d**2)

def find_Re(V, visc):
  return V*d/visc

def find_lyam(Re: int, eps: float = roughness/d):
    lyam: float
    if Re == 0:
        return 0
    if Re < 2320:
        lyam = 64 / Re
        if lyam > 0.1:
            lyam = 0.1
    elif (10 / eps) > Re >= 2320:
        lyam = 0.3164 / Re**0.25
    elif (10 / eps) <= Re < (500 / eps):
        lyam = 0.11 * (eps + 68 / Re) ** 0.25
    else:
        lyam = 0.11 * (eps) ** 0.25
    return lyam

def find_i(lyam, V):
    return lyam/d*V**2/2/g

def find_H(prev_H, i, x, prev_x):
    return prev_H + i*(prev_x-x)

def find_p(ro, H, z):
    return ro*g* (H - z)


def remake_parameters_with_gravity_section(p, H, prev_x, prev_H, ro, prev_z, z, prev_i, x):
    if p> vapor_pressure:
        return p, H
    else:
        numerator = (prev_H - prev_z) - vapor_pressure/ro/g
        denominator = (prev_z - z) + prev_i* (prev_x - x)
        gravity_x = prev_x + numerator/denominator * (prev_x - x)
        return vapor_pressure, z+vapor_pressure/ro/g