[← Previous: Data Transformation](7-data-transformation.md) | [🏠 Home](README.md) | [Next: Merging & Joining →](9-merging-joining.md)

---

# 8. Grouping & Aggregation

## Table of Contents
- [GroupBy Basics](#groupby-basics)
- [Aggregation Functions](#aggregation-functions)
- [Multiple Aggregations](#multiple-aggregations)
- [Pivot Tables](#pivot-tables)
- [Crosstab](#crosstab)
- [Internal Working](#internal-working)
- [Traditional vs Pandas Way](#traditional-vs-pandas-way)
- [Common Mistakes](#common-mistakes)
- [Best Practices](#best-practices)

---

## GroupBy Basics

### Concept: Split → Apply → Combine

```
Original DataFrame
┌──────────┬───────┬────────┐
│   Name   │ Dept  │ Salary │
├──────────┼───────┼────────┤
│  Alice   │  IT   │ 50000  │
│  Bob     │  HR   │ 60000  │
│  Charlie │  IT   │ 70000  │
│  Diana   │  HR   │ 55000  │
│  Eve     │  IT   │ 62000  │
└──────────┴───────┴────────┘

             groupby("Dept")
                  │
         ┌────────┴────────┐
         ▼                 ▼
   ┌─── IT ───┐     ┌─── HR ───┐     ← SPLIT
   │ Alice 50k│     │ Bob  60k │
   │ Charlie 70│     │ Diana 55│
   │ Eve   62k│     └─────────┘
   └──────────┘
         │                 │
     mean()            mean()           ← APPLY
         │                 │
        60667            57500
         │                 │
         └────────┬────────┘
                  ▼                     ← COMBINE
   ┌──────────┬─────────┐
   │   Dept   │  Salary │
   ├──────────┼─────────┤
   │    IT    │  60667  │
   │    HR    │  57500  │
   └──────────┴─────────┘
```

### Basic GroupBy

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "Dept": ["IT", "HR", "IT", "HR", "IT"],
    "Salary": [50000, 60000, 70000, 55000, 62000],
    "Age": [25, 30, 35, 28, 32],
})

# Group by single column
grouped = df.groupby("Dept")

# This returns a GroupBy object (lazy - no computation yet)
print(type(grouped))  # <class 'DataFrameGroupBy'>

# Now apply aggregation
print(grouped["Salary"].mean())
# Dept
# HR    57500.0
# IT    60666.7

# Group by + aggregate directly
print(df.groupby("Dept")["Salary"].mean())
```

### Multiple Group Columns

```python
df = pd.DataFrame({
    "Dept": ["IT", "IT", "HR", "HR", "IT", "HR"],
    "Level": ["Junior", "Senior", "Junior", "Senior", "Senior", "Junior"],
    "Salary": [50000, 80000, 45000, 75000, 85000, 48000]
})

# Group by multiple columns
print(df.groupby(["Dept", "Level"])["Salary"].mean())
# Dept  Level
# HR    Junior    46500.0
#       Senior    75000.0
# IT    Junior    50000.0
#       Senior    82500.0
```

---

## Aggregation Functions

### Built-in Aggregations

```python
grouped = df.groupby("Dept")["Salary"]

print(grouped.sum())       # Total per group
print(grouped.mean())      # Average per group
print(grouped.median())    # Median per group
print(grouped.min())       # Minimum per group
print(grouped.max())       # Maximum per group
print(grouped.count())     # Count per group
print(grouped.std())       # Standard deviation
print(grouped.var())       # Variance
print(grouped.first())     # First value per group
print(grouped.last())      # Last value per group
```

### Custom Aggregation

```python
# Apply custom function
def salary_range(x):
    return x.max() - x.min()

print(df.groupby("Dept")["Salary"].apply(salary_range))
# or
print(df.groupby("Dept")["Salary"].agg(salary_range))
```

---

## Multiple Aggregations

### agg() with Multiple Functions

```python
# Multiple aggregations on one column
result = df.groupby("Dept")["Salary"].agg(["mean", "min", "max", "count"])
print(result)
#          mean    min    max  count
# Dept
# HR    57500  55000  60000      2
# IT    60667  50000  70000      3
```

### Different Aggregations per Column

```python
# Different functions for different columns
result = df.groupby("Dept").agg({
    "Salary": ["mean", "max"],
    "Age": ["min", "max", "mean"]
})
print(result)
#       Salary          Age
#         mean    max  min  max   mean
# Dept
# HR    57500  60000   28   30  29.0
# IT    60667  70000   25   35  30.67
```

### Named Aggregations (Clean Output)

```python
# Named aggregation (recommended - cleaner column names)
result = df.groupby("Dept").agg(
    avg_salary=("Salary", "mean"),
    max_salary=("Salary", "max"),
    min_age=("Age", "min"),
    headcount=("Name", "count")
)
print(result)
#       avg_salary  max_salary  min_age  headcount
# Dept
# HR       57500.0       60000       28          2
# IT       60666.7       70000       25          3
```

---

## Pivot Tables

### Basic Pivot Table

```python
df = pd.DataFrame({
    "Date": ["2024-01", "2024-01", "2024-02", "2024-02", "2024-01", "2024-02"],
    "Dept": ["IT", "HR", "IT", "HR", "IT", "HR"],
    "Sales": [100, 150, 200, 180, 120, 160]
})

# Pivot table
pivot = pd.pivot_table(df,
    values="Sales",      # Values to aggregate
    index="Dept",        # Rows
    columns="Date",      # Columns
    aggfunc="sum"        # Aggregation function
)
print(pivot)
# Date     2024-01  2024-02
# Dept
# HR          150      340
# IT          220      200
```

### Advanced Pivot Table

```python
# Multiple aggregations
pivot = pd.pivot_table(df,
    values="Sales",
    index="Dept",
    columns="Date",
    aggfunc=["sum", "mean", "count"],
    fill_value=0,         # Fill NaN with 0
    margins=True          # Add row/column totals
)
```

### Pivot Table Flow

```
Original Data:                  Pivot Table:
┌────────┬──────┬───────┐       ┌──────┬─────────┬─────────┐
│  Date  │ Dept │ Sales │       │ Dept │ 2024-01 │ 2024-02 │
├────────┼──────┼───────┤  ──►  ├──────┼─────────┼─────────┤
│ 2024-01│  IT  │  100  │       │  HR  │   150   │   340   │
│ 2024-01│  HR  │  150  │       │  IT  │   220   │   200   │
│ 2024-02│  IT  │  200  │       └──────┴─────────┴─────────┘
│ 2024-02│  HR  │  180  │
│ 2024-01│  IT  │  120  │       Rows: Dept
│ 2024-02│  HR  │  160  │       Cols: Date
└────────┴──────┴───────┘       Values: sum(Sales)
```

---

## Crosstab

```python
df = pd.DataFrame({
    "Dept": ["IT", "HR", "IT", "HR", "IT", "IT"],
    "Level": ["Junior", "Senior", "Senior", "Junior", "Junior", "Senior"],
    "Gender": ["M", "F", "M", "F", "F", "M"]
})

# Simple crosstab (frequency count)
print(pd.crosstab(df["Dept"], df["Level"]))
# Level   Junior  Senior
# Dept
# HR           1       1
# IT           2       2

# With margins (totals)
print(pd.crosstab(df["Dept"], df["Level"], margins=True))

# Normalized (percentages)
print(pd.crosstab(df["Dept"], df["Level"], normalize=True))

# With values and aggregation
print(pd.crosstab(df["Dept"], df["Level"], values=df["Gender"],
                   aggfunc="count"))
```

---

## Internal Working

### GroupBy is Lazy

```python
# GroupBy doesn't compute anything immediately
grouped = df.groupby("Dept")  # Just creates a mapping

# Internally it creates:
# {
#   "HR": [index_1, index_3],  ← Stores indices, not data
#   "IT": [index_0, index_2, index_4]
# }

# Computation happens only when you call an aggregation
result = grouped.mean()  # NOW it computes per group
```

### Iterating Over Groups

```python
for name, group in df.groupby("Dept"):
    print(f"\n--- {name} ---")
    print(group)

# Get specific group
it_dept = grouped.get_group("IT")
```

---

## Traditional vs Pandas Way

### Group and Aggregate

```python
# ======= Traditional Python =======
from collections import defaultdict

employees = [
    {"dept": "IT", "salary": 50000},
    {"dept": "HR", "salary": 60000},
    {"dept": "IT", "salary": 70000},
    {"dept": "HR", "salary": 55000},
]

# Average salary by department
dept_salaries = defaultdict(list)
for emp in employees:
    dept_salaries[emp["dept"]].append(emp["salary"])

avg_salary = {}
for dept, salaries in dept_salaries.items():
    avg_salary[dept] = sum(salaries) / len(salaries)

print(avg_salary)  # {'IT': 60000.0, 'HR': 57500.0}

# ======= Pandas Way =======
df = pd.DataFrame(employees)
print(df.groupby("dept")["salary"].mean())
# One line!
```

### Pivot Table

```python
# ======= Traditional Python =======
# Creating a cross-tabulation manually is extremely verbose
# Requires nested dictionaries, multiple loops, etc.

# ======= Pandas Way =======
pd.pivot_table(df, values="sales", index="dept", columns="month", aggfunc="sum")
# One line!
```

---

## Common Mistakes

### 1. Forgetting reset_index()

```python
# GroupBy result has grouped column as index
result = df.groupby("Dept")["Salary"].mean()
# Dept is now the index, not a column!

# ✅ CORRECT - Reset to get Dept as column
result = df.groupby("Dept")["Salary"].mean().reset_index()
#   Dept   Salary
# 0   HR  57500.0
# 1   IT  60666.7
```

### 2. Aggregating Non-Numeric Columns

```python
# ❌ WRONG - Can't take mean of strings
# df.groupby("Dept").mean()  # Warning for string columns!

# ✅ CORRECT - Select numeric columns
df.groupby("Dept")[["Salary", "Age"]].mean()

# Or use numeric_only
df.groupby("Dept").mean(numeric_only=True)
```

### 3. Using Wrong Aggregation

```python
# ❌ WRONG - count() vs size()
df.groupby("Dept").count()   # Count non-NaN per column
df.groupby("Dept").size()    # Count all rows per group (including NaN)

# Use size() for group sizes, count() for non-null counts
```

---

## Best Practices

### 1. Use Named Aggregations
```python
# ✅ Clean, readable output
result = df.groupby("Dept").agg(
    avg_salary=("Salary", "mean"),
    headcount=("Name", "count")
)
```

### 2. Use as_index=False
```python
# ✅ Keep group columns as regular columns
result = df.groupby("Dept", as_index=False)["Salary"].mean()
# Same as .reset_index() but cleaner
```

### 3. Filter Groups
```python
# Keep only groups with more than 2 members
result = df.groupby("Dept").filter(lambda x: len(x) > 2)
```

---

## Quick Reference

```python
# GroupBy
df.groupby("col")["val"].mean()        # Basic group + aggregate
df.groupby(["c1","c2"])["val"].sum()   # Multiple group columns

# Aggregations
.sum(), .mean(), .median(), .min(), .max()
.count(), .std(), .var(), .first(), .last()

# Multiple aggregations
df.groupby("col").agg(["mean","max"])
df.groupby("col").agg(name=("col","func"))  # Named

# Pivot table
pd.pivot_table(df, values, index, columns, aggfunc)

# Crosstab
pd.crosstab(df["col1"], df["col2"])

# Utility
grouped.get_group("name")            # Get single group
grouped.filter(lambda x: len(x) > 2) # Filter groups
grouped.transform("mean")            # Broadcast result
```

---

[← Previous: Data Transformation](7-data-transformation.md) | [🏠 Home](README.md) | [Next: Merging & Joining →](9-merging-joining.md)
