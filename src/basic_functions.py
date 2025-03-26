import numpy as np
from src.config import Config as C

d = C.diameter
g = C.g
vapor_pressure = C.vapor_pressure
roughness = C.roughness

dx=C.dx

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

def find_H(prev_H, i):
    return prev_H + i*dx

def find_p(ro, H, z):
    return ro*g* (H - z)
