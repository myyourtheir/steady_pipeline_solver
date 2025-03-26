# Исходные данные (пользователь может изменять)
# 1. Характеристика технологического участка
from pprint import pprint
import numpy as np
from src.basic_functions import find_H, find_Re, find_V, find_i, find_lyam, find_p
from src.config import Config as C
from src.plot import plot

L =C.L
dx = C.dx
p0 = C.head_pressure
pL = C.end_pressure
Qmax = C.max_Q
Qmin = 0
ro = C.density
g = C.g
viscosity_1 = C.viscosity_1
withdrawal_position = C.withdrawal_position
withdrawal_flow=C.withdrawal_flow
has_withdrawal = C.has_withdrawal


def calc_section(Q, prev_H, z):
  """ Q - м3/ч H - м x - м"""
  V = find_V(Q)
  Re = find_Re(V, viscosity_1)
  lyam = find_lyam(Re)
  i = find_i(lyam, V)
  H = find_H(prev_H, i)
  p = find_p(ro, H, z)
  return [p, H]

if __name__ == '__main__':
  profile_x = np.arange(0, L, dx)
  profile_z = np.sin(profile_x / L * 10 * np.pi) * 50

  delta_H = 0.01
  can_continue = True
  HL = profile_z[-1] + pL/ ro/g
  head_H_idol = profile_z[0]+p0/(ro*g)
  iter=0
  while can_continue:
    Q=(Qmax+Qmin)/2
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
      current_Q = Q
      # Проверка на отвод
      if profile_x[index]>=withdrawal_position and has_withdrawal:
        current_Q+=withdrawal_flow
      p, H = calc_section(Q = current_Q,prev_H=prev_H, z=z)

      # Проверка на самотечный участок
      if p<=C.vapor_pressure:
        p=C.vapor_pressure
        H=z+p/ro/g

      p_list[index] = p
      H_list[index] = H
      index -= 1

    head_H_calc = H_list[0]

    if abs(head_H_calc - head_H_idol) <= delta_H:
      print('success')
      print(f"Q = {round(Q, 2)}")
      break

    if (head_H_calc>head_H_idol):
      Qmax = Q
    else:
      Qmin = Q


    iter+=1
  plot(profile_x, H_list, profile_z, [p*10**(-6) for p in p_list])



