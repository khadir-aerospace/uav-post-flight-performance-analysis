# Preliminary Engineering Technical Report
## UAV Post-Flight Performance Analysis Platform

**Report status:** Preliminary educational analysis  
**Data basis:** Supplied hypothetical synthetic teaching datasets  
**Verification:** Analysis programs and unit tests rerun for this report

## 1. Project Overview

The UAV Post-Flight Performance Analysis Platform is a Python project for examining electrical and basic flight-performance fields in two hypothetical fixed-wing UAV datasets. It calculates power and energy, summarizes energy by flight phase, compares a baseline with a modified dataset, and plots selected time histories.

The main analysis is implemented in [`uav_flight_analysis.py`](../src/uav_flight_analysis.py). Dataset comparison is provided by [`flight comparison.py`](../src/flight%20comparison.py), while [`uav_flight_comparison.py`](../src/uav_flight_comparison.py) performs a separate power-scaling sensitivity exercise. The shared calculation helpers are in [`uav_calculations.py`](../src/uav_calculations.py).

This report is preliminary and educational. Neither the datasets nor the calculations constitute validated aircraft performance evidence.

## 2. Engineering Objectives

The project aims to:

- Calculate electrical power from voltage and current samples.
- Estimate energy use over the recorded interval using numerical integration.
- Summarize mean and maximum electrical power and total energy.
- Attribute estimated energy use to labeled flight phases.
- Compare baseline data with an illustrative modified-current dataset and a separate power sensitivity case.
- Check basic dataset consistency and exercise calculation helpers with unit tests.

## 3. Dataset Description

Both CSV files contain 1,201 rows and 11 columns. Time spans 0 to 1,200 seconds, sampled at one-second intervals. The fields include time, flight phase, airspeed, groundspeed, altitude, battery voltage, battery current, supplied electrical power, cumulative energy, and estimated battery remaining.

| Dataset | Samples | Time span | Sample interval | Role in the project |
|---|---:|---:|---:|---|
| `hypothetical_fixed_wing_flight.csv` | 1,201 | 0-1,200 s (20 min) | 1 s | Flight A baseline |
| `hypothetical_fixed_wing_flight_B.csv` | 1,201 | 0-1,200 s (20 min) | 1 s | Flight B, illustrative 15% higher-current dataset |

The phase labels are `takeoff_climb`, `climb`, `cruise`, `descent`, and `landing`. In the supplied Flight B data, voltage, airspeed, and duration remain the same as Flight A while current, power, and cumulative energy are higher.

## 4. Assumptions and Synthetic-Data Disclaimer

**The datasets are hypothetical synthetic teaching data, not measurements from a real aircraft.** Their plausible-looking values do not establish that the data represent an actual flight, aircraft, battery, or propulsion system.

The calculations treat the recorded voltage and current as usable electrical inputs, accept the recorded time and phase labels, and use the dataset's sampling interval for integration. Scenario comparisons hold the stated non-scaled values constant. The `estimated_battery_remaining_pct` field is a synthetic linear bookkeeping value based on a nominal 222 Wh capacity, clipped to 0-100%; it is not a real-world battery state-of-charge estimate.

No result in this report is a validated aircraft performance prediction, fault diagnosis, or real-world battery prediction.

## 5. Engineering Methodology

### Electrical power

For each sample, electrical power is calculated as

$$P_i = V_i I_i$$

where voltage $V_i$ is in volts, current $I_i$ is in amperes, and power $P_i$ is in watts. Power is the instantaneous rate of electrical energy use. It describes how quickly energy is being used at a sample; it is not the accumulated amount used over the flight.

### Energy by trapezoidal integration

Between adjacent samples, the code approximates power as varying linearly and uses the trapezoidal rule:

$$\Delta E_i = \frac{P_i + P_{i+1}}{2} \frac{t_{i+1}-t_i}{3600}$$

Here, time is in seconds and the result is in watt-hours (Wh). Total energy is the sum of the interval contributions:

$$E_{total} = \sum_i \Delta E_i$$

Energy is the accumulated electrical use over time; the same power level sustained for longer produces more energy consumption.

