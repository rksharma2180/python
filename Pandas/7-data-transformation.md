[← Previous: Data Cleaning](6-data-cleaning.md) | [🏠 Home](README.md) | [Next: Grouping & Aggregation →](8-grouping-aggregation.md)

---

# 7. Data Transformation

## Table of Contents
- [Apply and Map](#apply-and-map)
- [Lambda Functions](#lambda-functions)
- [Replacing Values](#replacing-values)
- [Sorting](#sorting)
- [Ranking](#ranking)
- [String Operations](#string-operations)
- [Traditional vs Pandas Way](#traditional-vs-pandas-way)
- [Common Mistakes](#common-mistakes)
- [Best Practices](#best-practices)

---

## Apply and Map

### apply() - Most Versatile

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "Salary": [50000, 60000, 70000]
})

# Apply function to a column (Series)
def categorize_age(age):
    if age < 28:
        return "Junior"
    elif age < 33:
        return "Mid"
    else:
        return "Senior"

df["Level"] = df["Age"].apply(categorize_age)
print(df)
#       Name  Age  Salary   Level
# 0    Alice   25   50000  Junior
# 1      Bob   30   60000     Mid
# 2  Charlie   35   70000  Senior

# Apply function to entire DataFrame (row-wise)
def total_comp(row):
    return row["Salary"] + row["Salary"] * 0.1

df["TotalComp"] = df.apply(total_comp, axis=1)
```

### map() - Series Only

```python
# map() works on Series only (not DataFrame)

# With a function
df["Name_upper"] = df["Name"].map(str.upper)

# With a dictionary (lookup/replace)
dept_map = {"Alice": "IT", "Bob": "HR", "Charlie": "IT"}
df["Dept"] = df["Name"].map(dept_map)

# With a lambda
df["Age_doubled"] = df["Age"].map(lambda x: x * 2)
```

### applymap() / map() on DataFrame

```python
# Apply function to every element in DataFrame
# In Pandas 2.1+, use df.map() instead of df.applymap()
numeric_df = df[["Age", "Salary"]]
formatted = numeric_df.map(lambda x: f"${x:,.2f}" if isinstance(x, (int, float)) else x)
print(formatted)
```

### apply vs map vs applymap

```
┌──────────────┬───────────────────┬────────────────────┐
│   Method     │   Works On        │   Use Case         │
├──────────────┼───────────────────┼────────────────────┤
│ .apply()     │ Series or         │ Custom function    │
│              │ DataFrame         │ on column/row      │
├──────────────┼───────────────────┼────────────────────┤
│ .map()       │ Series only       │ Element-wise       │
│              │                   │ substitution       │
├──────────────┼───────────────────┼────────────────────┤
│ .map()       │ DataFrame         │ Element-wise on    │
│ (Pandas 2.1+)│                   │ entire DataFrame   │
└──────────────┴───────────────────┴────────────────────┘
```

---

## Lambda Functions

```python
# Lambda with apply
df["Tax"] = df["Salary"].apply(lambda x: x * 0.3 if x > 55000 else x * 0.2)

# Lambda with multiple columns
df["Label"] = df.apply(
    lambda row: f"{row['Name']} ({row['Age']})", axis=1
)

# Lambda with conditions
df["Category"] = df["Salary"].apply(
    lambda x: "High" if x > 60000 else "Medium" if x > 50000 else "Low"
)
```

---

## Replacing Values

### Simple Replace

```python
df = pd.DataFrame({
    "Grade": ["A", "B", "C", "A", "F", "B"],
    "Score": [90, 80, 70, 95, 40, 85]
})

# Replace single value
df["Grade"] = df["Grade"].replace("F", "Fail")

# Replace multiple values
df["Grade"] = df["Grade"].replace({"A": "Excellent", "B": "Good", "C": "Average"})

# Replace with regex
df["Grade"] = df["Grade"].replace(r"^F.*", "Failed", regex=True)
```

### Conditional Replace with np.where

```python
# Binary condition
df["Pass"] = np.where(df["Score"] >= 50, "Pass", "Fail")

# Multiple conditions with np.select
conditions = [
    df["Score"] >= 90,
    df["Score"] >= 70,
    df["Score"] >= 50,
    df["Score"] < 50
]
choices = ["A", "B", "C", "F"]
df["Grade"] = np.select(conditions, choices)
```

### Binning with pd.cut

```python
# Create bins
df["Score_Band"] = pd.cut(df["Score"], bins=[0, 50, 70, 90, 100],
                           labels=["Fail", "Average", "Good", "Excellent"])

# Equal-width bins
df["Score_Band"] = pd.cut(df["Score"], bins=4)  # 4 equal ranges

# Equal-frequency bins
df["Score_Band"] = pd.qcut(df["Score"], q=4, labels=["Q1", "Q2", "Q3", "Q4"])
```

---

## Sorting

```python
df = pd.DataFrame({
    "Name": ["Charlie", "Alice", "Bob", "Diana"],
    "Age": [35, 25, 30, 28],
    "Salary": [70000, 50000, 60000, 50000]
})

# Sort by single column
df_sorted = df.sort_values("Age")

# Sort descending
df_sorted = df.sort_values("Age", ascending=False)

# Sort by multiple columns
df_sorted = df.sort_values(["Salary", "Age"], ascending=[False, True])
# First by Salary (desc), then by Age (asc) for ties

# Sort by index
df_sorted = df.sort_index()

# Get top/bottom N
top3 = df.nlargest(3, "Salary")
bottom3 = df.nsmallest(3, "Age")
```

---

## Ranking

```python
df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Score": [85, 92, 85, 95]
})

# Default ranking (average for ties)
df["Rank"] = df["Score"].rank(ascending=False)
print(df)
#       Name  Score  Rank
# 0    Alice     85   3.5  ← Tied, average of 3 and 4
# 1      Bob     92   2.0
# 2  Charlie     85   3.5  ← Tied
# 3    Diana     95   1.0

# Different tie-breaking methods
df["Rank_min"] = df["Score"].rank(method="min", ascending=False)    # [3, 2, 3, 1]
df["Rank_max"] = df["Score"].rank(method="max", ascending=False)    # [4, 2, 4, 1]
df["Rank_first"] = df["Score"].rank(method="first", ascending=False) # [3, 2, 4, 1]
df["Rank_dense"] = df["Score"].rank(method="dense", ascending=False) # [3, 2, 3, 1]
```

---

## String Operations

### Common String Methods

```python
df = pd.DataFrame({
    "Name": ["Alice Smith", "Bob Jones", "Charlie Brown"],
    "Email": ["alice@company.com", "bob@test.org", "charlie@company.com"]
})

# Case
df["upper"] = df["Name"].str.upper()
df["lower"] = df["Name"].str.lower()
df["title"] = df["Name"].str.title()

# Split
df["First"] = df["Name"].str.split(" ").str[0]
df["Last"] = df["Name"].str.split(" ").str[1]

# Contains
df["is_company"] = df["Email"].str.contains("company")

# Extract with regex
df["Domain"] = df["Email"].str.extract(r"@(.+)$")

# Length
df["Name_len"] = df["Name"].str.len()

# Pad/Justify
df["ID"] = pd.Series([1, 2, 3]).astype(str).str.zfill(5)  # "00001"
```

### Traditional vs Pandas

```python
# ======= Traditional Python =======
names = ["alice smith", "bob jones", "charlie brown"]
first_names = [n.split(" ")[0].title() for n in names]

# ======= Pandas Way =======
s = pd.Series(names)
first_names = s.str.split(" ").str[0].str.title()
```

---

## Traditional vs Pandas Way

### Complex Transformation

```python
employees = [
    {"name": "Alice", "salary": 50000, "dept": "IT"},
    {"name": "Bob", "salary": 60000, "dept": "HR"},
    {"name": "Charlie", "salary": 70000, "dept": "IT"},
]

# ======= Traditional Python =======
# Add bonus and tax columns
for emp in employees:
    emp["bonus"] = emp["salary"] * 0.1
    emp["tax"] = emp["salary"] * 0.3 if emp["salary"] > 55000 else emp["salary"] * 0.2
    emp["net"] = emp["salary"] + emp["bonus"] - emp["tax"]

# ======= Pandas Way =======
df = pd.DataFrame(employees)
df["bonus"] = df["salary"] * 0.1
df["tax"] = np.where(df["salary"] > 55000, df["salary"] * 0.3, df["salary"] * 0.2)
df["net"] = df["salary"] + df["bonus"] - df["tax"]
```

---

## Common Mistakes

### 1. Using apply When Vectorized Exists

```python
# ❌ BAD - Slow
df["double"] = df["Salary"].apply(lambda x: x * 2)

# ✅ GOOD - Vectorized (much faster!)
df["double"] = df["Salary"] * 2
```

### 2. Not Using axis in apply

```python
# ❌ WRONG - Applies to columns by default (axis=0)
df.apply(lambda row: row["A"] + row["B"])  # Error!

# ✅ CORRECT - Specify axis=1 for row-wise
df.apply(lambda row: row["A"] + row["B"], axis=1)
```

### 3. Modifying Original with apply

```python
# ❌ BAD - Side effects in apply
def bad_func(x):
    some_list.append(x)  # Side effect!
    return x * 2

# ✅ GOOD - Pure functions
def good_func(x):
    return x * 2
```

---

## Best Practices

### 1. Prefer Vectorized Operations
```python
# ✅ Speed ranking:
# 1. Vectorized operations (fastest)
df["result"] = df["A"] * 2 + df["B"]

# 2. np.where for conditions
df["result"] = np.where(df["A"] > 0, df["A"], 0)

# 3. .apply() (slowest - use only when needed)
df["result"] = df["A"].apply(custom_function)
```

### 2. Use Categorical for Repeated Strings
```python
df["Status"] = df["Status"].astype("category")  # Saves memory
```

### 3. Chain Transformations
```python
result = (df
    .assign(bonus=lambda x: x["Salary"] * 0.1)
    .assign(total=lambda x: x["Salary"] + x["bonus"])
    .query("total > 60000")
    .sort_values("total", ascending=False)
)
```

---

## Quick Reference

```python
# Apply/Map
df["col"].apply(func)             # Apply to column
df.apply(func, axis=1)           # Apply row-wise
df["col"].map(dict_or_func)      # Map values

# Replace
df["col"].replace(old, new)      # Replace values
np.where(cond, true, false)      # Conditional
np.select(conditions, choices)   # Multiple conditions
pd.cut(col, bins, labels)       # Binning

# Sort
df.sort_values("col")            # Sort by column
df.nlargest(n, "col")            # Top N
df.nsmallest(n, "col")           # Bottom N

# Rank
df["col"].rank()                 # Rank values

# String
df["col"].str.upper()            # Uppercase
df["col"].str.split(" ")         # Split
df["col"].str.contains("x")     # Search
df["col"].str.extract(r"regex")  # Extract
```

---

[← Previous: Data Cleaning](6-data-cleaning.md) | [🏠 Home](README.md) | [Next: Grouping & Aggregation →](8-grouping-aggregation.md)
