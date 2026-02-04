# Session 2: Building the Swarm - Complete Reference Document

## For NotebookLM & Google Slides Preparation

---

## LEARNING OUTCOMES

By the end of Session 2, participants will be able to:

1. **Articulate why traditional automation** is insufficient for modern predictive maintenance
2. **Describe the ISA-95 architecture** and where AI agents fit
3. **Understand each agent's role** in the Drishti swarm
4. **Configure threshold settings** that balance sensitivity and false positives
5. **Connect MCP tools** to extend AI agent capabilities
6. **Design a complete agent architecture** for industrial monitoring

---

## THE CASE FOR AI AGENTS

### The Skeptic's Question
> "We have PLCs, SCADA, DCS systems. We have threshold alarms and predictive maintenance algorithms. Why do we need AI agents?"

### The Answer: 7 Capabilities That Justify AI Agents

#### 1. Cross-Silo Reasoning
**Traditional**: PLC sees pressure spike → Alerts operator → Operator checks multiple systems manually

**With AI Agent**: Agent correlates pressure spike with:
- Upstream valve position (different PLC)
- Ambient temperature (building management)
- Current production batch (MES)
- Recent maintenance (CMMS)
- Similar historical incidents (data lake)

#### 2. Unstructured Data Understanding
**Traditional**: Maintenance manual in PDF, operator searches manually

**With AI Agent**:
- Reads equipment manuals, extracts procedures
- Understands technician notes in natural language
- Parses old incident reports for patterns

#### 3. Adaptive Pattern Recognition
**Traditional**: Fixed threshold: Temperature > 85°C = Alarm

**With AI Agent**: Learns that:
- 82°C is normal in summer, concerning in winter
- 85°C after startup is fine, during steady-state is not
- This machine runs 3°C hotter than identical Unit #6

#### 4. Natural Language Interface
**Traditional**: Navigate SCADA menus, interpret codes

**With AI Agent**:
- Operator: "Why is Unit 7 running hot?"
- Agent: "Unit 7 is 6°C above baseline. Correlates with 12% motor current increase. Pattern matches bearing wear from Unit 4 in 2023. Recommend inspection within 14 days."

#### 5. Explainable Recommendations
**Traditional**: "Maintenance Required" with no explanation

**With AI Agent**:
```
RECOMMENDATION: Schedule bearing replacement within 14 days

REASONING:
1. Harmonics drifted 18% from baseline
2. Motor current increased 12% (r²=0.87 correlation)
3. Pattern matches bearing degradation (87% confidence)
4. Last replacement: 847 days ago (MTBF: 900 days)

ALTERNATIVE EXPLANATIONS CONSIDERED:
- Lubrication issue: Less likely (no acoustic change)
- Belt wear: Ruled out (vibration doesn't match)

CONFIDENCE: 87%
UNCERTAINTY: Could be motor winding issue (8% probability)
```

#### 6. Multi-System Orchestration
**Traditional**: Each system has separate scheduling, alerting, escalation

**With AI Agent**:
- Checks parts inventory (ERP)
- Finds maintenance window (MES schedule)
- Assigns technician (CMMS)
- Pre-orders parts (procurement)
- Schedules quality check (QMS)
- Notifies stakeholders (communications)

#### 7. Continuous Learning & Adaptation
**Traditional**: Rules static until manually updated

**With AI Agent**:
- Learns from each incident resolution
- Adjusts sensitivity based on false positive feedback
- Incorporates new failure patterns automatically

---

## ISA-95 ARCHITECTURE

### Traditional Automation Pyramid

