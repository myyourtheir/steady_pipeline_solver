import numpy as np
import matplotlib.pyplot as plt

# Исходные данные (пользователь может изменять)
# 1. Характеристика технологического участка
L = 100000  # Протяженность участка, м
profile_x = np.linspace(0, L, 100)  # Координаты сечений трубопровода
profile_z = np.sin(profile_x / L * 2 * np.pi) * 50 + 100  # Профиль трубопровода (высота), м
diameter = 1.2  # Диаметр трубы, м
wall_thickness = 0.012  # Толщина стенки, м
roughness = 0.0001  # Абсолютная шероховатость, м
nps_positions = [20000, 60000]  # Позиции НПС, м
withdrawal_position = 40000  # Позиция отвода, м
withdrawal_flow = -500  # Расход отбора/закачки через отвод, м³/ч (отрицательное значение - отбор)

# 2. Гидравлическая характеристика агрегатов на НПС
a_head = 2500  # Коэффициент a в уравнении H = a - bQ^2, м
b_head = 0.0001  # Коэффициент b в уравнении H = a - bQ^2, м/(м³/ч)^2
cavitation_margin = 50000  # Противокавитационный запас насосов, Па

# 3. Свойства перекачиваемой нефти
density = 850  # Плотность нефти, кг/м³
viscosity_1 = 0.001  # Кинематическая вязкость при температуре T1, м²/с
viscosity_2 = 0.0005  # Кинематическая вязкость при температуре T2, м²/с
T1, T2 = 20, 50  # Температуры для вязкости, °C
vapor_pressure = 50000  # Давление упругости насыщенных паров, Па

# 4. Условия эксплуатации
head_pressure = 200000  # Подпор головной станции, Па
end_pressure = 100000  # Давление в конце участка, Па
outlet_temperature = 60  # Температура на выходе НПС, °C
ambient_temperature = 10  # Температура окружающей среды, °C

# Константы
g = 9.81  # Ускорение свободного падения, м/с²
Cp = 2000  # Удельная теплоемкость нефти, Дж/(кг·°C)
thermal_conductivity = 0.1  # Теплопроводность, Вт/(м·°C)

# Функции для расчетов
def hydraulic_gradient(Q, d, nu, e):
    """Рассчитывает гидравлический уклон по формуле Дарси-Вейсбаха."""
    Re = 4 * Q / (np.pi * d * nu)  # Число Рейнольдса
    lambda_f = (0.11 * (e / d + 68 / Re) ** 0.25)  # Коэффициент трения
    i = lambda_f * (Q ** 2) / (2 * g * (d ** 5))  # Гидравлический уклон
    return i

def temperature_change(T, Q, d, dx, ambient_T):
    """Рассчитывает изменение температуры на участке."""
    heat_loss = thermal_conductivity * np.pi * d * (T - ambient_T) / (density * Q * Cp)
    return T - heat_loss * dx

def calculate_flow_and_pressures(L, profile_x, profile_z, diameter, roughness, nps_positions, withdrawal_position, withdrawal_flow):
    """Основная функция для расчета теплогидравлического режима."""
    dx = profile_x[1] - profile_x[0]
    Q = 2000  # Начальное предположение расхода, м³/ч
    pressures = []
    temperatures = []
    hydraulic_line = []

    for i in range(len(profile_x)):
        x = profile_x[i]
        z = profile_z[i]

        # Расчет давления и температуры
        pressure = head_pressure if i == 0 else pressures[-1] - hydraulic_gradient(Q, diameter, viscosity_1, roughness) * dx * density * g
        temperature = outlet_temperature if i == 0 else temperature_change(temperatures[-1], Q, diameter, dx, ambient_temperature)

        # Обработка НПС
        if x in nps_positions:
            pressure += (a_head - b_head * Q**2) * density * g

        # Обработка отвода
        if x == withdrawal_position:
            Q += withdrawal_flow

        # Сохранение результатов
        pressures.append(pressure)
        temperatures.append(temperature)
        hydraulic_line.append(z + pressure / (density * g))

    return pressures, temperatures, hydraulic_line

# Выполнение расчетов
pressures, temperatures, hydraulic_line = calculate_flow_and_pressures(
    L, profile_x, profile_z, diameter, roughness, nps_positions, withdrawal_position, withdrawal_flow
)

# Построение графиков
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
plt.ylabel("Давление, Па")
plt.legend()

# Распределение температуры
plt.subplot(3, 1, 3)
plt.plot(profile_x, temperatures, label="Температура", color="blue")
plt.title("Распределение температуры")
plt.xlabel("Расстояние, м")
plt.ylabel("Температура, °C")
plt.legend()

plt.tight_layout()
plt.show()