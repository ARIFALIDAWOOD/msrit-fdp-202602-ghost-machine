#!/usr/bin/env python3
"""
Generate maintenance history that Athena will reference for root cause analysis.
"""

import json
from datetime import datetime, timedelta
import argparse


def generate_maintenance_history():
    """Generate realistic maintenance records for Unit #7."""

    base_date = datetime.now()

    records = [
        {
            "record_id": "MNT-2021-0342",
            "equipment_id": "HYD_PRESS_07",
            "date": (base_date - timedelta(days=847)).isoformat(),
            "type": "preventive",
            "description": "Main spindle bearing replacement",
            "parts_replaced": ["SKF 6205-2RS bearing", "Seal kit"],
            "technician": "Ramesh Kumar",
            "downtime_hours": 6,
            "notes": "Manufacturer recommended replacement at 15,000 operating hours or 900 days"
        },
        {
            "record_id": "MNT-2022-0156",
            "equipment_id": "HYD_PRESS_07",
            "date": (base_date - timedelta(days=540)).isoformat(),
            "type": "corrective",
            "description": "Hydraulic line leak repair",
            "parts_replaced": ["High-pressure hose assembly"],
            "technician": "Suresh Patel",
            "downtime_hours": 2,
            "notes": "Routine wear, no underlying issues"
        },
        {
            "record_id": "MNT-2023-0089",
            "equipment_id": "HYD_PRESS_07",
            "date": (base_date - timedelta(days=365)).isoformat(),
            "type": "preventive",
            "description": "Annual inspection and lubrication",
            "parts_replaced": [],
            "technician": "Ramesh Kumar",
            "downtime_hours": 4,
            "notes": "All parameters within spec. Bearing wear at 65% of expected life."
        },
        {
            "record_id": "MNT-2023-0412",
            "equipment_id": "HYD_PRESS_04",  # Different unit - the precedent!
            "date": (base_date - timedelta(days=180)).isoformat(),
            "type": "emergency",
            "description": "Catastrophic bearing failure - main spindle",
            "parts_replaced": ["SKF 6205-2RS bearing", "Spindle shaft", "Motor coupling"],
            "technician": "Emergency Response Team",
            "downtime_hours": 72,
            "notes": "CRITICAL INCIDENT: Bearing failure caused shaft damage. Root cause: missed warning signs in vibration data - 2.3kHz harmonic drift detected in post-analysis. Recommend enhanced monitoring."
        },
        {
            "record_id": "MNT-2024-0023",
            "equipment_id": "HYD_PRESS_07",
            "date": (base_date - timedelta(days=45)).isoformat(),
            "type": "preventive",
            "description": "Quarterly filter replacement",
            "parts_replaced": ["Hydraulic filter element"],
            "technician": "Suresh Patel",
            "downtime_hours": 1,
            "notes": "Standard maintenance"
        }
    ]

    # Equipment specs
    equipment_specs = {
        "equipment_id": "HYD_PRESS_07",
        "manufacturer": "Shakti Heavy Industries",
        "model": "HP-500T",
        "installation_date": "2018-03-15",
        "specifications": {
            "bearing_type": "SKF 6205-2RS",
            "bearing_mtbf_days": 900,
            "bearing_mtbf_hours": 15000,
            "normal_vibration_rms": {"min": 1.5, "max": 2.5, "unit": "mm/s"},
            "normal_temperature": {"min": 60, "max": 85, "unit": "celsius"},
            "normal_pressure": {"min": 150, "max": 180, "unit": "bar"},
            "warning_thresholds": {
                "vibration_2_3khz_drift": 0.05,  # Per week
                "temperature_deviation": 10,
                "current_increase_percent": 5
            }
        },
        "current_operating_hours": 12450,
        "last_bearing_replacement_hours": 11600
    }

    # Failure signatures for pattern matching
    failure_signatures = [
        {
            "signature_id": "SIG-001",
            "failure_type": "bearing_degradation",
            "equipment_type": "hydraulic_press",
            "indicators": [
                {"metric": "harmonic_freq_2_3khz", "pattern": "increasing_drift", "threshold": 0.003, "per": "day"},
                {"metric": "motor_current", "pattern": "correlated_increase", "threshold": 0.02, "per": "day"},
                {"metric": "vibration_rms", "pattern": "gradual_increase", "threshold": 0.01, "per": "day"}
            ],
            "time_to_failure_days": {"min": 14, "max": 30},
            "confidence_weight": 0.85,
            "source": "Post-incident analysis MNT-2023-0412"
        }
    ]

    return {
        "maintenance_records": records,
        "equipment_specs": equipment_specs,
        "failure_signatures": failure_signatures
    }


def main():
    parser = argparse.ArgumentParser(description="Generate maintenance history data")
    parser.add_argument('--output-dir', default='.', help='Output directory')

    args = parser.parse_args()

    data = generate_maintenance_history()

    import os
    os.makedirs(args.output_dir, exist_ok=True)

    output_file = f'{args.output_dir}/maintenance_history.json'
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Generated {output_file}")


if __name__ == '__main__':
    main()