```
┌─────────────────────────────────────────────────────────────┐
│                 TRADITIONAL AUTOMATION PYRAMID               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Level 4: ERP (Enterprise Planning)        ──── Days/Weeks  │
│              ↑                                               │
│  Level 3: MES (Manufacturing Execution)    ──── Hours       │
│              ↑                                               │
│  Level 2: SCADA/HMI (Supervisory)          ──── Minutes     │
│              ↑                                               │
│  Level 1: PLC/DCS (Control)                ──── Seconds     │
│              ↑                                               │
│  Level 0: Sensors/Actuators (Field)        ──── Milliseconds│
│                                                              │
│  ⚠️ PROBLEM: Each level is SILOED                           │
│  ⚠️ PROBLEM: Rules are STATIC                               │
│  ⚠️ PROBLEM: Context is LOST between levels                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### AI-Augmented Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  AI-AUGMENTED AUTOMATION                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │           AI AGENT LAYER (Cognitive)                 │    │
│  │                                                      │    │
│  │  • Understands CONTEXT across all levels             │    │
│  │  • Reasons about UNSTRUCTURED data                   │    │
│  │  • Learns from PATTERNS not just thresholds          │    │
│  │  • Communicates in NATURAL LANGUAGE                  │    │
│  │  • Makes RECOMMENDATIONS with explanations           │    │
│  │                                                      │    │
│  └──────────────────────┬───────────────────────────────┘    │
│                         │                                    │
│                         ▼ Interfaces with ALL levels         │
│                                                              │
│  Level 4: ERP ←────────── Agent can query/update            │
│  Level 3: MES ←────────── Agent can coordinate              │
│  Level 2: SCADA ←──────── Agent can interpret               │
│  Level 1: PLC ←────────── Agent can recommend               │
│  Level 0: Sensors ←────── Agent understands semantics       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## THE AGENT SWARM

**Machine context:** All agent examples refer to **Hydraulic Press Machine 7** (HYD_PRESS_07) at Shakti Heavy Industries—the same asset from Session 1 (Neel's machine).

### Meet the Team

| Agent | Role | Specialty | Color |
|-------|------|-----------|-------|
| **Drishti** | Continuous Monitor | 24/7 data watching, baseline tracking | Purple (#a855f7) |
| **Jibreel** | Anomaly Detector | Pattern recognition, deviation scoring | Yellow (#eab308) |
| **Athena** | Root Cause Analyzer | Diagnosis, failure mode identification | Cyan (#06b6d4) |
| **Vidhaata** | Maintenance Scheduler | Planning, resource optimization | Pink (#ec4899) |
| **Hermes** | Alert Messenger | Communication, escalation, notifications | Green (#84cc16) |

### Agent Responsibilities

#### Drishti (दृष्टि - "Vision")
- Ingests all sensor streams
- Maintains rolling baselines per equipment
- Flags statistical anomalies (z-score > 2.5)
- Correlates multi-sensor patterns
- Passes suspicious data to Jibreel

**Sample Output:**
```json
{
  "agent": "Drishti",
  "event": "anomaly_flagged",
  "machine_id": "HYD_PRESS_07",
  "sensors": ["harmonics", "motor_current"],
  "deviation_score": 3.2,
  "duration": "48 hours",
  "confidence": 0.78
}
```

#### Jibreel (جبریل - "Gabriel, the messenger")
- Receives flagged data from Drishti
- Compares against known failure patterns
- Classifies anomaly type (bearing, motor, belt, etc.)
- Scores urgency (INFO/WARNING/CRITICAL)
- Escalates to Athena if diagnosis needed

**Classification Categories:**
- BEARING_DEGRADATION
- MOTOR_WINDING_ISSUE
- BELT_WEAR
- LUBRICATION_FAILURE
- ELECTRICAL_FAULT
- UNKNOWN (requires Athena)

#### Athena (Αθηνά - "Goddess of wisdom")
- Deep analysis of complex failures
- Root cause determination
- Alternative hypothesis testing
- Historical incident correlation
- Generates diagnostic report

**Sample Diagnostic:**
```
ROOT CAUSE ANALYSIS - HYD_PRESS_07 (Hydraulic Press Machine 7)

PRIMARY DIAGNOSIS: Inner race bearing wear (87% confidence)

EVIDENCE:
1. Harmonics at 2.3kHz drifted 18% (characteristic frequency)
2. Motor current increased 12% (bearing friction)
3. Temperature rise 4°C (heat from friction)
4. Matches Unit-4 failure pattern from 2023-08

