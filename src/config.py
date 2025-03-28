import numpy as np

class NPS:
  def __init__(self, position, a, b, cavitation_margin, title=''):
    self.position = position
    self.a = a
    self.b = b
    self.cavitation_margin = cavitation_margin
    self.title = title
  def __str__(self):
    return f"NPS(position={self.position}, a={self.a}, b={self.b}, cavitation_margin={self.cavitation_margin})"
class Config: 
  L = 100000  # Протяженность участка, м
  diameter = 1.2  # Диаметр трубы, м
  wall_thickness = 0.012  # Толщина стенки, м
  roughness = 0.0002  # Абсолютная шероховатость, м
  nps_positions = [20000, 60000]  # Позиции НПС, м
  withdrawal_position = 40000  # Позиция отвода, м
  withdrawal_flow = -500  # Расход отбора/закачки через отвод, м³/ч (отрицательное значение - отбор)

  # 2. Гидравлическая характеристика агрегатов на НПС
  NPS_list = [
    NPS(0, 310, 0.0000008, 0, 'ГНПС'),
    NPS(22000, 310, 0.0000008, 5, 'НПС 1'),
    NPS(60000, 310, 0.0000008, 5, 'НПС 2')
  ]

  # 3. Свойства перекачиваемой нефти
  density = 850  # Плотность нефти, кг/м³
  viscosity_1 = 0.00001  # Кинематическая вязкость при температуре T1, м²/с
  viscosity_0 = 0.0005  # Кинематическая вязкость при температуре T2, м²/с
  T_visc_0 =20+273.15  # Температура вязкости, K
  Tk = 60+273.15  # Температура в конце участка, K
  Kt = 0.1  # Коэффициент теплопроводности, Вт/(м³/ч)
  Tokr = 10+273.15  # Температура окружающей среды, K
  vapor_pressure = 50000  # Давление упругости насыщенных паров, Па
  Cv = 2000 # Удельная теплоемкость нефти, Дж/(кг·K)

  # 4. Условия эксплуатации
  head_pressure = 3*10**6  # Подпор головной станции, Па
  end_pressure = 1*10**5  # Давление в конце участка, Па
  outlet_temperature = 60  # Температура на выходе НПС, °C
  ambient_temperature = 10  # Температура окружающей среды, °C

  # 5. Отводы/подкачки
  has_withdrawal = False
  withdrawal_position = 50000  # Позиция отвода, м
  withdrawal_flow = -0.5  # Расход отбора/закачки через отвод, м³/c (отрицательное значение - отбор)

  # Константы
  g = 9.81  # Ускорение свободного падения, м/с²
  thermal_conductivity = 0.1  # Теплопроводность, Вт/(м·°C)
  dx = 1000


  max_Q = 10 # м³/c



