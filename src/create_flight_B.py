
# UAV Performance Analyst
# Lesson 12: Generate Modified Flight B Dataset

import csv
from pathlib import Path


# 1. Locate the original dataset

project_folder = Path(__file__).resolve().parents[1] / "data"

input_file = project_folder / "hypothetical_fixed_wing_flight.csv"

output_file = project_folder / "hypothetical_fixed_wing_flight_B.csv"


# 2. Define the experiment

current_increase_factor = 1.15

# Original battery specification:
# 6S LiPo, nominal voltage 22.2 V, capacity 10 Ah
# Nominal energy = 22.2 x 10 = 222 Wh

nominal_battery_energy_wh = 222.0


# 3. Load the original dataset

if not input_file.exists():

    print("ERROR: Original dataset not found.")
    print("Expected file:", input_file)

else:

    with open(input_file, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        column_names = reader.fieldnames

        flight_data = list(reader)

    if not flight_data:

        print("ERROR: Original dataset is empty.")

    else:

        # 4. Modify battery current and recalculate power

        for row in flight_data:

            original_current = float(row["battery_current_a"])

            voltage = float(row["battery_voltage_v"])

            new_current = (
                original_current * current_increase_factor
            )

            new_power = voltage * new_current

            row["battery_current_a"] = round(new_current, 4)

            row["electrical_power_w"] = round(new_power, 4)

        # 5. Recalculate cumulative energy

        cumulative_energy_wh = 0.0

        flight_data[0]["cumulative_energy_wh"] = 0.0

        for i in range(1, len(flight_data)):

            previous_row = flight_data[i - 1]

            current_row = flight_data[i]

            time_interval_s = (
                float(current_row["time_s"])
                - float(previous_row["time_s"])
            )

            previous_power = float(
                previous_row["electrical_power_w"]
            )

            current_power = float(
                current_row["electrical_power_w"]
            )

            average_power = (
                previous_power + current_power
            ) / 2

            energy_interval_wh = (
                average_power * time_interval_s / 3600
            )

            cumulative_energy_wh += energy_interval_wh

            current_row["cumulative_energy_wh"] = round(
                cumulative_energy_wh, 4
            )

        # 6. Recalculate estimated battery remaining

        for row in flight_data:

            energy_used = float(row["cumulative_energy_wh"])

            remaining_percentage = (
                (nominal_battery_energy_wh - energy_used)
                / nominal_battery_energy_wh
            ) * 100

            remaining_percentage = max(
                0.0, min(100.0, remaining_percentage)
            )

            row["estimated_battery_remaining_pct"] = round(
                remaining_percentage, 2
            )

        # 7. Save the modified dataset

        with open(
            output_file,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=column_names
            )

            writer.writeheader()

            writer.writerows(flight_data)

        # 8. Display experiment summary

        print("\n----- FLIGHT B DATASET CREATED -----")

        print("Original dataset:", input_file.name)

        print("New dataset:", output_file.name)

        print("Number of samples:", len(flight_data))

        print("Battery current increase: 15%")

        print("Battery voltage: unchanged")

        print("Airspeed: unchanged")

        print("Flight duration: unchanged")

        print(
            "New cumulative energy:",
            flight_data[-1]["cumulative_energy_wh"],
            "Wh"
        )

        print("\nFlight B dataset created successfully.")

        print("Reminder: this is a hypothetical sensitivity experiment.")
