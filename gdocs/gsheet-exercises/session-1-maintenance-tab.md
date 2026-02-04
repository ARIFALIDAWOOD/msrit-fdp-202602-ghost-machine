# Session 1 — Maintenance tab (spec and sample data)

Use this to add a **Maintenance** tab (or separate sheet) to the same Google Sheet, so participants can complete **Step 7** of the Session 1 exercises.

---

## Suggested columns

| Column name | Description | Example |
|-------------|-------------|--------|
| `equipment_id` | Matches telemetry (e.g. HYD_PRESS_07) | HYD_PRESS_07 |
| `last_bearing_replacement_days_ago` | Days since last bearing replacement | 847 |
| `MTBF_days` | Manufacturer mean time between failure (days) | 900 |
| `operational_hours` | Current run hours (optional) | 12450 |
| `rated_hours` | Rated life or service interval in hours (optional) | 15000 |
| `notes` | Short note (optional) | Bearing degradation risk |

You can use fewer columns (e.g. just `equipment_id`, `last_bearing_replacement_days_ago`, `MTBF_days`) and add the rest if needed.

---

## Sample row for HYD_PRESS_07

Paste this as the header and one data row in the Maintenance tab so it matches the Session 1 narrative (outline: “Last bearing replacement: 847 days ago”, “Manufacturer MTBF: 900 days”).

**Header row:**

```
equipment_id	last_bearing_replacement_days_ago	MTBF_days	operational_hours	rated_hours	notes
```

**Data row (tab-separated; paste into the sheet and split by Tab or use “Paste → Split to columns”):**

```
HYD_PRESS_07	847	900	12450	15000	Bearing degradation risk; recommend replacement within 14 days
```

**Same row as comma-separated** (if your sheet expects CSV-style paste):

```
HYD_PRESS_07,847,900,12450,15000,Bearing degradation risk; recommend replacement within 14 days
```

Participants can then look up **HYD_PRESS_07** and see that the equipment is past the typical service window (847 days vs 900-day MTBF), supporting the “subtle vibration drift” story and the need to combine telemetry with maintenance context.
