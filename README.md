# Ghost in the Machine - Workshop Resources

Workshop resources for the "Ghost in the Machine" session at MSRIT FDP 2026. This repository contains n8n workflows, sample data, Python generators, and documentation for building AI agent swarms.

## Quick Start

### 1. Generate Sample Data

```bash
cd sample-data/generators
pip install -r requirements.txt

# Generate 3 days of telemetry data
python neel_telemetry.py --mode all --days 3 --output-dir ../

# Generate maintenance history
python maintenance_history.py --output-dir ../
```

### 2. Import n8n Workflows

1. Open your n8n instance
2. Go to **Settings** > **Import from file**
3. Import workflows from `n8n-workflows/`:
   - `01-drishti-monitor.json` - Basic monitoring
   - `07-complete-swarm.json` - Complete agent swarm

### 3. Test the Workflow

```bash
# Send test data to Drishti
curl -X POST http://localhost:5678/webhook/drishti-webhook \
  -H "Content-Type: application/json" \
  -d '{"sensors":{"vibration_rms":2.1,"temperature":72}}'
```

## Repository Structure

```
.
├── n8n-workflows/              # n8n workflow definitions
│   ├── 01-drishti-monitor.json # Basic monitoring workflow
│   └── 07-complete-swarm.json  # Complete agent swarm
│
├── sample-data/                # Data files
│   ├── generators/             # Python data generators
│   │   ├── neel_telemetry.py
│   │   ├── maintenance_history.py
│   │   └── requirements.txt
│   ├── neel_telemetry.csv      # Pre-generated telemetry (CSV)
│   ├── neel_telemetry.json     # Pre-generated telemetry (JSON)
│   └── maintenance_history.json # Equipment history
│
├── prompts/                    # AI agent system prompts
│   └── agent-prompts.md
│
├── diagrams/                   # Architecture diagrams
│   └── architecture.txt
│
├── docs/                       # Documentation
│   ├── setup-guide.md
│   └── workshop-overview.md
│
├── LICENSE                     # MIT License
└── README.md                   # This file
```

## AI Agent Swarm

The workshop demonstrates a coordinated swarm of AI agents:

| Agent | Role | Function |
|-------|------|----------|
| **Drishti** | Monitor | Observes telemetry, identifies anomalies |
| **Jibreel** | Detector | Classifies severity and type |
| **Athena** | Analyzer | Root cause analysis |
| **Vidhaata** | Scheduler | Plans maintenance |
| **Hermes** | Messenger | Delivers notifications |

## Requirements

- Python 3.9+
- numpy, pandas
- n8n instance (local or cloud)
- Optional: Slack workspace for notifications

## The Scenario

You are monitoring **Hydraulic Press Unit #7** at Shakti Heavy Industries. The equipment shows subtle signs of bearing degradation—patterns nearly invisible to manual inspection but detectable by AI agents working together.

**The Signal:** 2.3kHz harmonic drift indicating bearing wear, correlated with vibration increase and temperature rise.

## Documentation

- [Setup Guide](docs/setup-guide.md) - Installation and configuration
- [Workshop Overview](docs/workshop-overview.md) - Full workshop description
- [Agent Prompts](prompts/agent-prompts.md) - System prompt reference

## License

MIT License - See [LICENSE](LICENSE) for details.

---

*Part of the MSRIT FDP 2026 Workshop Series*
