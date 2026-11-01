
# UAV Performance Analyst
# Lesson 12: Independent Flight Comparison

import csv
from pathlib import Path
import matplotlib.pyplot as plt


# 1. Define a function to load flight data

def load_flight_data(filename):

    project_folder = Path(__file__).resolve().parents[1] / "data"
    csv_file = project_folder / filename

    if not csv_file.exists():
        raise FileNotFoundError("Dataset not found: " + filename)

    with open(csv_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = list(reader)

    if not data:
        raise ValueError("Dataset is empty: " + filename)

    required_columns = [
        "time_s",
        "airspeed_m_s",
        "battery_voltage_v",
        "battery_current_a"
    ]

    for column in required_columns:
        if column not in data[0]:
            raise ValueError("Missing required column: " + column)

    for row in data:
        for column in required_columns:
            row[column] = float(row[column])

    return data


# 2. Calculate flight performance metrics

def analyse_flight(data):

    times = [row["time_s"] for row in data]

    airspeeds = [
        row["airspeed_m_s"] for row in data
    ]

    powers = [
        row["battery_voltage_v"] * row["battery_current_a"]
        for row in data
    ]

    duration_s = times[-1] - times[0]

    average_airspeed = sum(airspeeds) / len(airspeeds)

    average_power = sum(powers) / len(powers)

    maximum_power = max(powers)

    # Calculate energy using trapezoidal integration

    total_energy_wh = 0.0

    cumulative_energy = [0.0]

    for i in range(1, len(data)):

        time_interval_s = times[i] - times[i - 1]

        if time_interval_s <= 0:
            raise ValueError("Timestamps must increase strictly.")

        average_interval_power = (
            powers[i - 1] + powers[i]
        ) / 2

        energy_interval_wh = (
            average_interval_power * time_interval_s / 3600
        )

        total_energy_wh += energy_interval_wh

        cumulative_energy.append(total_energy_wh)

    return {
        "duration_min": duration_s / 60,
        "average_airspeed": average_airspeed,
        "average_power": average_power,
        "maximum_power": maximum_power,
        "total_energy": total_energy_wh,
        "time_min": [(t - times[0]) / 60 for t in times],
        "power": powers,
        "cumulative_energy": cumulative_energy
    }


# 3. Load and analyse both flights

try:

    flight_a = load_flight_data(
        "hypothetical_fixed_wing_flight.csv"
    )

    flight_b = load_flight_data(
        "hypothetical_fixed_wing_flight_B.csv"
    )

    results_a = analyse_flight(flight_a)

    results_b = analyse_flight(flight_b)

    # 4. Display Flight A results

    print("\n----- FLIGHT A PERFORMANCE -----")

    print("Duration:",
          round(results_a["duration_min"], 2), "minutes")

    print("Average airspeed:",
          round(results_a["average_airspeed"], 2), "m/s")

    print("Average power:",
          round(results_a["average_power"], 2), "W")

    print("Maximum power:",
          round(results_a["maximum_power"], 2), "W")

    print("Total energy:",
          round(results_a["total_energy"], 2), "Wh")

    # 5. Display Flight B results

    print("\n----- FLIGHT B PERFORMANCE -----")

    print("Duration:",
          round(results_b["duration_min"], 2), "minutes")

    print("Average airspeed:",
          round(results_b["average_airspeed"], 2), "m/s")

    print("Average power:",
          round(results_b["average_power"], 2), "W")

    print("Maximum power:",
          round(results_b["maximum_power"], 2), "W")

    print("Total energy:",
          round(results_b["total_energy"], 2), "Wh")

    # 6. Calculate and display differences

    print("\n----- FLIGHT COMPARISON -----")

    metrics = [
        ("Duration", "duration_min", "minutes"),
        ("Average airspeed", "average_airspeed", "m/s"),
        ("Average power", "average_power", "W"),
        ("Maximum power", "maximum_power", "W"),
        ("Total energy", "total_energy", "Wh")
    ]

    for label, key, unit in metrics:

        value_a = results_a[key]
        value_b = results_b[key]

        difference = value_b - value_a

        print("\n" + label)
        print("Flight A:", round(value_a, 2), unit)
        print("Flight B:", round(value_b, 2), unit)
        print("Difference:", round(difference, 2), unit)

        if value_a != 0:

            percentage_change = (
                difference / abs(value_a) * 100
            )

            print("Percentage change:",
                  round(percentage_change, 2), "%")

        else:
            print("Percentage change: not defined")

    # 7. Plot electrical power comparison

    plt.figure(figsize=(10, 5))

    plt.plot(
        results_a["time_min"],
        results_a["power"],
        label="Flight A",
        linestyle="-",
        linewidth=2
    )

    plt.plot(
        results_b["time_min"],
        results_b["power"],
        label="Flight B",
        linestyle="--",
        linewidth=2
    )

    plt.xlabel("Elapsed time (minutes)")
    plt.ylabel("Electrical power (W)")
    plt.title("Electrical Power: Flight A vs Flight B")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # 8. Plot cumulative energy comparison

    plt.figure(figsize=(10, 5))

    plt.plot(
        results_a["time_min"],
        results_a["cumulative_energy"],
        label="Flight A",
        linestyle="-",
        linewidth=2
    )

    plt.plot(
        results_b["time_min"],
        results_b["cumulative_energy"],
        label="Flight B",
        linestyle="--",
        linewidth=2
    )

    plt.xlabel("Elapsed time (minutes)")
    plt.ylabel("Cumulative energy (Wh)")
    plt.title("Energy Consumption: Flight A vs Flight B")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # 9. Finish analysis

    print("\nFlight comparison completed.")
    print("Both datasets analysed successfully.")
    print("Flight B is a hypothetical 15% higher-current scenario.")

    plt.show()


except (FileNotFoundError, ValueError, KeyError) as error:

    print("\nANALYSIS ERROR:")
    print(error)
