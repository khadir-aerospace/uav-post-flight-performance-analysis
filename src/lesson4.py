
# UAV Flight Performance Analyst
# Version 5: Range, Energy and Efficiency Comparison


# 1. Calculate estimated flight range
def calculate_range(airspeed_kmh, flight_time_hours):
    flight_range_km = airspeed_kmh * flight_time_hours
    return flight_range_km


# 2. Calculate electrical power and energy
def calculate_energy(voltage_v, current_a, flight_time_hours):
    power_w = voltage_v * current_a
    energy_wh = power_w * flight_time_hours
    return power_w, energy_wh


# 3. Calculate energy consumed per kilometre
def calculate_energy_per_km(energy_wh, flight_range_km):
    if flight_range_km <= 0:
        return None

    energy_per_km = energy_wh / flight_range_km
    return energy_per_km


# 4. Validate positive numeric input
def get_positive_number(prompt):
    while True:
        try:
            value = float(input(prompt))

            if value > 0:
                return value
            else:
                print("Enter a number greater than zero.")

        except ValueError:
            print("Invalid input. Enter a number.")


# 5. Ask how many scenarios to compare
while True:
    try:
        number_of_scenarios = int(
            input("How many scenarios do you want to compare? ")
        )

        if number_of_scenarios > 0:
            break
        else:
            print("Enter at least 1 scenario.")

    except ValueError:
        print("Enter a whole number, such as 3.")


# 6. Collect data and calculate results
scenarios = []

for i in range(number_of_scenarios):
    print("\nEnter details for Scenario", i + 1)

    airspeed_kmh = get_positive_number(
        "Enter airspeed (km/h): "
    )

    flight_time_hours = get_positive_number(
        "Enter flight duration (hours): "
    )

    voltage_v = get_positive_number(
        "Enter average battery voltage (V): "
    )

    current_a = get_positive_number(
        "Enter average current (A): "
    )

    flight_range_km = calculate_range(
        airspeed_kmh, flight_time_hours
    )

    power_w, energy_wh = calculate_energy(
        voltage_v, current_a, flight_time_hours
    )

    energy_per_km = calculate_energy_per_km(
        energy_wh, flight_range_km
    )

    scenarios.append([
        i + 1,
        airspeed_kmh,
        flight_time_hours,
        flight_range_km,
        voltage_v,
        current_a,
        power_w,
        energy_wh,
        energy_per_km
    ])


# 7. Display the comparison table
print("\n" + "=" * 112)
print("UAV FLIGHT PERFORMANCE COMPARISON")
print("=" * 112)

print(
    "{:<10} {:>12} {:>12} {:>14} {:>12} {:>14} {:>14} {:>16}".format(
        "Scenario",
        "Speed km/h",
        "Time h",
        "Range km",
        "Power W",
        "Energy Wh",
        "Voltage V",
        "Energy Wh/km"
    )
)

print("-" * 112)

for scenario in scenarios:
    print(
        "{:<10} {:>12.1f} {:>12.2f} {:>14.1f} {:>12.1f} {:>14.1f} {:>14.1f} {:>16.2f}".format(
            scenario[0],
            scenario[1],
            scenario[2],
            scenario[3],
            scenario[6],
            scenario[7],
            scenario[4],
            scenario[8]
        )
    )

print("=" * 112)


# 8. Display detailed results
print("\nDETAILED SCENARIO RESULTS")

for scenario in scenarios:
    print("\nScenario", scenario[0])
    print("Airspeed:", scenario[1], "km/h")
    print("Duration:", scenario[2], "hours")
    print("Estimated range:", scenario[3], "km")
    print("Battery voltage:", scenario[4], "V")
    print("Average current:", scenario[5], "A")
    print("Electrical power:", scenario[6], "W")
    print("Estimated energy consumption:", scenario[7], "Wh")
    print("Energy per kilometre:", scenario[8], "Wh/km")

print("\nAnalysis completed successfully.")
print("Note: These results use simplified constant-speed and constant-power assumptions.")

