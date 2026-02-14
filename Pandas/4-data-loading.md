[← Previous: DataFrames](3-dataframes.md) | [🏠 Home](README.md) | [Next: Indexing & Selection →](5-indexing-selection.md)

---

# 4. Data Loading & Export

## Table of Contents
- [Reading CSV Files](#reading-csv-files)
- [Reading Excel Files](#reading-excel-files)
- [Reading JSON](#reading-json)
- [Writing/Exporting Data](#writingexporting-data)
- [Traditional vs Pandas Way](#traditional-vs-pandas-way)
- [Common Mistakes](#common-mistakes)
- [Best Practices](#best-practices)

---

## Reading CSV Files

### Basic CSV Read

```python
import pandas as pd

# Simple read
df = pd.read_csv("data.csv")

# With options
df = pd.read_csv("data.csv",
    sep=",",              # Delimiter (default: comma)
    header=0,             # Row number for column names (default: 0)
    index_col=None,       # Column to use as index
    usecols=["Name", "Age"],  # Read only specific columns
    nrows=100,            # Read only first 100 rows
    skiprows=5,           # Skip first 5 rows
    na_values=["N/A", ""], # Custom NaN markers
    encoding="utf-8",     # Encoding
    dtype={"Age": int}    # Force column types
)
```

### Reading Large Files

```python
# Read in chunks (for files too large for memory)
chunks = pd.read_csv("huge_file.csv", chunksize=10000)

# Process each chunk
results = []
for chunk in chunks:
    # Process each chunk
    result = chunk[chunk["value"] > 100]
    results.append(result)

final_df = pd.concat(results)
```

### CSV with Different Formats

```python
# Tab-separated
df = pd.read_csv("data.tsv", sep="\t")

# Semicolon-separated
df = pd.read_csv("data.csv", sep=";")

# No header row
df = pd.read_csv("data.csv", header=None, names=["A", "B", "C"])

# Skip bad lines
df = pd.read_csv("data.csv", on_bad_lines="skip")
```

---

## Reading Excel Files

```python
# Basic read (requires openpyxl)
# pip install openpyxl
df = pd.read_excel("data.xlsx")

# Specific sheet
df = pd.read_excel("data.xlsx", sheet_name="Sheet2")

# Multiple sheets
all_sheets = pd.read_excel("data.xlsx", sheet_name=None)
# Returns dict: {"Sheet1": df1, "Sheet2": df2, ...}

# With options
df = pd.read_excel("data.xlsx",
    header=0,
    usecols="A:D",          # Excel column range
    skiprows=2,
    nrows=100
)
```

---

## Reading JSON

```python
# From JSON file
df = pd.read_json("data.json")

# From JSON string
json_str = '[{"Name": "Alice", "Age": 25}, {"Name": "Bob", "Age": 30}]'
df = pd.read_json(json_str)

# Nested JSON (common with APIs)
import json

with open("nested.json") as f:
    data = json.load(f)

# Normalize nested JSON to flat table
df = pd.json_normalize(data)

# Deeply nested
df = pd.json_normalize(data, record_path="items",
                        meta=["store_name", "location"])
```

---

## Writing/Exporting Data

### To CSV

```python
# Basic write
df.to_csv("output.csv")

# Without index
df.to_csv("output.csv", index=False)

# With options
df.to_csv("output.csv",
    sep=",",
    index=False,
    columns=["Name", "Age"],    # Only specific columns
    na_rep="NULL",               # Replace NaN with string
    encoding="utf-8"
)
```

### To Excel

```python
# Basic write
df.to_excel("output.xlsx", index=False)

# Multiple sheets
with pd.ExcelWriter("output.xlsx") as writer:
    df1.to_excel(writer, sheet_name="Employees")
    df2.to_excel(writer, sheet_name="Departments")
```

### To JSON

```python
# To JSON string
json_str = df.to_json()

# To JSON file
df.to_json("output.json", orient="records", indent=2)

# orient options:
# "records" → [{col: val}, ...]  (most common)
# "columns" → {col: {idx: val}}
# "index"   → {idx: {col: val}}
```

### To Other Formats

```python
# To dictionary
data_dict = df.to_dict()
data_dict = df.to_dict(orient="records")  # List of dicts

# To NumPy array
arr = df.to_numpy()
arr = df.values  # Same thing

# To clipboard (for pasting)
df.to_clipboard()

# To HTML
html = df.to_html()

# To string (for printing)
print(df.to_string())
```

---

## Traditional vs Pandas Way

### Reading CSV

```python
# ======= Traditional Python =======
import csv

data = []
with open("data.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append(row)

# Problem: Everything is strings!
# Must manually convert: int(row["Age"]), float(row["Salary"])

# ======= Pandas Way =======
df = pd.read_csv("data.csv")
# Done! Types auto-detected ✓
```

### Reading JSON

```python
# ======= Traditional Python =======
import json

with open("data.json") as f:
    data = json.load(f)

# Now you have a list of dicts, manual processing needed

# ======= Pandas Way =======
df = pd.read_json("data.json")
# Ready for analysis! ✓
```

### Writing CSV

```python
# ======= Traditional Python =======
import csv

with open("output.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Age"])
    for person in people:
        writer.writerow([person["name"], person["age"]])

# ======= Pandas Way =======
df.to_csv("output.csv", index=False)
```

---

## Internal Working

### How read_csv Works

```
┌──────────────────────────────────────┐
│           pd.read_csv()             │
│                                      │
│  1. Open file handle                │
│  2. Detect delimiter (if not given) │
│  3. Parse header row → column names │
│  4. Read data in chunks             │
│  5. Infer dtypes per column         │
│  6. Build Block Manager             │
│  7. Return DataFrame                │
└──────────────────────────────────────┘

Key: Step 5 (dtype inference) can be slow!
Tip: Specify dtypes explicitly for large files
```

```python
# Faster for large files - skip inference
df = pd.read_csv("large.csv", dtype={
    "id": "int32",
    "name": "string",
    "value": "float32"
})
```

---

## Common Mistakes

### 1. Forgetting index=False When Writing

```python
# ❌ WRONG - Writes index as extra column
df.to_csv("output.csv")
# Output: ,Name,Age
#         0,Alice,25
#         1,Bob,30

# ✅ CORRECT
df.to_csv("output.csv", index=False)
# Output: Name,Age
#         Alice,25
#         Bob,30
```

### 2. Not Handling Encoding

```python
# ❌ WRONG - May fail with special characters
df = pd.read_csv("data.csv")

# ✅ CORRECT - Specify encoding
df = pd.read_csv("data.csv", encoding="utf-8")
# or encoding="latin1" for older files
```

### 3. Loading Entire File When You Need a Subset

```python
# ❌ BAD - Loads everything into memory
df = pd.read_csv("huge_10gb.csv")

# ✅ GOOD - Load only what you need
df = pd.read_csv("huge_10gb.csv",
    usecols=["Name", "Age"],
    nrows=1000
)
```

---

## Best Practices

### 1. Preview Before Loading
```python
# Read just first 5 rows to check structure
df_preview = pd.read_csv("data.csv", nrows=5)
print(df_preview.info())
```

### 2. Specify dtypes for Large Files
```python
df = pd.read_csv("data.csv", dtype={"zip_code": str, "count": "int32"})
```

### 3. Use Parquet for Large Data
```python
# Parquet is faster and smaller than CSV
df.to_parquet("data.parquet")        # Write
df = pd.read_parquet("data.parquet")  # Read (much faster!)
```

---

## Quick Reference

```python
# Reading
pd.read_csv("file.csv")            # CSV
pd.read_excel("file.xlsx")         # Excel
pd.read_json("file.json")          # JSON
pd.read_parquet("file.parquet")     # Parquet (fast!)

# Writing
df.to_csv("out.csv", index=False)
df.to_excel("out.xlsx", index=False)
df.to_json("out.json", orient="records")
df.to_parquet("out.parquet")

# Useful options
usecols=[]      # Select columns
nrows=100       # Limit rows
chunksize=10000 # Read in chunks
dtype={}        # Force types
na_values=[]    # Custom NaN
encoding="utf-8"# Encoding
```

---

[← Previous: DataFrames](3-dataframes.md) | [🏠 Home](README.md) | [Next: Indexing & Selection →](5-indexing-selection.md)
