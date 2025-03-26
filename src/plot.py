from matplotlib import pyplot as plt

def plot(profile_x, hydraulic_line, profile_z, pressures ):
  plt.figure(figsize=(12, 8))

  # Линия гидравлического уклона и профиль трубопровода
  plt.subplot(3, 1, 1)
  plt.plot(profile_x, hydraulic_line, label="Линия гидравлического уклона")
  plt.plot(profile_x, profile_z, label="Профиль трубопровода", linestyle="--")
  plt.title("Линия гидравлического уклона и профиль трубопровода")
  plt.xlabel("Расстояние, м")
  plt.ylabel("Высота, м")
  plt.legend()

  # Распределение давления
  plt.subplot(3, 1, 2)
  plt.plot(profile_x, pressures, label="Давление", color="red")
  plt.title("Распределение давления")
  plt.xlabel("Расстояние, м")
  plt.ylabel("Давление, МПа")
  plt.legend()

  # Распределение температуры
  # plt.subplot(3, 1, 3)
  # plt.plot(profile_x, temperatures, label="Температура", color="blue")
  # plt.title("Распределение температуры")
  # plt.xlabel("Расстояние, м")
  # plt.ylabel("Температура, °C")
  # plt.legend()

  plt.tight_layout()
  plt.show()