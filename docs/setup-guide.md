# Setup Guide

This guide explains how to use the workshop resources in this repository.

## Requirements

- Python 3.9 or higher
- pip or uv for package management
- n8n instance (local or cloud) for workflow import

## Installing Python Dependencies

```bash
cd sample-data/generators
pip install -r requirements.txt
```

Or with uv:

```bash
cd sample-data/generators
uv pip install -r requirements.txt
```

## Running the Data Generators

### Generate Telemetry Data (CSV)

```bash
python neel_telemetry.py --mode csv --days 3 --output-dir ../
```

### Generate Telemetry Data (JSON)

```bash
python neel_telemetry.py --mode json --days 3 --output-dir ../
```

### Generate Both Formats

```bash
python neel_telemetry.py --mode all --days 21 --output-dir ../
```

### Generate Maintenance History

```bash
python maintenance_history.py --output-dir ../
```

## Importing n8n Workflows

1. Open your n8n instance
2. Go to **Settings** > **Import from file**
3. Select the workflow JSON file from `n8n-workflows/`:
   - `01-drishti-monitor.json` - Basic monitoring workflow
   - `07-complete-swarm.json` - Full agent swarm workflow
4. Configure credentials:
   - Set up any required API credentials (Slack, etc.)
   - Configure InfluxDB connection if using live data

## Workflow Overview

### 01-drishti-monitor.json

The Drishti monitoring workflow:
- Receives sensor data via webhook
- Analyzes readings using an AI agent
- Checks for critical severity levels
- Sends alerts for anomalies

**Webhook endpoint:** `POST /webhook/drishti-webhook`

### 07-complete-swarm.json

The complete agent swarm workflow with:
- **Drishti** - Monitoring agent
- **Jibreel** - Anomaly classification
- **Athena** - Root cause analysis
- **Vidhaata** - Maintenance scheduling
- **Hermes** - Notification delivery

**Webhook endpoint:** `POST /webhook/factory-telemetry`

## Testing the Setup

1. Generate sample data:
   ```bash
   python neel_telemetry.py --mode json --days 1 --output-dir ../
   ```

2. Send a test reading to n8n:
   ```bash
   curl -X POST http://localhost:5678/webhook/drishti-webhook \
     -H "Content-Type: application/json" \
     -d @../neel_telemetry.json
   ```

## Troubleshooting

### Python errors

Make sure you have the required packages installed:
```bash
pip install numpy pandas
```

### n8n workflow errors

- Check that all nodes are properly connected
- Verify API credentials are configured
- Check the n8n execution logs for detailed errors
