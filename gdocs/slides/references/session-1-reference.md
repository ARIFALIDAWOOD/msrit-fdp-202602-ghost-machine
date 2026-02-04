# Session 1: The Discovery - Complete Reference Document

## For NotebookLM & Google Slides Preparation

---

## LEARNING OUTCOMES

By the end of Session 1, participants will be able to:

1. **Define telemetry** and explain its role in industrial monitoring
2. **Identify key components** of a telemetry pipeline (sensors → collection → storage → visualization)
3. **Interpret time-series data** and identify patterns indicating equipment health
4. **Understand the manual diagnosis challenge** that traditional monitoring presents
5. **Recognize why AI agents** are needed for proactive maintenance
6. **Configure basic OpenTelemetry** concepts for data collection

---

## NEEL'S STORY: THE NARRATIVE THREAD

### The Setup
Neelakantha (Neel) is a 34-year-old factory worker at Shakti Heavy Industries in Bhopal. He operates the Hydraulic Press Machine 7 (HYD_PRESS_07), which has been in service for 8 years. He's married with two children and is the primary earner for his family.

### The Problem
Three weeks ago, a bearing in Neel's machine began to degrade. The telemetry data tells the story:

- **Week 1**: Subtle harmonic frequency drift (0.5% from baseline)
- **Week 2**: Motor current increases by 3%
- **Week 3**: Temperature rises by 2°C, vibration anomalies appear
- **Day 21**: Catastrophic failure during operation, resulting in injury

### The Tragedy
The machine experienced a catastrophic bearing failure. Flying debris injured Neel's hand, requiring surgery. He will be unable to work for 6 months. His family faces financial hardship.

### The Twist
All the warning signs were in the data. The telemetry showed:
- Harmonics drifting as early as Day 3
- Current patterns changing by Day 10
- Temperature anomalies by Day 14

**But no one was watching.** The factory's monitoring system had over 500 sensors, 2,000+ alarms per day, and only 3 operators trying to make sense of it all.

### The Mission
This workshop challenges participants to build an AI agent system that could have saved Neel - detecting the bearing degradation pattern weeks before failure and alerting the right people at the right time.

---

## TELEMETRY FUNDAMENTALS

### What is Telemetry?
**Definition**: The automated collection, transmission, and analysis of data from remote sources.

In industrial settings, telemetry includes:
- **Sensors**: Physical devices measuring temperature, pressure, vibration, current, etc.
- **Protocols**: Communication standards (Modbus, OPC-UA, MQTT)
- **Time-series databases**: Specialized storage for timestamp-indexed data
- **Visualization**: Dashboards showing trends and anomalies

### Key Metrics for Equipment Health

| Metric | What It Measures | Normal Range | Warning Signs |
|--------|------------------|--------------|---------------|
| **Temperature** | Heat generation | 45-75°C | Sudden rises, gradual drift |
| **Vibration** | Mechanical balance | 0.1-2.0 mm/s | High frequency spikes |
| **Motor Current** | Power consumption | ±5% of baseline | Gradual increase |
| **Harmonics** | Frequency components | <0.15 of fundamental | Drift from baseline |
| **Pressure** | System load | Process-specific | Fluctuations, drops |
| **Sound/Acoustic** | Mechanical noise | Baseline profile | New frequencies |

### The Telemetry Pipeline

```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│   SENSORS   │──▶│ COLLECTION  │──▶│   STORAGE   │──▶│ VISUALIZATION│
│  (Field)    │   │ (Protocols) │   │ (Database)  │   │ (Dashboards) │
└─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘
                                           │
                                           ▼
                                    ┌─────────────┐
                                    │  ANALYSIS   │
                                    │  (AI/Rules) │
                                    └─────────────┘
```

---

## INFLUXDB & TIME-SERIES DATA

### Why Time-Series Databases?

Traditional databases are designed for:
- Point-in-time queries ("What is the current temperature?")
- CRUD operations (Create, Read, Update, Delete)

Time-series databases are optimized for:
- Range queries ("Show temperature from 9 AM to 5 PM")
- Aggregations ("Average temperature per hour for the last week")
- Downsampling ("Store hourly averages instead of per-second readings")
- Retention policies ("Delete data older than 90 days")

### InfluxDB Key Concepts