### Average power

The main analysis calculates average power from integrated energy divided by elapsed time:

$$P_{avg} = \frac{E_{total}}{T_{hours}}$$

The comparison programs also report the arithmetic mean of the sample power values. These averaging methods are close but not identical: the energy-based average is time-integrated over the elapsed interval, while a sample mean weights each listed sample equally.

### Energy by flight phase

The analysis integrates each interval and assigns it to the phase label on the interval's preceding sample. For each phase it reports interval duration, summed energy, mean interval power, and share of the integrated total. This is a label-based allocation over the synthetic data, not an independent assessment of actual flight dynamics.

## 6. Baseline Flight A Results

The baseline analysis was rerun against the supplied Flight A CSV. It reported 1,201 samples over 20 minutes, with no missing cells and no unexpected timestamp intervals.

| Metric | Flight A result |
|---|---:|
| Mean airspeed | 16.07 m/s |
| Mean battery voltage | 24.47 V |
| Minimum / maximum battery voltage | 24.26 / 24.74 V |
| Mean battery current | 9.41 A |
| Maximum battery current | 20.63 A |
| Mean power, energy divided by elapsed time | 230.61 W |
| Maximum recalculated power | 509.18 W |
| Integrated total energy | 76.87 Wh |
| Flight duration | 20.00 min |

Recalculated $V I$ power differed from the supplied power column by at most 0.0218 W. The integrated energy differed from the supplied final cumulative-energy value by 0.0005 Wh. These are checks of numerical consistency within this dataset, not validation of physical accuracy.

## 7. Energy Consumption by Flight Phase

| Flight phase | Duration | Mean interval power | Energy | Share of total energy |
|---|---:|---:|---:|---:|
| Takeoff/climb | 1.00 min | 488.28 W | 8.14 Wh | 10.59% |
| Climb | 3.00 min | 349.10 W | 17.46 Wh | 22.71% |
| Cruise | 11.00 min | 217.95 W | 39.96 Wh | 51.98% |
| Descent | 3.00 min | 150.09 W | 7.50 Wh | 9.76% |
| Landing | 2.00 min | 114.45 W | 3.82 Wh | 4.96% |

Values are rounded as printed by the analysis program, so displayed phase energies and shares may not sum exactly to the displayed total and 100%.

Cruise has the greatest total energy because it lasts much longer than the other phases. Energy depends on both power and time: takeoff/climb has a much higher mean interval power, but lasts about one minute; cruise averages a lower power for about eleven minutes. Consequently, the integrated cruise energy is 39.96 Wh versus 8.14 Wh for takeoff/climb. A higher peak or average power over a short period does not necessarily mean greater total energy than a lower power sustained over a longer period.

## 8. Flight A Versus Flight B Comparison

The existing Flight B CSV is the illustrative dataset produced by the project generator's 15% increase to battery current. The comparison program calculates power from voltage and current and integrates each dataset over its 20-minute duration.

| Metric | Flight A | Flight B | Difference (B - A) |
|---|---:|---:|---:|
| Duration | 20.00 min | 20.00 min | 0.00 min |
| Mean airspeed | 16.07 m/s | 16.07 m/s | 0.00 m/s |
| Mean power (sample mean) | 230.66 W | 265.26 W | +34.60 W (+15.0%) |
| Maximum power | 509.18 W | 585.56 W | +76.38 W (+15.0%) |
| Integrated total energy | 76.87 Wh | 88.40 Wh | +11.53 Wh (+15.0%) |

These are the comparison program's outputs for the supplied CSVs. The current increase is a constructed sensitivity change with other listed flight quantities held fixed; it does not demonstrate how an aircraft would respond to a real current change.

## 9. Separate 10% Higher-Power Sensitivity Experiment

A different program, `uav_flight_comparison.py`, takes the baseline power series and multiplies it by 1.10. This is a direct power scaling, not the Flight B dataset and not the 15% current modification.