ALTERNATIVE HYPOTHESES:
- Motor winding (8%): No electrical signature
- Belt slip (3%): Vibration doesn't match
- Lubrication (2%): Acoustic normal

RECOMMENDED ACTION: Bearing replacement
TIMELINE: Within 14 days
RISK IF DELAYED: Catastrophic failure probability 65% by day 30
```

#### Vidhaata (विधाता - "Creator/Destiny")
- Receives maintenance recommendation
- Queries parts inventory
- Checks production schedule
- Finds optimal maintenance window
- Assigns resources
- Creates work order

**Scheduling Constraints:**
- Production deadlines
- Technician availability
- Parts lead time
- Equipment criticality
- Safety requirements

#### Hermes (Ἑρμῆς - "Messenger god")
- Delivers notifications to right recipients
- Escalates based on severity
- Manages acknowledgment workflow
- Provides summary reports
- Handles human response routing

**Notification Levels:**
| Severity | Recipients | Channels | SLA |
|----------|------------|----------|-----|
| INFO | Maintenance log | Email, dashboard | 24h |
| WARNING | Maintenance team | Email, SMS | 4h |
| CRITICAL | Plant manager | SMS, phone, alarm | 15m |

---

## THE SWARM ARCHITECTURE

```
┌────────────────────────────────────────────────────────────────┐
│                    AGENT SWARM ARCHITECTURE                     │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│     SENSORS                                                     │
│        │                                                        │
│        ▼                                                        │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐               │
│  │ DRISHTI  │────▶│ JIBREEL  │────▶│  ATHENA  │               │
│  │ Monitor  │     │ Detector │     │ Analyzer │               │
│  └──────────┘     └──────────┘     └──────────┘               │
│                         │                │                      │
│                         │                ▼                      │
│                         │          ┌──────────┐                │
│                         │          │ VIDHAATA │                │
│                         │          │Scheduler │                │
│                         │          └──────────┘                │
│                         │                │                      │
│                         │                ▼                      │
│                         │          ┌──────────┐                │
│                         └─────────▶│  HERMES  │◀───────────────│
│                                    │Messenger │                 │
│                                    └──────────┘                │
│                                         │                       │
│                                         ▼                       │
│                              ┌───────────────────┐             │
│                              │  HUMAN OPERATORS  │             │
│                              │ (Decision makers) │             │
│                              └───────────────────┘             │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## MODEL CONTEXT PROTOCOL (MCP)

### What is MCP?
MCP (Model Context Protocol) is an open standard for connecting AI models to external tools and data sources.

### Key Components

| Component | Description | Example |
|-----------|-------------|---------|
| **MCP Server** | Provides tools and resources | InfluxDB query server |
| **MCP Client** | Application connecting to servers | Claude Code, IDE plugins |
| **Tool** | Action the AI can perform | `query_sensor_data()` |
| **Resource** | Data the AI can access | Equipment manuals, logs |

### MCP Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      AI APPLICATION                          │
│                                                              │
│  ┌──────────────┐                                           │
│  │   Claude     │                                           │
│  │   (LLM)      │                                           │
│  └──────┬───────┘                                           │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────┐                                           │
│  │  MCP Client  │                                           │
│  └──────┬───────┘                                           │
│         │                                                    │
└─────────┼────────────────────────────────────────────────────┘
          │
          │ JSON-RPC over stdio/HTTP
          │
