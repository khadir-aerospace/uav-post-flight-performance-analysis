import csv
from pathlib import Path
import matplotlib.pyplot as plt

from uav_calculations import (
    calculate_power,
    calculate_energy_wh,
    calculate_average_power
)


# --------------------------------------------------
# 1. LOAD FLIGHT DATA
# --------------------------------------------------

project_folder = Path(__file__).resolve().parents[1] / "data"

csv_file = project_folder / "hypothetical_fixed_wing_flight.csv"

data = []

try:
    with open(csv_file, "r", newline="") as file:
        reader = csv.DictReader(file)

        required_columns = [
            "time_s",
            "flight_phase",
            "airspeed_m_s",
            "altitude_m",
            "battery_voltage_v",
            "battery_current_a",
            "electrical_power_w",
            "cumulative_energy_wh"
        ]

        missing_columns = [
            column for column in required_columns
            if column not in (reader.fieldnames or [])
        ]

        if missing_columns:
            raise ValueError(
                "Missing required columns: " + str(missing_columns)
            )

        for row in reader:
            data.append(row)

except FileNotFoundError:
    print("ERROR: Flight CSV file not found.")
    print("Expected file:", csv_file)
    raise SystemExit

except ValueError as error:
    print("ERROR:", error)
    raise SystemExit


if len(data) < 2:
    print("ERROR: Not enough flight data to analyse.")
    raise SystemExit


# --------------------------------------------------
# 2. CONVERT DATA TO NUMBERS
# --------------------------------------------------

try:
    time_values = [float(row["time_s"]) for row in data]

    airspeed_values = [
        float(row["airspeed_m_s"]) for row in data
    ]

    altitude_values = [
        float(row["altitude_m"]) for row in data
    ]

    voltage_values = [
        float(row["battery_voltage_v"]) for row in data
    ]

    current_values = [
        float(row["battery_current_a"]) for row in data
    ]

    supplied_power_values = [
        float(row["electrical_power_w"]) for row in data
    ]

    supplied_energy_values = [
        float(row["cumulative_energy_wh"]) for row in data
    ]

    flight_phases = [
        row["flight_phase"] for row in data
    ]

except (ValueError, TypeError) as error:
    print("ERROR: Invalid numerical data in CSV.")
    print(error)
    raise SystemExit


if any(
    time_values[i] <= time_values[i - 1]
    for i in range(1, len(time_values))
):
    print("ERROR: Timestamps must be strictly increasing.")
    raise SystemExit


if any(
    value < 0
    for value in current_values + voltage_values + airspeed_values
):
    print("ERROR: Negative voltage, current or airspeed detected.")
    raise SystemExit


# --------------------------------------------------
# 3. BASIC DATASET INFORMATION
# --------------------------------------------------

print("\n===================================")
print("       UAV FLIGHT ANALYSIS")
print("===================================")

print("Dataset:", csv_file.name)
print("Number of samples:", len(data))
print("Number of columns:", len(data[0]))

print(
    "Flight duration:",
    round((time_values[-1] - time_values[0]) / 60, 2),
    "minutes"
)

print("\nFirst five rows:")

for row in data[:5]:
    print(row)


# --------------------------------------------------
# 4. CHECK FOR MISSING VALUES
# --------------------------------------------------

missing_values = 0

for row in data:
    for value in row.values():
        if value is None or value.strip() == "":
            missing_values += 1

print("\nMissing cells:", missing_values)


# --------------------------------------------------
# 5. CHECK TIMESTAMP INTERVALS
# --------------------------------------------------

unexpected_gaps = 0

for i in range(1, len(time_values)):
    interval = time_values[i] - time_values[i - 1]

    if interval != 1:
        unexpected_gaps += 1

print("Unexpected timestamp intervals:", unexpected_gaps)


# --------------------------------------------------
# 6. VERIFY POWER CALCULATIONS
# --------------------------------------------------

calculated_power_values = []

for voltage, current in zip(voltage_values, current_values):

    power = calculate_power(voltage, current)

    calculated_power_values.append(power)


power_differences = []

for calculated, supplied in zip(
    calculated_power_values,
    supplied_power_values
):
    power_differences.append(abs(calculated - supplied))


maximum_power_difference = max(power_differences)

print("\n===================================")
print("       POWER VERIFICATION")
print("===================================")

print(
    "Maximum difference between calculated and supplied power:",
    round(maximum_power_difference, 4),
    "W"
)


# --------------------------------------------------
# 7. CALCULATE TOTAL ENERGY
# --------------------------------------------------

total_energy = calculate_energy_wh(
    calculated_power_values,
    time_values
)

supplied_final_energy = supplied_energy_values[-1]

energy_difference = abs(
    total_energy - supplied_final_energy
)

print("\n===================================")
print("       ENERGY VERIFICATION")
print("===================================")

print("Calculated total energy:", round(total_energy, 2), "Wh")

print(
    "Supplied final cumulative energy:",
    round(supplied_final_energy, 2),
    "Wh"
)

print("Energy difference:", round(energy_difference, 4), "Wh")


# --------------------------------------------------
# 8. CALCULATE AVERAGE POWER
# --------------------------------------------------

duration_seconds = time_values[-1] - time_values[0]

average_power = calculate_average_power(
    total_energy,
    duration_seconds
)