| Metric | Baseline | 10% higher-power case | Difference |
|---|---:|---:|---:|
| Mean power (sample mean) | 230.66 W | 253.73 W | +23.07 W |
| Maximum power | 509.17 W | 560.09 W | +50.92 W |
| Integrated energy | 76.87 Wh | 84.56 Wh | +7.69 Wh (+10.0%) |
| Duration | 20.00 min | 20.00 min | 0.00 min |

The program reports a 10% energy increase because it scales the power profile by 10% while keeping the same time history. This describes the arithmetic sensitivity case only; no aircraft or battery response is modeled.

## 10. Software Testing and Verification

The automated test suite was rerun with `python -m unittest discover -s tests -v`: all four tests passed. They cover power calculation, trapezoidal energy calculation, average power, and rejection of zero duration in the average-power helper.

The baseline analysis and both comparison programs were also rerun using the noninteractive Matplotlib `Agg` backend. Each completed its calculations and printed results. The plots were constructed but not displayed interactively. The analysis checks reported zero missing cells and zero non-one-second intervals; the power and cumulative-energy differences are reported in Section 6.

The tests exercise the calculation helpers. They do not establish physical-model validity and do not comprehensively test malformed CSVs, plot appearance, scenario assumptions, or battery behavior.

## 11. Engineering Interpretation of Results

The outputs illustrate the difference between power and energy: Flight A reaches about 509 W at its highest calculated sample, while its total integrated electrical use over the 20-minute dataset is 76.87 Wh. The peak power indicates the highest rate in the data; total energy accounts for the rate across the full duration.

The phase results show why duration matters. Cruise contributes the largest share of total energy even though its mean interval power is substantially below takeoff/climb, because it occupies the longest phase interval. The constructed Flight B and 10% sensitivity cases also show that scaling current or power scales calculated power and integrated energy when the time history and other inputs are held fixed. This is a mathematical consequence of the setup, not evidence that real aircraft performance changes linearly in this way.

## 12. Limitations

- The inputs are synthetic and provide no evidence about a real vehicle or flight.
- The analysis uses $P=VI$ and does not model electrical conversion losses, wiring losses, motor/propeller efficiency, sensor calibration, uncertainty, or transient measurement effects.
- Trapezoidal integration assumes power changes linearly between adjacent samples. Results inherit the resolution, rounding, and quality of the input data.
- Phase energy depends on the supplied phase labels and the code's preceding-sample interval assignment; phase-boundary treatment is simplified.
- The comparison experiments hold duration and other flight quantities fixed. They do not recalculate aerodynamics, propulsion, trajectory, control response, or achievable endurance.
- The 222 Wh battery-energy assumption and linear remaining-energy field do not model electrochemical state of charge, voltage sag, temperature, aging, discharge limits, or uncertainty. No real-world battery prediction is supported.
- Basic data consistency checks and four helper tests do not amount to aircraft model validation, operational safety evidence, or fault-detection capability.

## 13. Future Development

Potential next steps, while retaining a clear boundary between teaching examples and validated analysis, include:

- Add automated tests for CSV schema, timestamp integrity, phase allocation, and expected end-to-end results.
- Separate data loading, metric calculation, and plotting into reusable functions with explicit units and input validation.
- Save plots and machine-readable result summaries into `reports/` with dataset identifiers and run metadata.
- Add uncertainty and sensitivity reporting once defensible uncertainty inputs are available.
- If real measurements are introduced, document provenance, sensor calibration, synchronization, and quality controls, and compare the methods against an independently validated reference before making engineering claims.
- Treat any battery state-of-charge or fault-detection capability as a separately specified and validated development effort, not an extension implied by the current calculations.

## 14. Conclusion

The platform successfully calculates and compares electrical metrics for its supplied hypothetical synthetic teaching datasets. The verified baseline result is 76.87 Wh over 20 minutes; the phase breakdown assigns 39.96 Wh to cruise and 8.14 Wh to takeoff/climb. The supplied Flight B comparison reports 88.40 Wh after its constructed 15% current increase, while the separate 10% higher-power experiment reports 84.56 Wh.

These figures demonstrate basic power, integration, and comparison methods only. They are not validated aircraft performance, fault diagnosis, or real-world battery predictions.
