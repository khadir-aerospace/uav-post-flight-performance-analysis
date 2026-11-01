def calculate_power(voltage, current):
    power = voltage * current
    return power


def calculate_energy_wh(power_values, time_values):
    total_energy = 0

    for i in range(1, len(power_values)):
        time_difference = time_values[i] - time_values[i - 1]

        average_power = (
            power_values[i] + power_values[i - 1]
        ) / 2

        energy = average_power * time_difference / 3600

        total_energy = total_energy + energy

    return total_energy


def calculate_average_power(energy_wh, duration_seconds):
    duration_hours = duration_seconds / 3600

    if duration_hours <= 0:
        raise ValueError("Duration must be greater than zero")

    average_power = energy_wh / duration_hours

    return average_power