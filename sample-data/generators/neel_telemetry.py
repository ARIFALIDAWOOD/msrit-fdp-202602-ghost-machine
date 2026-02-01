#!/usr/bin/env python3
"""
GHOST IN THE MACHINE - Neel's Telemetry Generator
Generates 21 days of synthetic industrial sensor data with embedded failure signature
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
import argparse

class NeelTelemetryGenerator:
    """
    Generates realistic telemetry data for Hydraulic Press Unit #7
    with an embedded bearing degradation pattern.
    """

    def __init__(self, seed=42):
        np.random.seed(seed)
        self.equipment_id = "HYD_PRESS_07"
        self.location = "Assembly Line B"

        # Sensor baseline configurations
        self.sensors = {
            'vibration_rms': {
                'unit': 'mm/s',
                'baseline': 2.0,
                'noise_std': 0.15,
                'daily_pattern': True,  # Higher during shifts
            },
            'temperature': {
                'unit': 'celsius',
                'baseline': 72.0,
                'noise_std': 2.5,
                'daily_pattern': True,
            },
            'pressure': {
                'unit': 'bar',
                'baseline': 165.0,
                'noise_std': 5.0,
                'daily_pattern': False,
            },
            'motor_current': {
                'unit': 'ampere',
                'baseline': 13.2,
                'noise_std': 0.3,
                'daily_pattern': True,
            },
            'acoustic_db': {
                'unit': 'decibel',
                'baseline': 75.0,
                'noise_std': 1.5,
                'daily_pattern': True,
            },
            'flow_rate': {
                'unit': 'liters_per_min',
                'baseline': 48.5,
                'noise_std': 1.2,
                'daily_pattern': False,
            }
        }

        # Bearing degradation parameters
        self.degradation_start_day = 5  # Subtle signs begin
        self.critical_day = 21  # When failure would occur

    def _calculate_degradation_factor(self, day: int, hour: int) -> float:
        """
        Calculate the degradation factor based on day.
        Returns a multiplier that increases exponentially as we approach failure.
        """
        if day < self.degradation_start_day:
            return 0.0

        # Days since degradation started
        days_degrading = day - self.degradation_start_day
        total_degradation_days = self.critical_day - self.degradation_start_day

        # Exponential growth factor (subtle at first, accelerating)
        progress = days_degrading / total_degradation_days

        # S-curve: slow start, faster middle, plateaus near end
        factor = 1 / (1 + np.exp(-10 * (progress - 0.5)))

        return factor

    def _add_daily_pattern(self, base_value: float, hour: int) -> float:
        """
        Add realistic daily operational pattern.
        Higher values during work shifts (6AM-10PM), lower at night.
        """
        # Shift pattern: 6AM-2PM (morning), 2PM-10PM (evening), 10PM-6AM (night/maintenance)
        if 6 <= hour < 22:  # Active shifts
            shift_factor = 1.0 + 0.05 * np.sin(np.pi * (hour - 6) / 16)
        else:  # Night shift - reduced operation
            shift_factor = 0.85

        return base_value * shift_factor

    def _generate_vibration_harmonics(self, day: int, hour: int) -> dict:
        """
        Generate vibration harmonics data - the key diagnostic signal.
        Bearing degradation shows up in specific frequency bands.
        """
        degradation = self._calculate_degradation_factor(day, hour)

        # Normal harmonics at different frequencies
        harmonics = {
            'freq_1x': 0.8 + np.random.normal(0, 0.05),  # Fundamental
            'freq_2x': 0.4 + np.random.normal(0, 0.03),  # 2nd harmonic
            'freq_bearing': 0.2 + np.random.normal(0, 0.02),  # Bearing frequency
            'freq_2_3khz': 0.15 + np.random.normal(0, 0.01),  # High frequency band
        }

        # THE SIGNAL: Bearing degradation shows up in the 2.3kHz band
        # This is what Drishti needs to find!
        if degradation > 0:
            # Subtle drift that's hard to spot manually but significant
            harmonics['freq_2_3khz'] += degradation * 0.08  # 0.3% weekly drift
            harmonics['freq_bearing'] += degradation * 0.05

        return harmonics

    def generate_reading(self, timestamp: datetime) -> dict:
        """Generate a single sensor reading at the given timestamp."""

        # Use relative day calculation from start_date
        base_date = timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
        day = min(21, max(1, (timestamp - (timestamp - timedelta(days=20))).days % 21 + 1))
        hour = timestamp.hour

        degradation = self._calculate_degradation_factor(day, hour)

        reading = {
            'timestamp': timestamp.isoformat(),
            'equipment_id': self.equipment_id,
            'location': self.location,
            'day_of_test': day,
            'sensors': {},
            'harmonics': self._generate_vibration_harmonics(day, hour),
            'metadata': {
                'shift': 'morning' if 6 <= hour < 14 else ('evening' if 14 <= hour < 22 else 'night'),
                'operator_id': f"OP_{(day % 3) + 1:03d}",
            }
        }

        for sensor_name, config in self.sensors.items():
            base = config['baseline']
            noise = np.random.normal(0, config['noise_std'])

            # Add daily pattern if applicable
            if config['daily_pattern']:
                base = self._add_daily_pattern(base, hour)

            # Add degradation effects
            if sensor_name == 'vibration_rms':
                # Primary degradation indicator
                degradation_effect = degradation * 0.4  # Up to 20% increase
            elif sensor_name == 'motor_current':
                # Secondary indicator - motor works harder
                degradation_effect = degradation * 0.3
            elif sensor_name == 'temperature':
                # Correlated with vibration (friction heat)
                degradation_effect = degradation * 2.0
            elif sensor_name == 'acoustic_db':
                # Bearing noise
                degradation_effect = degradation * 3.0
            elif sensor_name == 'flow_rate':
                # Slight decrease as efficiency drops
                degradation_effect = -degradation * 2.0
            else:
                degradation_effect = 0

            value = base + noise + degradation_effect

            reading['sensors'][sensor_name] = {
                'value': round(value, 3),
                'unit': config['unit'],
            }

        # Add some realistic anomalies (red herrings)
        if day == 12 and 10 <= hour <= 14:
            # Temperature spike due to ambient conditions (NOT the real issue)
            reading['sensors']['temperature']['value'] += 8.0
            reading['metadata']['note'] = 'Ambient temperature elevated - HVAC maintenance'

        return reading

    def generate_dataset(self,
                         start_date: datetime = None,
                         days: int = 21,
                         readings_per_hour: int = 12) -> list:
        """
        Generate complete dataset for the workshop.

        Args:
            start_date: Starting timestamp (defaults to N days ago)
            days: Number of days to generate
            readings_per_hour: Sensor reading frequency (12 = every 5 minutes)

        Returns:
            List of all readings
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=days)

        readings = []
        current_time = start_date
        end_time = start_date + timedelta(days=days)

        interval_minutes = 60 // readings_per_hour

        while current_time < end_time:
            reading = self.generate_reading(current_time)
            # Override day_of_test with actual sequential day
            reading['day_of_test'] = (current_time - start_date).days + 1
            readings.append(reading)
            current_time += timedelta(minutes=interval_minutes)

        return readings

    def export_csv(self, readings: list, filename: str = 'neel_telemetry.csv'):
        """Export to CSV format for manual analysis exercise."""

        flat_data = []
        for r in readings:
            row = {
                'timestamp': r['timestamp'],
                'equipment_id': r['equipment_id'],
                'day': r['day_of_test'],
                'shift': r['metadata']['shift'],
            }
            # Flatten sensors
            for sensor, data in r['sensors'].items():
                row[sensor] = data['value']
            # Flatten harmonics
            for harmonic, value in r['harmonics'].items():
                row[f'harmonic_{harmonic}'] = round(value, 4)

            flat_data.append(row)

        df = pd.DataFrame(flat_data)
        df.to_csv(filename, index=False)
        print(f"Exported {len(flat_data)} readings to {filename}")
        return df

    def export_json(self, readings: list, filename: str = 'neel_telemetry.json'):
        """Export to JSON format for n8n ingestion."""
        with open(filename, 'w') as f:
            json.dump(readings, f, indent=2)
        print(f"Exported {len(readings)} readings to {filename}")


def main():
    parser = argparse.ArgumentParser(description="Generate Neel's telemetry data")
    parser.add_argument('--mode', choices=['csv', 'json', 'all'],
                        default='all', help='Output mode')
    parser.add_argument('--days', type=int, default=21, help='Days of data')
    parser.add_argument('--output-dir', default='.', help='Output directory')

    args = parser.parse_args()

    generator = NeelTelemetryGenerator()

    print("Generating static dataset...")
    readings = generator.generate_dataset(days=args.days)

    import os
    os.makedirs(args.output_dir, exist_ok=True)

    if args.mode in ['csv', 'all']:
        generator.export_csv(readings, f'{args.output_dir}/neel_telemetry.csv')

    if args.mode in ['json', 'all']:
        generator.export_json(readings, f'{args.output_dir}/neel_telemetry.json')


if __name__ == '__main__':
    main()
