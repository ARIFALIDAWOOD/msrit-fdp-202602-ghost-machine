# Gsheet exercises — Session 1

Manual data exploration in Google Sheets for **Session 1: A Practical Introduction to Telemetry and Diagnostics**.

## Purpose

Participants work through the same raw telemetry data (Hydraulic Press Unit #7) in a shared Google Sheet. The exercises are step-by-step so they experience why diagnosing failure from raw data is hard—setting up the “why we need agents” moment later in the session.

## Prerequisites

- **Data in a Google Sheet**: The Neel telemetry data is already uploaded to a Google Sheet (from the CSV).
- **Access**: Participants have view or edit access to that sheet, as decided by the facilitator.

## Session 1 exercises

| Document | Description |
|----------|-------------|
| [session-1-exercises.md](session-1-exercises.md) | Step-by-step instructions: data orientation → extract numbers → single metric → red herring → multi-metric → subtle vibration trend → maintenance context. |

## Maintenance tab

The last exercise refers to a **Maintenance** tab (or separate sheet). The facilitator should either:

- Add a second tab/sheet in the same workbook with the maintenance data, or  
- Use the spec and sample data in [session-1-maintenance-tab.md](session-1-maintenance-tab.md) to create it or hand it out.

## Data source (for facilitators)

- **CSV**: `backend/data/neel_telemetry.csv` in this repo (~6050 rows, 5-minute intervals, ~3 weeks).
- Columns: `timestamp`, `equipment_id`, `acoustic_db`, `flow_rate`, `motor_current`, `pressure`, `temperature`, `vibration_rms`. Sensor columns may contain values as text like `{'value': 75.096, 'unit': 'decibel'}`; the exercises include a step to extract the numeric value if needed.
