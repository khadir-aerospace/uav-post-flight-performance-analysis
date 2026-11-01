
# UAV Performance Analyst
# Lesson 12: Flight Performance Comparison
#
# Baseline vs illustrative higher-power scenario
# Scenario B is a mathematical sensitivity exercise,
# NOT a validated aircraft performance prediction.

import csv
from pathlib import Path
import matplotlib.pyplot as plt


# 1. Load the baseline flight dataset

project_folder = Path(__file__).resolve().parents[1] / "data"
csv_file = project_folder / "hypothetical_fixed_wing_flight.csv"

if not csv_file.exists():
    print("ERROR: Dataset not found.")
    print("Expected location:", csv_file)

else:
    with open(csv_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        flight_data = list(reader)

    if not flight_data:
        print("ERROR: Dataset is empty.")

    else:
        # 2. Convert required measurements to numbers

        for row in flight_data:
            row["time_s"] = float(row["time_s"])
            row["battery_voltage_v"] = float(row["battery_voltage_v"])
            row["battery_current_a"] = float(row["battery_current_a"])
            row["electrical_power_w"] = float(row["electrical_power_w"])
            row["airspeed_m_s"] = float(row["airspeed_m_s"])

        # 3. Define the comparison scenarios

        power_increase_factor = 1.10

        baseline_power = [
            row["electrical_power_w"] for row in flight_data
        ]

        scenario_b_power = [
            power * power_increase_factor
            for power in baseline_power
        ]

        # 4. Calculate energy for each scenario

        baseline_energy_wh = 0.0
        scenario_b_energy_wh = 0.0

        for i in range(1, len(flight_data)):

            time_interval_s = (
                flight_data[i]["time_s"]
                - flight_data[i - 1]["time_s"]
            )

            baseline_average_power = (
                baseline_power[i - 1] + baseline_power[i]
            ) / 2

            scenario_b_average_power = (
                scenario_b_power[i - 1] + scenario_b_power[i]
            ) / 2

            baseline_energy_wh += (
                baseline_average_power * time_interval_s / 3600
            )

            scenario_b_energy_wh += (
                scenario_b_average_power * time_interval_s / 3600
            )

        # 5. Calculate average and maximum power

        baseline_average_power = sum(baseline_power) / len(baseline_power)
        scenario_b_average_power = sum(scenario_b_power) / len(scenario_b_power)

        baseline_maximum_power = max(baseline_power)
        scenario_b_maximum_power = max(scenario_b_power)

        # 6. Calculate comparison differences

        energy_difference_wh = (
            scenario_b_energy_wh - baseline_energy_wh
        )

        energy_difference_percentage = (
            energy_difference_wh / baseline_energy_wh * 100
        )

        average_power_difference = (
            scenario_b_average_power - baseline_average_power
        )

        # 7. Display comparison results

        print("\n----- UAV FLIGHT PERFORMANCE COMPARISON -----")

        print("\nBASELINE FLIGHT")
        print("Total energy:",
              round(baseline_energy_wh, 2), "Wh")
        print("Average power:",
              round(baseline_average_power, 2), "W")
        print("Maximum power:",
              round(baseline_maximum_power, 2), "W")

        print("\nSCENARIO B: 10% HIGHER POWER")
        print("Total energy:",
              round(scenario_b_energy_wh, 2), "Wh")
        print("Average power:",
              round(scenario_b_average_power, 2), "W")
        print("Maximum power:",
              round(scenario_b_maximum_power, 2), "W")

        print("\n----- DIFFERENCE -----")
        print("Additional energy:",
              round(energy_difference_wh, 2), "Wh")
        print("Energy increase:",
              round(energy_difference_percentage, 2), "%")
        print("Additional average power:",
              round(average_power_difference, 2), "W")

        # 8. Prepare chart data

        time_min = [
            row["time_s"] / 60 for row in flight_data
        ]

        # 9. Plot power comparison

        plt.figure(figsize=(10, 5))

        plt.plot(
            time_min,
            baseline_power,
            label="Baseline"
        )

        plt.plot(
            time_min,
            scenario_b_power,
            label="Scenario B: 10% higher power"
        )

        plt.xlabel("Time (minutes)")
        plt.ylabel("Electrical power (W)")
        plt.title("UAV Electrical Power Comparison")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # 10. Plot energy comparison

        scenario_labels = [
            "Baseline",
            "Scenario B"
        ]

        energy_values = [
            baseline_energy_wh,
            scenario_b_energy_wh
        ]

        plt.figure(figsize=(8, 5))
        plt.bar(scenario_labels, energy_values)
        plt.ylabel("Total energy (Wh)")
        plt.title("UAV Total Energy Comparison")
        plt.grid(axis="y")
        plt.tight_layout()

        # 11. Display charts

        print("\nComparison completed.")
        print("Scenario B is illustrative, not a validated flight prediction.")

        plt.show()
