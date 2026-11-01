import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from uav_calculations import (
    calculate_power,
    calculate_energy_wh,
    calculate_average_power
)


class TestUAVCalculations(unittest.TestCase):

    def test_calculate_power(self):
        result = calculate_power(24, 10)

        self.assertEqual(result, 240)

    def test_calculate_energy(self):
        power_values = [100, 100, 100]
        time_values = [0, 60, 120]

        result = calculate_energy_wh(
            power_values,
            time_values
        )

        self.assertAlmostEqual(result, 3.3333, places=3)

    def test_calculate_average_power(self):
        result = calculate_average_power(100, 3600)

        self.assertEqual(result, 100)

    def test_zero_duration(self):
        with self.assertRaises(ValueError):
            calculate_average_power(100, 0)


if __name__ == "__main__":
    unittest.main()
