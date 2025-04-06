import math
from pprint import pprint
import numpy as np
from src.basic_functions import  bisection_method, find_H, find_Re, find_T, find_V, find_i, find_lyam, find_nps_H, find_p, find_viscosity
from src.config import NPS, Config as C
from src.plot import plot

L =C.L
dx = C.dx
p0 = C.head_pressure
pL = C.end_pressure
Qmax = C.max_Q
Qmin = 0
ro = C.density
g = C.g
d = C.diameter
viscosity_1 = C.viscosity_1
withdrawal_position = C.withdrawal_position
withdrawal_flow=C.withdrawal_flow
has_withdrawal = C.has_withdrawal
NPS_list = C.NPS_list


def make_profiles():
  profile_x = np.arange(0, L, dx)
  # profile_z = np.zeros(profile_x.size)
  profile_z = np.sin(profile_x / L * 10 * np.pi) * 500
  nps_vsas_indexes = []
  for nps in NPS_list:
    index = np.where(profile_x == nps.position)[0][0]
    nps_vsas_indexes.append(index)
    profile_x = np.insert(profile_x, index, nps.position)
    profile_z = np.insert(profile_z, index, profile_z[index])
    
  return profile_x, profile_z,nps_vsas_indexes


def make_initial_nps_mode_data(NPS_list: list[NPS]):
  nps_mode_data = {}
  for nps in NPS_list:
    nps_mode_data[nps.title] = {
      "title": nps.title,
      "p_vsas": 0,
      "p_nagn": 0,
    }
  return nps_mode_data

def check_withdrawal_Q(x, Q):
    if x>=withdrawal_position and has_withdrawal:
      return Q+withdrawal_flow
    return Q

def pipeline_traverse(Q, i, H_list,T_list, profile_x, profile_z, nps_mode_data,visc_list=[], with_temperature=False):
  index = profile_x.size-2
  while index>=0:
    prev_H = H_list[index+1]
    prev_T = T_list[index+1]
    x = profile_x[index]
    z = profile_z[index]
    current_Q = Q
    # Проверка на отвод
    if x>=withdrawal_position and has_withdrawal:
     current_Q+=withdrawal_flow

    V = find_V(current_Q)
    p_list[-1] = pL
    H_list[-1] = HL
    Re = find_Re(V, viscosity_1)
    if with_temperature: 
      T = find_T(i=i, Q=current_Q, prev_T=prev_T)
      T_list[index] = T
      viscosity = find_viscosity(T)
      visc_list[index] = viscosity
      Re = find_Re(V, viscosity)
    lyam = find_lyam(Re)
    i = find_i(lyam, V)
    H = find_H(prev_H, i)
    p = find_p(ro, H, z)
      
    # Проверка на самотечный участок
    if p<=C.vapor_pressure:
      p=C.vapor_pressure
      H=z+p/ro/g
    # Всас НПС
    if index in nps_vsas_indexes:
      current_NPS = [nps for nps in NPS_list if nps.position == profile_x[index]][0]
      dH = find_nps_H(Q, current_NPS.a, current_NPS.b, current_NPS.n)
      H = H_list[index+1] - dH
      p_vsas = ro*g*(H-z)
      p = p_vsas
      nps_mode_data[current_NPS.title]['p_vsas'] = p
      nps_mode_data[current_NPS.title]['p_nagn'] = p_list[index+1]
    p_list[index] = p
    H_list[index] = H
    i_list[index] = i
    index -= 1