┌─────────┴─────────┬─────────────────┬───────────────────────┐
│                   │                 │                        │
▼                   ▼                 ▼                        ▼
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────────────┐
│InfluxDB │   │ Grafana │   │  CMMS   │   │ Equipment       │
│ MCP     │   │ MCP     │   │ MCP     │   │ Manual MCP      │
│ Server  │   │ Server  │   │ Server  │   │ Server          │
└─────────┘   └─────────┘   └─────────┘   └─────────────────┘
```

### Sample MCP Tool Definition

```json
{
  "name": "query_sensor_data",
  "description": "Query time-series sensor data from InfluxDB",
  "inputSchema": {
    "type": "object",
    "properties": {
      "machine_id": {
        "type": "string",
        "description": "Equipment identifier"
      },
      "sensor_type": {
        "type": "string",
        "enum": ["temperature", "vibration", "current", "harmonics"]
      },
      "time_range": {
        "type": "string",
        "description": "ISO 8601 duration (e.g., 'P7D' for 7 days)"
      }
    },
    "required": ["machine_id", "sensor_type", "time_range"]
  }
}
```

---

## SESSION 2 EXERCISES

### Exercise 2.1: Why AI Agents Quiz (75 pts, 6 min)

**Sample Questions:**

1. Which capability do AI agents have that traditional PLCs lack?
   - [ ] Faster processing speed
   - [x] Cross-silo reasoning across systems
   - [ ] Lower cost of implementation
   - [ ] Better sensor accuracy

2. In the ISA-95 pyramid, where does the AI agent layer sit?
   - [ ] Replaces Level 1 (PLC)
   - [ ] Between Level 2 and 3
   - [x] As an overlay connecting all levels
   - [ ] Only at Level 4 (ERP)

3. What makes AI agents "adaptive" compared to rule-based systems?
   - [x] They learn from outcomes and adjust
   - [ ] They run faster
   - [ ] They cost less to maintain
   - [ ] They need fewer sensors

### Exercise 2.2: Five Demos Scenarios (100 pts, 8 min)

Present 5 scenarios, ask participants to identify which AI agent capability applies:

1. **Scenario**: Agent reads a 200-page equipment manual to find relevant troubleshooting steps
   **Capability**: Unstructured Data Understanding

2. **Scenario**: Agent correlates pressure spike with upstream valve, ambient temp, and production batch
   **Capability**: Cross-Silo Reasoning

3. **Scenario**: Operator asks "Why is Unit 7 hot?" and gets a natural language explanation
   **Capability**: Natural Language Interface

4. **Scenario**: Agent explains not just "replace bearing" but WHY with evidence chain
   **Capability**: Explainable Recommendations

5. **Scenario**: Single command triggers inventory check, scheduling, technician assignment
   **Capability**: Multi-System Orchestration

### Exercise 2.3: Threshold Tuner (100 pts, 6 min)

Interactive simulation where participants adjust warning and critical thresholds for:
- Temperature
- Vibration
- Motor Current
- Harmonics

**Goal**: Detect the real anomaly (bearing degradation) while avoiding:
- False positives (alert fatigue)
- False negatives (missing the failure)
- Red herrings (ambient temp spike)

**Optimal Settings:**
| Sensor | Warning | Critical |
|--------|---------|----------|
| Temperature | 72°C | 80°C |
| Vibration | 1.8 mm/s | 2.5 mm/s |
| Motor Current | +8% | +15% |
| Harmonics | +12% | +20% |

### Exercise 2.4: Classification Game (150 pts, 10 min)

Timed game where participants classify scenarios as INFO, WARNING, or CRITICAL:

**Sample Scenarios:**

1. "Motor current 3% above baseline, stable for 48 hours"
   → **INFO** (normal variation)

2. "Harmonics drifted 15%, motor current up 10%, correlated"
   → **WARNING** (developing issue)

3. "Vibration spike 4x normal, temperature rising rapidly"
   → **CRITICAL** (imminent failure)

**Scoring:**
- Correct: +10 points
- Streak bonus: 3+ correct = +10, 5+ = +25, 10+ = +50
- Wrong answer: Streak reset

### Exercise 2.5: Architecture Builder (100 pts, 7 min)

Drag-and-drop node connector exercise to build the complete swarm:

**Available Nodes:**
- Sensors
- Drishti (Monitor)
- Jibreel (Detector)
- Athena (Analyzer)
- Vidhaata (Scheduler)
- Hermes (Messenger)
- Human Operator
- InfluxDB
- Alert System

**Required Connections:**
1. Sensors → Drishti
2. Drishti → Jibreel
3. Jibreel → Athena
4. Athena → Vidhaata
5. Vidhaata → Hermes
6. Hermes → Human Operator
7. Drishti → InfluxDB
8. Hermes → Alert System

### Exercise 2.6: Final Integration (175 pts, 12 min)

Comprehensive assessment covering all workshop concepts:

**Section A**: Telemetry Fundamentals (5 questions)
**Section B**: AI Agent Capabilities (5 questions)
**Section C**: Swarm Architecture (5 questions)
**Section D**: MCP & Tools (5 questions)
**Section E**: Scenario Analysis (5 questions)

**Passing Criteria**: 60% for completion certificate, 80% for proficiency, 95% for mastery

---

## HUMAN-IN-THE-LOOP

### Why Humans Stay in Control

AI agents are **advisors**, not **autonomous controllers**. The human:
- Makes final decisions on maintenance scheduling
- Approves work orders
- Validates diagnoses before action
- Handles edge cases and exceptions
- Provides feedback for agent learning

### The Escalation Path

```
Agent Recommendation
        │
        ▼
