import numpy as np

class NPS:
  def __init__(self, position, a, b, cavitation_margin):
    self.position = position
    self.a = a
    self.b = b
    self.cavitation_margin = cavitation_margin
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
    NPS(0, 310, 0.0000008, 0),
    NPS(22000, 310, 0.0000008, 5),
    NPS(60000, 310, 0.0000008, 5)
  ]

  # 3. Свойства перекачиваемой нефти
  density = 850  # Плотность нефти, кг/м³
  viscosity_1 = 0.00001  # Кинематическая вязкость при температуре T1, м²/с
  viscosity_2 = 0.0005  # Кинематическая вязкость при температуре T2, м²/с
  T1, T2 = 20, 50  # Температуры для вязкости, °C
  vapor_pressure = 50000  # Давление упругости насыщенных паров, Па

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
  Cp = 2000  # Удельная теплоемкость нефти, Дж/(кг·°C)
  thermal_conductivity = 0.1  # Теплопроводность, Вт/(м·°C)
  dx = 1000


  max_Q = 10 # м³/c



