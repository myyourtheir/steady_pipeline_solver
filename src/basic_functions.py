from math import exp
import math
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


def find_nps_H(Q, a, b, n):
    return (a - b * Q**2)*n


def find_viscosity(T):
  return C.viscosity_0* exp(-C.K*(T-C.T_visc_0))


def find_T(prev_T, Q, i):
    return prev_T + (math.pi*C.Kt*C.diameter/C.density/Q/C.Cv * (prev_T-C.Tokr)-C.g*i/C.Cv)*C.dx

def bisection_method(a, b, func, tol=1e-6, max_iter=1000):
    fa = func(a)
    fb = func(b)
    
    if fa * fb >= 0:
        raise ValueError("Функция не меняет знак на заданном интервале.")
    
    for _ in range(max_iter):
        c = (a + b) / 2
        fc = func(c)
        
        if abs(fc) < tol or (b - a) / 2 < tol:
            return c
        
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
    
    raise RuntimeError("Метод бисекции не сходится за заданное число итераций.")