┌───────────────┐
│ Auto-approved │ ◀── Low risk, high confidence
│   actions     │
└───────────────┘
        │
        ▼
┌───────────────┐
│   Operator    │ ◀── Standard maintenance
│   approval    │
└───────────────┘
        │
        ▼
┌───────────────┐
│  Supervisor   │ ◀── High cost or risk
│   approval    │
└───────────────┘
        │
        ▼
┌───────────────┐
│    Plant      │ ◀── Production impact
│   Manager     │
└───────────────┘
```

---

## OBJECTION HANDLING

### Common Objections and Responses

**"This is just another buzzword"**
→ Show the 7 capabilities demo. Let them experience cross-silo reasoning they can't do with existing tools.

**"We already have predictive maintenance"**
→ Ask: Does it explain WHY? Can you ask it questions? Does it learn from mistakes? AI agents add cognition, not just prediction.

**"AI will replace workers"**
→ AI handles the 2,000 alarms/day so humans can focus on decisions. It's augmentation, not replacement. Neel still needs his job—he just needs AI watching his back.

**"We can't afford this"**
→ Calculate the cost of one catastrophic failure (equipment, downtime, injury, liability). Compare to AI agent implementation. The ROI is clear.

**"Our data isn't good enough"**
→ Start with existing sensors. AI agents can work with imperfect data—they understand context that rules cannot.

---

## CONCLUSION: SAVING NEEL

### The Alternative Timeline

With the Agent Swarm:
- **Day 3**: Drishti flags subtle harmonic drift
- **Day 5**: Jibreel classifies as potential bearing issue
- **Day 7**: Athena confirms bearing degradation, 78% confidence
- **Day 8**: Vidhaata schedules maintenance for Day 14 (production window)
- **Day 9**: Hermes notifies maintenance team, orders parts
- **Day 14**: Bearing replaced during planned maintenance
- **Day 21**: Neel operates healthy machine, goes home safely

### The Mission Continues

This workshop gave you:
1. Understanding of telemetry and industrial monitoring
2. Knowledge of AI agent capabilities and architecture
3. Hands-on experience configuring and connecting agents
4. A vision for the future of industrial automation

**Your next step**: Take these concepts back to your institution. Build demos. Train students. Help create the next generation of engineers who design systems that protect workers like Neel.

---

## SLIDE STRUCTURE SUGGESTIONS

### Slide 1: Recap of Session 1
- Neel's story recap
- What we learned about telemetry

### Slide 2-4: Why AI Agents?
- The 7 capabilities
- ISA-95 pyramid comparison

### Slide 5-7: Meet the Swarm
- Each agent introduction
- The architecture diagram

### Slide 8-10: MCP Deep Dive
- What is MCP
- Tool definitions
- Connection diagram

### Slide 11-12: Threshold Exercise
- Interactive demo
- Balance sensitivity vs. false positives

### Slide 13-14: Classification Game
- Sample scenarios
- Timed challenge

### Slide 15-16: Human-in-the-Loop
- Why humans stay in control
- The escalation path

### Slide 17-18: Saving Neel
- The alternative timeline
- The mission continues

### Slide 19: Call to Action
- What participants will do next
- Resources and next steps

---

*Document prepared for FDP Workshop: Ghost in the Machine*
*Version: 1.0 | Date: February 2025*
