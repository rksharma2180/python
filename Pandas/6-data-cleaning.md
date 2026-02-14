[← Previous: Indexing & Selection](5-indexing-selection.md) | [🏠 Home](README.md) | [Next: Data Transformation →](7-data-transformation.md)

---

# 6. Data Cleaning

## Table of Contents
- [Missing Data](#missing-data)
- [Duplicates](#duplicates)
- [Type Conversion](#type-conversion)
- [Outlier Handling](#outlier-handling)
- [String Cleaning](#string-cleaning)
- [Traditional vs Pandas Way](#traditional-vs-pandas-way)
- [Common Mistakes](#common-mistakes)
- [Best Practices](#best-practices)

---

## Missing Data

### Detecting Missing Values

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "Name": ["Alice", "Bob", None, "Diana", "Eve"],
    "Age": [25, np.nan, 35, 28, np.nan],
    "Salary": [50000, 60000, 70000, np.nan, 62000]
})

# Check for missing values
print(df.isnull())     # True where NaN
print(df.notnull())    # True where NOT NaN

# Count missing per column
print(df.isnull().sum())
# Name      1
# Age       2
# Salary    1

# Percentage missing
print(df.isnull().mean() * 100)
# Name       20.0
# Age        40.0
# Salary     20.0

# Total missing
print(df.isnull().sum().sum())  # 4
```

### Handling Missing Values

```python
# 1. Drop rows with any NaN
df_dropped = df.dropna()

# Drop rows where ALL values are NaN
df_dropped = df.dropna(how="all")

# Drop rows with NaN in specific columns
df_dropped = df.dropna(subset=["Name", "Age"])

# Require minimum non-NaN values
df_dropped = df.dropna(thresh=2)  # Keep rows with at least 2 non-NaN

# 2. Fill missing values
df_filled = df.fillna(0)                    # Fill with constant
df_filled = df.fillna({"Age": 30, "Salary": 55000})  # Column-specific

# Fill with statistics
df["Age"] = df["Age"].fillna(df["Age"].mean())      # Fill with mean
df["Salary"] = df["Salary"].fillna(df["Salary"].median())  # Fill with median

# Forward fill (use previous value)
df_filled = df.fillna(method="ffill")

# Backward fill (use next value)
df_filled = df.fillna(method="bfill")

# Interpolate (linear interpolation)
df["Age"] = df["Age"].interpolate()
```

### Internal Flow: Missing Data Handling

```
                    Missing Data Found
                         │
           ┌─────────────┼─────────────┐
           │             │             │
         Drop         Fill          Interpolate
           │             │             │
     ┌─────┴─────┐  ┌───┴───┐    Linear/Polynomial
     │           │  │       │
   dropna()   dropna  fillna  fillna(method)
   (any)      (thresh) (value)  ffill/bfill
```

---

## Duplicates

### Detecting Duplicates

```python
df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Alice", "Charlie", "Bob"],
    "Age": [25, 30, 25, 35, 30],
    "Dept": ["IT", "HR", "IT", "IT", "HR"]
})

# Find duplicate rows
print(df.duplicated())
# 0    False
# 1    False
# 2     True  ← Duplicate of row 0
# 3    False
# 4     True  ← Duplicate of row 1

# Count duplicates
print(df.duplicated().sum())  # 2

# Find duplicates based on specific columns
print(df.duplicated(subset=["Name"]))  # Only check Name column
```

### Removing Duplicates

```python
# Remove all duplicates (keep first occurrence)
df_clean = df.drop_duplicates()

# Keep last occurrence
df_clean = df.drop_duplicates(keep="last")

# Remove based on specific columns
df_clean = df.drop_duplicates(subset=["Name"])

# Keep no duplicates (remove all copies)
df_clean = df.drop_duplicates(keep=False)
```

---

## Type Conversion

### Checking Types

```python
df = pd.DataFrame({
    "id": ["1", "2", "3"],
    "price": ["99.99", "149.50", "79.99"],
    "active": ["True", "False", "True"],
    "date": ["2024-01-15", "2024-02-20", "2024-03-10"]
})

print(df.dtypes)
# id        object  ← String, should be int
# price     object  ← String, should be float
# active    object  ← String, should be bool
# date      object  ← String, should be datetime
```

### Converting Types

```python
# String to numeric
df["id"] = df["id"].astype(int)
df["price"] = df["price"].astype(float)

# String to boolean
df["active"] = df["active"].map({"True": True, "False": False})

# String to datetime
df["date"] = pd.to_datetime(df["date"])

# Safe conversion (handles errors)
df["price"] = pd.to_numeric(df["price"], errors="coerce")  # NaN for bad values

# Category type (saves memory for repeated strings)
df["status"] = df["status"].astype("category")

print(df.dtypes)
# id          int64
# price     float64
# active       bool
# date    datetime64[ns]
```

### Conversion Flow

```
Original: "123"  (object/string)
           │
    ┌──────┴──────┐
    │             │
  astype()    pd.to_numeric()
    │             │
  int(123)    123 or NaN
              (errors="coerce")
```

---

## Outlier Handling

### Detecting Outliers

```python
data = pd.DataFrame({
    "Value": [10, 12, 11, 13, 100, 9, 11, 12, 150, 10]
})

# Method 1: IQR (Interquartile Range)
Q1 = data["Value"].quantile(0.25)
Q3 = data["Value"].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = data[(data["Value"] < lower_bound) | (data["Value"] > upper_bound)]
print("Outliers:", outliers)

# Method 2: Z-score
mean = data["Value"].mean()
std = data["Value"].std()
z_scores = (data["Value"] - mean) / std
outliers = data[z_scores.abs() > 2]
```

### Handling Outliers

```python
# Option 1: Remove
df_clean = data[(data["Value"] >= lower_bound) & (data["Value"] <= upper_bound)]

# Option 2: Cap (winsorize)
data["Value"] = data["Value"].clip(lower=lower_bound, upper=upper_bound)

# Option 3: Replace with NaN
data.loc[(data["Value"] < lower_bound) | (data["Value"] > upper_bound), "Value"] = np.nan
```

---

## String Cleaning

```python
df = pd.DataFrame({
    "Name": ["  Alice  ", "BOB", "charlie", "  Diana"],
    "Email": ["Alice@Gmail.COM", "bob@yahoo", "CHARLIE@GMAIL.COM", None],
    "Phone": ["123-456-7890", "(123) 456 7890", "1234567890", "123.456.7890"]
})

# Strip whitespace
df["Name"] = df["Name"].str.strip()

# Consistent case
df["Name"] = df["Name"].str.title()
df["Email"] = df["Email"].str.lower()

# Replace patterns
df["Phone"] = df["Phone"].str.replace(r"[^\d]", "", regex=True)
# All become: "1234567890"

# Check format
df["valid_email"] = df["Email"].str.contains(r"@.*\.", regex=True, na=False)
```

---

## Traditional vs Pandas Way

### Handling Missing Values

```python
# ======= Traditional Python =======
data = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": None},
    {"name": "Charlie", "age": 35}
]

# Remove missing
clean = [d for d in data if d["age"] is not None]

# Fill missing with average
ages = [d["age"] for d in data if d["age"] is not None]
avg_age = sum(ages) / len(ages)
for d in data:
    if d["age"] is None:
        d["age"] = avg_age

# ======= Pandas Way =======
df = pd.DataFrame(data)
df["age"] = df["age"].fillna(df["age"].mean())  # One line!
```

### Removing Duplicates

```python
# ======= Traditional Python =======
seen = set()
unique = []
for item in data:
    key = (item["name"], item["age"])
    if key not in seen:
        seen.add(key)
        unique.append(item)

# ======= Pandas Way =======
df = df.drop_duplicates()  # One line!
```

---

## Common Mistakes

### 1. Not Using inplace or Reassigning

```python
# ❌ WRONG - Original unchanged
df.dropna()
df.fillna(0)

# ✅ CORRECT
df = df.dropna()             # Option 1: Reassign
df.dropna(inplace=True)      # Option 2: inplace
```

### 2. Filling All Columns with Same Value

```python
# ❌ WRONG - Filling text column with number
df.fillna(0)  # "Name" column gets 0 too!

# ✅ CORRECT - Column-specific fills
df.fillna({"Name": "Unknown", "Age": df["Age"].mean(), "Salary": 0})
```

### 3. Dropping Too Many Rows

```python
# ❌ WRONG - May lose too much data
df.dropna()  # Drops row if ANY column has NaN

# ✅ CORRECT - Be selective
df.dropna(subset=["critical_column"])  # Only drop if critical column is NaN
```

---

## Best Practices

### 1. Audit Missing Data First
```python
# ✅ Always check the pattern of missing data
print(df.isnull().sum())
print(df.isnull().mean() * 100)  # Percentage
```

### 2. Document Your Cleaning Steps
```python
# ✅ Track what you changed
print(f"Before cleaning: {len(df)} rows")
df = df.dropna(subset=["Name"])
print(f"After dropping Name NaN: {len(df)} rows")
df = df.drop_duplicates()
print(f"After removing duplicates: {len(df)} rows")
```

### 3. Create a Cleaning Pipeline
```python
def clean_data(df):
    """Standard cleaning pipeline"""
    df = df.copy()
    df = df.drop_duplicates()
    df["Name"] = df["Name"].str.strip().str.title()
    df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
    df["Age"] = df["Age"].fillna(df["Age"].median())
    return df
```

---

## Quick Reference

```python
# Missing data
df.isnull().sum()              # Count per column
df.dropna()                    # Drop rows with NaN
df.dropna(subset=["col"])     # Drop if specific col is NaN
df.fillna(value)              # Fill with value
df.fillna(method="ffill")     # Forward fill
df.interpolate()              # Interpolate

# Duplicates
df.duplicated().sum()          # Count duplicates
df.drop_duplicates()           # Remove duplicates
df.drop_duplicates(subset=[])  # By specific columns

# Type conversion
df["col"].astype(int)          # Convert type
pd.to_numeric(df["col"], errors="coerce")  # Safe numeric
pd.to_datetime(df["col"])     # To datetime

# String cleaning
df["col"].str.strip()          # Remove whitespace
df["col"].str.lower()          # Lowercase
df["col"].str.replace("a","b") # Replace
df["col"].str.contains("x")   # Check pattern

# Outliers
df["col"].clip(lower, upper)   # Cap values
```

---

[← Previous: Indexing & Selection](5-indexing-selection.md) | [🏠 Home](README.md) | [Next: Data Transformation →](7-data-transformation.md)