def find_gravity_sections(profile_x, profile_z, p_list, H_list,Q, visc_list):
    gravity_sections = []
    for index in range(profile_x.size):
      p = p_list[index]
      H = H_list[index]
      z=profile_z[index]
      prev_p = p_list[index-1]
      prev_H = H_list[index-1]
      prev_z=profile_z[index-1]

      is_gravity_index = p==C.vapor_pressure and H==z+p/ro/g
      is_prev_gravity_index = prev_p==C.vapor_pressure and prev_H==prev_z+prev_p/ro/g

      if not is_prev_gravity_index and is_gravity_index:
          gravity_sections.append({'start': profile_x[index], "start_z": z, 'end': profile_x[index], "end_z":z})
      if is_prev_gravity_index and not is_gravity_index:
          gravity_sections[-1]['end'] = profile_x[index]
          gravity_sections[-1]['end_z'] = z

    for index,gravity_section in enumerate(gravity_sections):
        
      dH = gravity_section['end_z']-gravity_section['start_z']
      L = gravity_section['end']-gravity_section['start']
      gravity_sections[index]['L'] = L
      alpha = math.atan(abs(dH)/L)
      constant = (0.2419 * Q) / d**(8/3) / math.sqrt(abs(math.sin(alpha)))
      def f(phi):
        return phi - np.sin(phi) - (constant**(3/5)) * (phi**(2/5))
 
      phi = bisection_method(0.1, math.pi, f)
      gravity_sections[index]['filling degree'] = (phi-math.sin(phi))/2/math.pi
    return gravity_sections


if __name__ == '__main__':
  profile_x, profile_z,nps_vsas_indexes = make_profiles()

  delta_H = 0.01
  can_continue = True
  HL = profile_z[-1] + pL/ ro/g
  head_H_idol = profile_z[0]+p0/(ro*g)
  iter=0
  nps_mode_data = make_initial_nps_mode_data(NPS_list)
  while can_continue:
    p_list = np.zeros(profile_x.size)
    H_list = np.zeros(profile_x.size)
    T_list = np.zeros(profile_x.size)
    i_list = np.zeros(profile_x.size)
    visc_list = np.zeros(profile_x.size)

    Q=(Qmax+Qmin)/2
    V = find_V(Q)
    p_list[-1] = pL
    H_list[-1] = HL
    Re = find_Re(V, viscosity_1)
    lyam = find_lyam(Re)
    i = find_i(lyam, V)
    i_list[-1] = i
    T_list[-1] = C.Tk

    pipeline_traverse(Q=Q,i=i, H_list=H_list,T_list=T_list, profile_x=profile_x, nps_mode_data= nps_mode_data,profile_z=profile_z)
    pipeline_traverse(Q=Q,i=i, H_list=H_list,T_list=T_list, profile_x=profile_x, nps_mode_data= nps_mode_data,profile_z=profile_z,visc_list=visc_list, with_temperature=True)



    head_H_calc = H_list[0]

    if abs(head_H_calc - head_H_idol) <= delta_H:
      break

    if (head_H_calc>head_H_idol):
      Qmax = Q
    else:
      Qmin = Q
    iter+=1

  
  isSuccess = True
  for i in nps_vsas_indexes:
    current_NPS = [nps for nps in NPS_list if nps.position == profile_x[i]][0]
    if H_list[i]-profile_z[i]<current_NPS.cavitation_margin:
      isSuccess = False
  if isSuccess:
    print('Q = ', Q, 'm³/c')
    pprint([{
      'Станция': title,
      'Давление в линии всасывания': f'{nps['p_vsas']/10**6} МПа',
      'Давление в линии нагнетания': f'{nps['p_nagn']/10**6} МПа',
    } for title, nps in nps_mode_data.items()])
    gravity_sections = find_gravity_sections(H_list=H_list, profile_x=profile_x, p_list=p_list, profile_z=profile_z, Q=Q, visc_list=visc_list)
    pprint([{
      'Начало самотечного участка': f'{section['start']} м',
      'Конец самотечного участка': f'{section["end"]} м',
      'Длина самотечного участка': f'{section["L"]} м',
      'Степень заполнения': section["filling degree"],
    } for section in gravity_sections])
    plot(profile_x, H_list, profile_z, [p*10**(-6) for p in p_list], T_list)
  else: 
    print('fail')