| Concept | Description | Example |
|---------|-------------|---------|
| **Measurement** | The "table" for a data type | `temperature`, `vibration` |
| **Tag** | Indexed metadata | `machine_id=hyd_press_7`, `location=hall_a` |
| **Field** | The actual data values | `value=72.5`, `unit=celsius` |
| **Timestamp** | When the data was recorded | `2024-01-15T10:30:00Z` |

### Sample Query (Flux language)
```flux
from(bucket: "factory_metrics")
  |> range(start: -24h)
  |> filter(fn: (r) => r["_measurement"] == "temperature")
  |> filter(fn: (r) => r["machine_id"] == "hyd_press_7")
  |> aggregateWindow(every: 1h, fn: mean)
```

---

## OPENTELEMETRY (OTEL)

### What is OpenTelemetry?
OpenTelemetry is an open-source observability framework for generating, collecting, and exporting telemetry data (metrics, logs, traces).

### The Three Pillars

1. **Metrics**: Numeric measurements over time
   - Counter: Cumulative value (e.g., total requests)
   - Gauge: Current value (e.g., temperature)
   - Histogram: Distribution of values (e.g., response times)

2. **Logs**: Text records of events
   - Structured logging with context
   - Correlation with traces
   - Severity levels (DEBUG, INFO, WARN, ERROR)

3. **Traces**: Request flow through systems
   - Spans representing operations
   - Parent-child relationships
   - Distributed context propagation

### OTEL Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     APPLICATION CODE                         │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │ Metrics  │  │   Logs   │  │  Traces  │                  │
│  │   API    │  │   API    │  │   API    │                  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                  │
│       │             │             │                         │
│       └─────────────┼─────────────┘                         │
│                     ▼                                        │
│            ┌──────────────┐                                  │
│            │  OTEL SDK    │                                  │
│            └──────┬───────┘                                  │
│                   │                                          │
└───────────────────┼──────────────────────────────────────────┘
                    ▼
           ┌──────────────┐
           │ OTEL         │
           │ COLLECTOR    │
           └──────┬───────┘
                  │
         ┌───────┴───────┐
         ▼               ▼
    ┌─────────┐    ┌─────────┐
    │InfluxDB │    │ Grafana │
    │         │    │  Tempo  │
    └─────────┘    └─────────┘
