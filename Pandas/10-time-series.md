[← Previous: Merging & Joining](9-merging-joining.md) | [🏠 Home](README.md) | [Next: Advanced Topics →](11-advanced-topics.md)

---

# 10. Time Series

## Table of Contents
- [DateTime Basics](#datetime-basics)
- [Parsing Dates](#parsing-dates)
- [DateTime Indexing](#datetime-indexing)
- [Resampling](#resampling)
- [Rolling Windows](#rolling-windows)
- [Shifting and Lagging](#shifting-and-lagging)
- [Time Zones](#time-zones)
- [Traditional vs Pandas Way](#traditional-vs-pandas-way)
- [Common Mistakes](#common-mistakes)
- [Best Practices](#best-practices)

---

## DateTime Basics

### Creating DateTime Objects

```python
import pandas as pd
import numpy as np

# From string
dt = pd.Timestamp("2024-01-15")
print(dt)  # 2024-01-15 00:00:00

# Current time
now = pd.Timestamp.now()

# DateTime range
dates = pd.date_range("2024-01-01", periods=5, freq="D")
print(dates)
# DatetimeIndex(['2024-01-01', '2024-01-02', '2024-01-03',
#                '2024-01-04', '2024-01-05'], freq='D')

# Common frequencies
dates_daily = pd.date_range("2024-01-01", periods=5, freq="D")     # Daily
dates_weekly = pd.date_range("2024-01-01", periods=5, freq="W")    # Weekly
dates_monthly = pd.date_range("2024-01-01", periods=5, freq="MS")  # Month start
dates_hourly = pd.date_range("2024-01-01", periods=5, freq="h")    # Hourly
dates_bday = pd.date_range("2024-01-01", periods=5, freq="B")     # Business days
```

### DateTime Properties

```python
ts = pd.Timestamp("2024-03-15 14:30:45")

print(ts.year)        # 2024
print(ts.month)       # 3
print(ts.day)         # 15
print(ts.hour)        # 14
print(ts.minute)      # 30
print(ts.second)      # 45
print(ts.dayofweek)   # 4 (Friday, 0=Monday)
print(ts.day_name())  # Friday
print(ts.quarter)     # 1

# On a Series
df = pd.DataFrame({
    "date": pd.date_range("2024-01-01", periods=5, freq="MS"),
    "value": [100, 150, 200, 180, 220]
})

print(df["date"].dt.year)        # Year
print(df["date"].dt.month)       # Month
print(df["date"].dt.day_name())  # Day name
print(df["date"].dt.quarter)     # Quarter
```

---

## Parsing Dates

### Converting Strings to DateTime

```python
df = pd.DataFrame({
    "date_str": ["2024-01-15", "2024/02/20", "March 10, 2024", "15-04-2024"],
    "value": [100, 200, 300, 400]
})

# Auto-detect format
df["date"] = pd.to_datetime(df["date_str"])

# Specific format (faster for large datasets)
df["date"] = pd.to_datetime(df["date_str"], format="%Y-%m-%d")

# Handle errors
df["date"] = pd.to_datetime(df["date_str"], errors="coerce")  # NaT for bad dates

# Read CSV with date parsing
df = pd.read_csv("data.csv", parse_dates=["date_column"])
```

### Common Format Codes

```
%Y → 4-digit year  (2024)
%m → Month number  (01-12)
%d → Day number    (01-31)
%H → Hour          (00-23)
%M → Minute        (00-59)
%S → Second        (00-59)
%B → Month name    (January)
%A → Day name      (Monday)

Examples:
"2024-01-15"       → "%Y-%m-%d"
"15/01/2024"       → "%d/%m/%Y"
"Jan 15, 2024"     → "%b %d, %Y"
"2024-01-15 14:30" → "%Y-%m-%d %H:%M"
```

---

## DateTime Indexing

### Setting DateTime as Index

```python
df = pd.DataFrame({
    "date": pd.date_range("2024-01-01", periods=365, freq="D"),
    "sales": np.random.randint(100, 500, 365)
})

# Set date as index
df = df.set_index("date")

# Now you can slice by date!
print(df["2024-03"])           # All of March
print(df["2024-03":"2024-06"]) # March to June
print(df["2024-06-15"])        # Specific day
```

### Date Range Selection

```python
# Select specific range
march_data = df.loc["2024-03-01":"2024-03-31"]

# Select by year
year_2024 = df.loc["2024"]

# Select by month
june = df.loc["2024-06"]
```

---

## Resampling

### Concept: Change the Frequency

```
Resampling = Changing time frequency

Daily data → Monthly summary  (DOWNSAMPLING)
Monthly data → Daily data     (UPSAMPLING)

Daily Sales:
Jan 1: 100       Resample("MS")     Monthly:
Jan 2: 150       ─────────────►     Jan: 450 (sum)
Jan 3: 200                          Feb: 380 (sum)
Feb 1: 180
Feb 2: 200
```

### Downsampling (Higher → Lower frequency)

```python
# Daily data → Monthly sum
df = pd.DataFrame({
    "value": np.random.randint(50, 200, 365)
}, index=pd.date_range("2024-01-01", periods=365, freq="D"))

# Monthly sum
monthly = df.resample("MS").sum()
print(monthly.head())

# Monthly mean
monthly_avg = df.resample("MS").mean()

# Weekly max
weekly_max = df.resample("W").max()

# Quarterly sum
quarterly = df.resample("QS").sum()

# Custom aggregation
monthly_stats = df.resample("MS").agg(["mean", "min", "max", "sum"])
```

### Upsampling (Lower → Higher frequency)

```python
# Monthly data → Daily data
monthly = pd.DataFrame({
    "value": [100, 200, 300]
}, index=pd.date_range("2024-01-01", periods=3, freq="MS"))

# Upsample to daily
daily = monthly.resample("D").asfreq()     # NaN for new dates
daily = monthly.resample("D").ffill()       # Forward fill
daily = monthly.resample("D").interpolate() # Linear interpolation
```

---

## Rolling Windows

### Concept

```
Rolling window = Moving computation over fixed-size window

Data:    [10, 20, 30, 40, 50]
Window:   ↓ size=3

Step 1: [10, 20, 30] → mean = 20
Step 2: [20, 30, 40] → mean = 30
Step 3: [30, 40, 50] → mean = 40

Result: [NaN, NaN, 20, 30, 40]  (first 2 are NaN - not enough data)
```

### Rolling Mean (Moving Average)

```python
df = pd.DataFrame({
    "value": [10, 20, 30, 40, 50, 60, 70]
})

# Rolling mean (window=3)
df["rolling_avg"] = df["value"].rolling(window=3).mean()
print(df)
#    value  rolling_avg
# 0     10          NaN
# 1     20          NaN
# 2     30         20.0  ← (10+20+30)/3
# 3     40         30.0  ← (20+30+40)/3
# 4     50         40.0
# 5     60         50.0
# 6     70         60.0
```

### Other Rolling Operations

```python
# Rolling standard deviation
df["rolling_std"] = df["value"].rolling(3).std()

# Rolling min/max
df["rolling_min"] = df["value"].rolling(3).min()
df["rolling_max"] = df["value"].rolling(3).max()

# Rolling sum
df["rolling_sum"] = df["value"].rolling(3).sum()

# Expanding (cumulative - window grows from start)
df["expanding_mean"] = df["value"].expanding().mean()

# Exponentially weighted (more weight to recent values)
df["ewm_mean"] = df["value"].ewm(span=3).mean()
```

---

## Shifting and Lagging

### Shift

```python
df = pd.DataFrame({
    "value": [100, 150, 200, 180, 220]
}, index=pd.date_range("2024-01-01", periods=5, freq="MS"))

# Shift forward (lag)
df["prev_value"] = df["value"].shift(1)   # Previous period
df["prev2_value"] = df["value"].shift(2)  # Two periods back

# Shift backward (lead)
df["next_value"] = df["value"].shift(-1)  # Next period

print(df)
#             value  prev_value  prev2_value  next_value
# 2024-01-01    100         NaN          NaN       150.0
# 2024-02-01    150       100.0          NaN       200.0
# 2024-03-01    200       150.0        100.0       180.0
# 2024-04-01    180       200.0        150.0       220.0
# 2024-05-01    220       180.0        200.0         NaN
```

### Calculating Changes

```python
# Period-over-period change
df["change"] = df["value"] - df["value"].shift(1)

# Percentage change
df["pct_change"] = df["value"].pct_change() * 100

# Or use the built-in
df["pct_change"] = df["value"].pct_change()
```

---

## Time Zones

```python
# Create timezone-aware timestamp
ts = pd.Timestamp("2024-01-15 14:30", tz="US/Eastern")
print(ts)

# Convert timezone
ts_utc = ts.tz_convert("UTC")
ts_ist = ts.tz_convert("Asia/Kolkata")

# On a Series
df["date"] = pd.to_datetime(df["date"]).dt.tz_localize("UTC")
df["date_ist"] = df["date"].dt.tz_convert("Asia/Kolkata")
```

---

## Traditional vs Pandas Way

### Moving Average

```python
# ======= Traditional Python =======
data = [10, 20, 30, 40, 50, 60, 70]
window = 3

moving_avg = []
for i in range(len(data)):
    if i < window - 1:
        moving_avg.append(None)
    else:
        avg = sum(data[i-window+1:i+1]) / window
        moving_avg.append(avg)

# ======= Pandas Way =======
s = pd.Series(data)
moving_avg = s.rolling(window=3).mean()
```

### Date Grouping

```python
# ======= Traditional Python =======
from collections import defaultdict

sales = [
    {"date": "2024-01-05", "amount": 100},
    {"date": "2024-01-15", "amount": 200},
    {"date": "2024-02-05", "amount": 150},
]

monthly = defaultdict(int)
for sale in sales:
    month = sale["date"][:7]
    monthly[month] += sale["amount"]

# ======= Pandas Way =======
df = pd.DataFrame(sales)
df["date"] = pd.to_datetime(df["date"])
monthly = df.set_index("date").resample("MS")["amount"].sum()
```

---

## Common Mistakes

### 1. Forgetting to Parse Dates

```python
# ❌ WRONG - Dates are strings!
df = pd.read_csv("data.csv")
print(df["date"].dtype)  # object ← String!

# ✅ CORRECT - Parse when reading
df = pd.read_csv("data.csv", parse_dates=["date"])
print(df["date"].dtype)  # datetime64[ns] ✓
```

### 2. Wrong resample Frequency

```python
# ❌ WRONG - "M" is month END, not start
monthly = df.resample("M").sum()   # Groups by month end

# ✅ CORRECT - "MS" for month start
monthly = df.resample("MS").sum()  # Groups by month start
```

### 3. Not Setting Date as Index Before Resample

```python
# ❌ WRONG - resample requires DatetimeIndex
# df.resample("MS").sum()  # Error if date is a column!

# ✅ CORRECT - Set as index first
df = df.set_index("date")
monthly = df.resample("MS").sum()
```

---

## Best Practices

### 1. Always Parse Dates Early
```python
df = pd.read_csv("data.csv", parse_dates=["date"])
```

### 2. Use DatetimeIndex for Time Series
```python
df = df.set_index("date").sort_index()
```

### 3. Use Appropriate Resampling Frequency
```python
# Common frequencies
"D"  → Daily      "W"  → Weekly     "MS" → Month Start
"QS" → Quarter    "YS" → Year Start "h"  → Hourly
"B"  → Business   "min"→ Minute
```

---

## Quick Reference

```python
# DateTime creation
pd.Timestamp("2024-01-15")                    # Single timestamp
pd.date_range("2024-01-01", periods=5, freq="D")  # Range
pd.to_datetime(series)                        # Parse strings

# Properties (.dt accessor)
df["date"].dt.year, .month, .day, .hour
df["date"].dt.day_name(), .quarter

# Resampling
df.resample("MS").sum()      # Monthly sum
df.resample("W").mean()      # Weekly average
df.resample("D").ffill()     # Upsample with forward fill

# Rolling
df["col"].rolling(7).mean()      # 7-day moving average
df["col"].expanding().mean()     # Cumulative average
df["col"].ewm(span=7).mean()    # Exponential moving average

# Shifting
df["col"].shift(1)          # Previous period
df["col"].shift(-1)         # Next period
df["col"].pct_change()      # Percentage change

# Timezones
ts.tz_localize("UTC")       # Set timezone
ts.tz_convert("US/Eastern") # Convert timezone
```

---

[← Previous: Merging & Joining](9-merging-joining.md) | [🏠 Home](README.md) | [Next: Advanced Topics →](11-advanced-topics.md)
