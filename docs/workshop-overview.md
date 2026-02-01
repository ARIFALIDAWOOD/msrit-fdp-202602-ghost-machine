# Workshop Overview: Ghost in the Machine

## About This Workshop

"Ghost in the Machine" is a hands-on workshop exploring AI agent orchestration in industrial settings. Participants learn to build autonomous AI agents that monitor factory telemetry, detect anomalies, and coordinate maintenance responses.

## The Scenario

You are tasked with monitoring **Hydraulic Press Unit #7** at Shakti Heavy Industries. The equipment has been showing subtle signs of bearing degradation - patterns that are nearly invisible to manual inspection but detectable by AI agents working together.

## Key Concepts

### AI Agent Swarm

The workshop introduces a coordinated swarm of specialized AI agents:

| Agent | Role | Responsibility |
|-------|------|----------------|
| **Drishti** | Monitor | Observes telemetry streams, identifies deviations |
| **Jibreel** | Detector | Classifies anomaly severity and type |
| **Athena** | Analyzer | Performs root cause analysis using historical data |
| **Vidhaata** | Scheduler | Plans maintenance actions based on analysis |
| **Hermes** | Messenger | Delivers notifications to stakeholders |

### The Signal in the Noise

The dataset contains a subtle bearing degradation pattern:
- **2.3kHz harmonic drift**: The critical indicator
- **Correlated vibration increase**: Secondary confirmation
- **Temperature rise**: Friction-related warming

These patterns are embedded in normal operational noise, requiring AI assistance to detect early.

## Workshop Sessions

### Session 1: Manual Analysis vs. AI Observation

1. Participants attempt manual CSV analysis
2. Discover the difficulty of pattern detection at scale
3. Introduction to Drishti monitoring agent
4. First automated anomaly detection

### Session 2: Building the Agent Swarm

1. Build detection and classification agents
2. Implement root cause analysis with historical data
3. Add scheduling and notification agents
4. Full swarm demonstration with live data

## Resources in This Repository

```
.
├── n8n-workflows/           # n8n workflow JSON files
│   ├── 01-drishti-monitor.json
│   └── 07-complete-swarm.json
├── sample-data/             # Pre-generated data files
│   ├── generators/          # Python scripts
│   └── *.csv, *.json        # Generated data
├── prompts/                 # Agent system prompts
├── diagrams/                # Architecture diagrams
└── docs/                    # Documentation
```

## Learning Outcomes

By the end of this workshop, participants will:

1. Understand AI agent orchestration patterns
2. Build workflows using n8n with AI nodes
3. Design effective agent prompts
4. Implement anomaly detection pipelines
5. Coordinate multi-agent systems for complex tasks

## Prerequisites

- Basic understanding of JSON and APIs
- Familiarity with workflow automation concepts
- No prior AI/ML experience required
