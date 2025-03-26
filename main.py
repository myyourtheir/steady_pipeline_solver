# Исходные данные (пользователь может изменять)
# 1. Характеристика технологического участка
from pprint import pprint
import numpy as np
from src.basic_functions import find_H, find_Re, find_V, find_i, find_lyam, find_p, remake_parameters_with_gravity_section
from src.config import Config as C
from src.plot import plot

L =C.L
dx = C.dx
p0 = C.head_pressure
pL = C.end_pressure
max_Q = C.max_Q
ro = C.density
g = C.g
viscosity_1 = C.viscosity_1



def calc_section(Q, x, prev_H, prev_x, z):
  """ Q - м3/ч H - м x - м"""
  V = find_V(Q)
  Re = find_Re(V, viscosity_1)
  lyam = find_lyam(Re)
  i = find_i(lyam, V)
  H = find_H(prev_H, i, x, prev_x)
  p = find_p(ro, H, z)
  return [p, H]


def find_last_i(Q):
    V = find_V(Q)
    Re = find_Re(V, viscosity_1)
    lyam = find_lyam(Re)
    i = find_i(lyam, V)
    return i

if __name__ == '__main__':
  profile_x = np.arange(0, L, dx)
  profile_z = np.sin(profile_x / L * 10 * np.pi) * 1000
  prev_Q = float('inf')
  Q = max_Q/2
  delta_Q = 0.001
  is_first_iteration = True
  can_continue = True
  HL = profile_z[-1] + pL/ ro/g
  while can_continue:

    p_list = np.zeros(profile_x.size)
    H_list = np.zeros(profile_x.size)
    p_list[-1] = pL
    H_list[-1] = HL

    index = profile_x.size-2

    while index>=0:
      prev_H = H_list[index+1]
      prev_x = profile_x[index+1]
      prev_z = profile_z[index+1]
      x = profile_x[index]
      z = profile_z[index]

      p, H = calc_section(Q = Q,prev_H=prev_H, x=x, prev_x=prev_x, z=z)
      # Проверка на самотечный участок
      if p<=C.vapor_pressure:
        p=C.vapor_pressure
        H=z-p/ro/g

      p_list[index] = p
      H_list[index] = H
      index -= 1
    if abs(Q - prev_Q) < delta_Q:
      print('success')
      break
    if (not is_first_iteration):
      prev_Q = Q
      head_H_calc = H_list[0]
      head_H_idol = p0/(ro*g)
      if (head_H_calc>head_H_idol):
        Q = prev_Q/2
        if Q<=1:
          print('cannot find solution')
          break
      else:
        Q = prev_Q + 0.5*(max_Q-prev_Q)
        if Q > max_Q:
          print('cannot find solution')
          break
    is_first_iteration = False
  plot(profile_x, H_list, profile_z, [p*10**(-6) for p in p_list])



