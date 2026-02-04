# Session 1 — Step-by-step exercises (Google Sheet)

Work through these steps **in your shared Google Sheet** that contains the Neel telemetry data. The goal is to explore the raw data and see how hard it is to find the signal that predicted the failure.

---

## Step 1: Data orientation

**What you have**

- **Rows**: Thousands of readings (one every 5 minutes over about 3 weeks).
- **Columns**: `timestamp`, `equipment_id`, and six sensor channels: `acoustic_db`, `flow_rate`, `motor_current`, `pressure`, `temperature`, `vibration_rms`.
- **Equipment**: All rows are for **HYD_PRESS_07** (Hydraulic Press Unit #7).

**Do this**

1. Check the first and last `timestamp` to confirm the date range (about 3 weeks).
2. Note how many data rows you have (e.g. count non-header rows).

**Think:** If you had to find “the” warning sign in this many rows and columns, where would you start?

---

## Step 2: Extract numeric values

Sensor columns may contain text that looks like: `{'value': 75.096, 'unit': 'decibel'}`. To chart and use formulas, we need the number.

**If your sensor cells already show plain numbers** (e.g. `75.096`), skip to Step 3.

**If your sensor cells still show the full text** (with `'value':` and `'unit':`):

1. Add a new column next to the first sensor column (e.g. after `acoustic_db`). Name it something like `acoustic_value`.
2. In the first data row of that new column, use this formula (adjust the cell reference to match your sheet; here we assume the raw value is in column C and row 2):

   ```
   =IF(ISNUMBER(C2), C2, VALUE(REGEXEXTRACT(C2,"value':\s*([0-9.]+)")))
   ```

   - If the cell is already a number, it stays as is. Otherwise, it extracts the number after `'value':` and converts it to a number.
3. Fill the formula down to the last data row.
4. Repeat the same idea for the other sensor columns: `flow_rate`, `motor_current`, `pressure`, `temperature`, `vibration_rms` (each in its own new column, e.g. `temperature_value`, `vibration_value`). Use the same formula pattern but reference the column that has the raw text (e.g. for temperature in column G, use `G2` in the formula).

**Facilitator note:** You can do this for one or two columns and have participants do the rest, or do all columns once and share the sheet.

---

## Step 3: Single-metric exploration

Pick one metric to explore—for example **temperature** (use your extracted numeric column if you added one in Step 2).

**Do this**

1. For that column, compute:
   - **Min**: `=MIN(range)`  
   - **Max**: `=MAX(range)`  
   - **Average**: `=AVERAGE(range)`  
   (Use the full data range, e.g. from row 2 to the last row.)
2. Insert a **line chart**:
   - X-axis: timestamp (column A).
   - Y-axis: the numeric temperature values.
3. Look at the shape of the curve over the 3 weeks.

**Think:** What stands out? Any big spikes or dips? Would you call any of this “the” failure signal?

---

## Step 4: Spot the red herring

There is a **noticeable temperature spike** in the data—a period where temperature is clearly higher than usual.

**Do this**

1. In your temperature chart or table, find that spike (e.g. filter or sort by the temperature column to see the highest values and their dates).
2. Note the date/time and size of the spike.

**Think:** “Could this temperature spike be the warning that predicted the failure?” We’ll come back to this: the real signal is subtler and in a different metric.

---

## Step 5: Multi-metric view

Real failures often show up in **more than one** signal. Compare temperature with **vibration** (and optionally **motor current**).

**Do this**

1. Create a chart that shows at least two metrics over time:
   - Option A: Two series on the same chart (e.g. timestamp vs temperature and timestamp vs vibration, using two Y-axes if the scales are very different).
   - Option B: Two separate line charts, one for temperature and one for vibration, for the same time range.
2. Compare behavior: Where does temperature spike? Where does vibration change? Do they move together or differently?

**Think:** If you only looked at temperature, you might blame the spike. What does vibration do in that same period?

---

## Step 6: The subtle signal

The **real** predictive signal is a **small, gradual drift** in vibration—the kind that’s easy to miss when you’re looking at raw points.

**Do this**

1. Use your numeric vibration column. Compute a **weekly average** (or a 7-day moving average) so the trend is visible:
   - **Weekly average**: Add a column for “week” (e.g. `=WEEKNUM(A2)` or a date rounded to week), then use `=AVERAGEIF(week_column, week_number, vibration_column)` for each week.
   - **7-day moving average**: In a new column, use `=AVERAGE(offset_range)` over the last 7 rows (or about 7×288 rows if you have 5-min data and want 7 days). Fill down.
2. Chart this trend (e.g. weekly average or moving average over time).
3. Look for a **slight upward drift** over the three weeks—small percentage change, not a big spike.

**Think:** This is the kind of signal that can predict failure but is easy to overlook when you’re scanning raw data. Would you have found it without focusing on vibration and smoothing the series?

---

## Step 7: The missing piece

Diagnosis often needs **context** that isn’t in the telemetry stream—for example **maintenance history**.

**Do this**

1. Open the **Maintenance** tab (or the separate Maintenance sheet your facilitator set up).
2. Find the row for **HYD_PRESS_07** and look for:
   - Last bearing replacement (e.g. “days ago” or last service date).
   - Any MTBF (mean time between failure) or recommended service interval.
3. Compare that to the vibration trend you saw: the equipment may be near or past a recommended service window.

**Think:** Would you have thought to open this tab while looking at the telemetry? Agents can combine telemetry and maintenance data in one analysis—something that’s easy to miss when we work manually.

---

## Debrief (facilitator-led)

- How many people noticed the temperature spike? How many focused on vibration trend?
- How many checked the Maintenance tab without being told?
- This is why we need a different approach: more context, multiple signals, and no single place where “the” answer lives. Later in the session you’ll see how an agent (Drishti) can do this kind of analysis in seconds.