print("\n===================================")
print("       FLIGHT PERFORMANCE")
print("===================================")

print(
    "Average airspeed:",
    round(sum(airspeed_values) / len(airspeed_values), 2),
    "m/s"
)

print(
    "Average voltage:",
    round(sum(voltage_values) / len(voltage_values), 2),
    "V"
)

print(
    "Minimum voltage:",
    round(min(voltage_values), 2),
    "V"
)

print(
    "Maximum voltage:",
    round(max(voltage_values), 2),
    "V"
)

print(
    "Average current:",
    round(sum(current_values) / len(current_values), 2),
    "A"
)

print(
    "Maximum current:",
    round(max(current_values), 2),
    "A"
)

print(
    "Average power:",
    round(average_power, 2),
    "W"
)

print(
    "Maximum power:",
    round(max(calculated_power_values), 2),
    "W"
)

print("Total energy:", round(total_energy, 2), "Wh")


# --------------------------------------------------
# 9. ENERGY CONSUMPTION BY FLIGHT PHASE
# --------------------------------------------------

phase_energy = {}
phase_duration = {}
phase_power_sum = {}
phase_interval_count = {}

for i in range(1, len(data)):

    phase = flight_phases[i - 1]

    time_difference = time_values[i] - time_values[i - 1]

    average_interval_power = (
        calculated_power_values[i - 1]
        + calculated_power_values[i]
    ) / 2

    interval_energy = (
        average_interval_power * time_difference / 3600
    )

    if phase not in phase_energy:
        phase_energy[phase] = 0
        phase_duration[phase] = 0
        phase_power_sum[phase] = 0
        phase_interval_count[phase] = 0

    phase_energy[phase] += interval_energy

    phase_duration[phase] += time_difference

    phase_power_sum[phase] += average_interval_power

    phase_interval_count[phase] += 1


print("\n===================================")
print("       ENERGY BY FLIGHT PHASE")
print("===================================")

for phase in phase_energy:

    energy = phase_energy[phase]

    duration = phase_duration[phase]

    average_phase_power = (
        phase_power_sum[phase] / phase_interval_count[phase]
    )

    energy_percentage = energy / total_energy * 100

    print("\nFlight phase:", phase)

    print("Duration:", round(duration / 60, 2), "minutes")

    print("Energy:", round(energy, 2), "Wh")

    print(
        "Average power:",
        round(average_phase_power, 2),
        "W"
    )

    print(
        "Share of total energy:",
        round(energy_percentage, 2),
        "%"
    )


# --------------------------------------------------
# 10. PLOT POWER AGAINST TIME
# --------------------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(
    time_values,
    calculated_power_values,
    label="Electrical Power"
)

plt.xlabel("Time (seconds)")
plt.ylabel("Power (W)")
plt.title("UAV Electrical Power During Flight")

plt.grid(True)
plt.legend()
plt.tight_layout()


# --------------------------------------------------
# 11. PLOT BATTERY VOLTAGE
# --------------------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(
    time_values,
    voltage_values,
    label="Battery Voltage"
)

plt.xlabel("Time (seconds)")
plt.ylabel("Voltage (V)")
plt.title("UAV Battery Voltage During Flight")

plt.grid(True)
plt.legend()
plt.tight_layout()


# --------------------------------------------------
# 12. PLOT AIRSPEED
# --------------------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(
    time_values,
    airspeed_values,
    label="Airspeed"
)

plt.xlabel("Time (seconds)")
plt.ylabel("Airspeed (m/s)")
plt.title("UAV Airspeed During Flight")

plt.grid(True)
plt.legend()
plt.tight_layout()


# --------------------------------------------------
# 13. PLOT CUMULATIVE ENERGY
# --------------------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(
    time_values,
    supplied_energy_values,
    label="Recorded Cumulative Energy"
)

plt.xlabel("Time (seconds)")
plt.ylabel("Energy (Wh)")
plt.title("UAV Cumulative Energy Consumption")

plt.grid(True)
plt.legend()
plt.tight_layout()


# --------------------------------------------------
# 14. PLOT ENERGY BY FLIGHT PHASE
# --------------------------------------------------

phase_labels = {
    "takeoff_climb": "Takeoff / Climb",
    "climb": "Climb",
    "cruise": "Cruise",
    "descent": "Descent",
    "landing": "Landing"
}

labels = [
    phase_labels.get(phase, phase)
    for phase in phase_energy.keys()
]

values = list(phase_energy.values())

plt.figure(figsize=(10, 5))

bars = plt.bar(labels, values)

plt.xlabel("Flight Phase")
plt.ylabel("Energy Consumption (Wh)")
plt.title("Energy Consumption by Flight Phase")

# Display energy values above each bar
for bar in bars:
    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        round(height, 2),
        ha="center",
        va="bottom"
    )

plt.grid(axis="y", alpha=0.3)
plt.tight_layout()


# --------------------------------------------------
# 15. FINAL RESULT
# --------------------------------------------------

print("\n===================================")
print("       ANALYSIS COMPLETED")
print("===================================")

print("Flight dataset analysed successfully.")

print("Power calculations verified.")

print("Total energy independently calculated.")

print("Flight-phase energy analysis completed.")

print("\nNote: This is hypothetical teaching data.")
print("It is not a validated real aircraft performance model.")

plt.show()