```

---

## GRAFANA VISUALIZATION

### Key Dashboard Concepts

1. **Panels**: Individual visualizations (graphs, gauges, tables)
2. **Rows**: Logical groupings of panels
3. **Variables**: Dynamic filters (select machine, time range)
4. **Alerts**: Threshold-based notifications

### Common Visualization Types

| Type | Best For | Example Use |
|------|----------|-------------|
| **Time Series** | Trends over time | Temperature history |
| **Gauge** | Current status | Current vibration level |
| **Stat** | Single values | Total alarms today |
| **Heatmap** | Pattern density | Alarm frequency by hour |
| **Table** | Detailed data | Recent alarm list |

---

## SESSION 1 EXERCISES

### Exercise 1.1: Telemetry Fundamentals Quiz (50 pts, 5 min)

**Question Examples:**

1. What is the primary purpose of telemetry in industrial settings?
   - [ ] Increase production speed
   - [x] Remote monitoring and data collection
   - [ ] Replace human workers
   - [ ] Reduce energy costs

2. Which database type is BEST suited for storing sensor data with timestamps?
   - [ ] Relational (SQL)
   - [ ] Document (MongoDB)
   - [x] Time-series (InfluxDB)
   - [ ] Graph (Neo4j)

3. In a telemetry pipeline, what comes immediately after data collection?
   - [ ] Visualization
   - [ ] Alerting
   - [x] Storage/Processing
   - [ ] Analysis

### Exercise 1.2: Data Challenge (100 pts, 8 min)

**Scenario**: Participants view 21 days of telemetry data from Neel's machine. They must:
1. Identify which sensors show anomalies
2. Determine when the degradation began
3. Predict what type of failure is occurring
4. Avoid red herrings (non-critical variations)

**Key Patterns to Identify**:
- Harmonics drift starting Day 3-5
- Current increase starting Day 8-10
- Temperature rise starting Day 12-14
- Red herring: Ambient temperature spike (not correlated to failure)

### Exercise 1.3: OpenTelemetry Matching (50 pts, 4 min)

**Match concepts to definitions:**

| Concept | Match To |
|---------|----------|
| Metric | Numeric measurement over time |
| Trace | Request flow through distributed system |
| Span | Single operation within a trace |
| Collector | Receives and exports telemetry data |
| Exporter | Sends data to backend storage |

### Exercise 1.4: Pipeline Builder (75 pts, 5 min)

**Build an n8n-style workflow connecting:**
- Sensor nodes
- Kafka message queue
- Transform/filter node
- AI Agent analysis
- InfluxDB storage
- Alert notification

### Exercise 1.5: LLMs & AI Agents Quiz (50 pts, 5 min)

**Topics Covered:**
- What is an LLM (Large Language Model)?
- LLM vs Traditional ML
- What is an AI Agent?
- Agent capabilities (reasoning, tool use, memory)
- Limitations and human oversight

### Exercise 1.6: MCP Challenge (75 pts, 6 min)

**Model Context Protocol (MCP) concepts:**
- MCP Client: Applications that connect to MCP servers
- MCP Server: Provides tools and resources to clients
- Tool: An action the AI can perform
- Resource: Data the AI can access

**Practical exercise**: Match MCP components and complete code snippets.

### Bonus: Drishti Interpretation (100 pts, no time limit)

**Interpret AI agent output:**
```json
{
  "agent": "Drishti",
  "timestamp": "2024-01-15T10:30:00Z",
  "analysis": {
    "machine_id": "HYD_PRESS_07",
    "anomaly_detected": true,
    "confidence": 0.87,
    "pattern": "bearing_degradation",
    "evidence": [
      "Harmonics drift 18% from baseline",
      "Current increase 12%",
      "Temperature 4°C above expected"
    ],
    "recommendation": "Schedule inspection within 7 days"
  }
}
```

Questions test understanding of:
- What evidence did the agent use?
- What does 87% confidence mean?
- Why is this a bearing issue specifically?
- What action should be taken?

---

## KEY TERMINOLOGY

**Workshop machine reference:** The scenario centres on **Hydraulic Press Machine 7** (machine ID: **HYD_PRESS_07** / tag: **hyd_press_7**), operated by Neel at Shakti Heavy Industries, Bhopal.

| Term | Definition |
|------|------------|
| **Telemetry** | Automated remote data collection and transmission |
| **Time-series** | Data indexed by timestamp |
| **MTBF** | Mean Time Between Failures |
| **Baseline** | Normal operating parameters |
| **Anomaly** | Deviation from expected behavior |
| **Harmonics** | Frequency components in a signal |
| **OPC-UA** | Industrial communication protocol |
| **MQTT** | Lightweight messaging protocol for IoT |
| **PLC** | Programmable Logic Controller |
| **SCADA** | Supervisory Control and Data Acquisition |

---

## TRANSITION TO SESSION 2

### The Question We've Answered
- What is telemetry and why it matters
- How data flows from sensors to dashboards
- What the data looks like when equipment fails

### The Question Session 2 Answers
- Why can't traditional automation solve this problem?
- How do AI agents think and reason?
- How do we build a multi-agent swarm for predictive maintenance?

### Preview: The Agent Swarm
In Session 2, we'll build:
1. **Drishti** - The Continuous Monitor (watches all data)
2. **Jibreel** - The Anomaly Detector (spots patterns)
3. **Athena** - The Root Cause Analyzer (diagnoses issues)
4. **Vidhaata** - The Maintenance Scheduler (plans actions)
5. **Hermes** - The Alert Messenger (notifies people)

---

## SLIDE STRUCTURE SUGGESTIONS

### Slide 1: Title
"Ghost in the Machine: AI Agents for Industrial Telemetry"

### Slide 2-3: Neel's Story (Hook)
- Photo representation of a factory worker
- The tragedy in brief
- "Could AI have saved him?"

### Slide 4-5: What is Telemetry?
- Definition with factory visual
- The pipeline diagram

### Slide 6-8: InfluxDB & Time-Series
- Why specialized databases matter
- Key concepts table
- Sample query

### Slide 9-11: OpenTelemetry
- The three pillars
- Architecture diagram
- How it connects to industrial systems

### Slide 12-13: The Data Challenge
- Show sample sensor data
- Ask audience: "What do you see?"

### Slide 14-15: The Problem Scale
- 500+ sensors
- 2,000+ alarms/day
- 3 operators
- "This is why AI agents matter"

### Slide 16: Transition to Session 2
- "Now let's build the solution"

---

*Document prepared for FDP Workshop: Ghost in the Machine*
*Version: 1.0 | Date: February 2025*
