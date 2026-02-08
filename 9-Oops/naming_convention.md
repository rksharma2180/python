# Python Class Naming Convention

## PascalCase (CapWords Convention)

In Python, class names follow the **PascalCase** convention, where each word in the class name starts with a capital letter, with no underscores between words.

## Rules

1. **Start with a capital letter**: The first letter of the class name should always be capitalized
2. **No underscores**: Unlike function and variable names (which use `snake_case`), class names don't use underscores
3. **Capitalize each word**: If the class name contains multiple words, capitalize the first letter of each word
4. **Acronyms**: For acronyms like HTTP, XML, etc., you can keep them all uppercase or use only the first letter capitalized

## Examples

### ✅ Correct Class Names

```python
class MyClass:
    pass

class StudentRecord:
    pass

class HTTPServerConnection:
    pass

class XMLParser:
    pass

class BankAccount:
    pass

class UserProfile:
    pass

class DatabaseConnection:
    pass
```

### ❌ Incorrect Class Names

```python
# Don't use snake_case
class my_class:
    pass

# Don't use all lowercase
class studentrecord:
    pass

# Don't use camelCase (first letter lowercase)
class bankAccount:
    pass
```

## Comparison with Other Naming Conventions

```python
# Class names - PascalCase
class UserProfile:
    pass

# Function/method names - snake_case
def get_user_data():
    pass

# Variable names - snake_case
user_name = "John"
age = 25

# Constants - UPPER_CASE_WITH_UNDERSCORES
MAX_CONNECTIONS = 100
DEFAULT_TIMEOUT = 30

# Private attributes/methods - prefix with single underscore
_internal_variable = "private"

def _internal_method():
    pass
```

## Reference

This convention is defined in **PEP 8** (Python Enhancement Proposal 8), which is Python's official style guide and the standard reference for Python code style.

**PEP 8 Link**: https://peps.python.org/pep-0008/
