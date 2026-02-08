# Python Source File Conventions

## Python vs Java: File Organization Philosophy

### Java's One-Class-Per-File Rule

In Java, the convention is **strict**:
- One **public** class per file
- File name **must match** the public class name
- Everything must be inside a class

```java
// User.java - Must contain only the User class
public class User {
    private String name;
    private int age;
    
    public User(String name, int age) {
        this.name = name;
        this.age = age;
    }
}

// UserService.java - Separate file for UserService
public class UserService {
    public void createUser(User user) {
        // logic
    }
}
```

### Python's Flexible Approach

Python is **much more flexible**:
- **Multiple classes** can exist in one file
- **Functions** can exist alongside classes
- **Module-level code** can exist
- File name **doesn't need to match** class names
- No requirement for everything to be in a class

```python
# users.py - Can contain multiple classes, functions, and variables

# Module-level constants
DEFAULT_ROLE = "user"
MAX_USERNAME_LENGTH = 50

# Utility functions
def validate_email(email):
    return "@" in email and "." in email

# Multiple classes in the same file
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class UserService:
    def __init__(self):
        self.users = []
    
    def create_user(self, name, email):
        if validate_email(email):
            user = User(name, email)
            self.users.append(user)
            return user

class UserRepository:
    def save(self, user):
        # Save to database
        pass

# Module-level code
service = UserService()
```

---

## Python File Organization Conventions

### 1. **Related Classes Together**

Group **closely related classes** in the same file:

```python
# shapes.py - Related geometric shapes

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Circle:
    def __init__(self, center, radius):
        self.center = center  # Point object
        self.radius = radius
    
    def area(self):
        import math
        return math.pi * self.radius ** 2

class Rectangle:
    def __init__(self, top_left, width, height):
        self.top_left = top_left  # Point object
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height

class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
```

**Rationale**: These classes are all related to geometric shapes and are likely to be used together.

### 2. **Separate Large or Complex Classes**

If a class is **large or complex**, give it its own file:

```python
# user_authentication.py - Complex authentication logic
class UserAuthenticationService:
    """
    Large class with many methods for authentication,
    password hashing, token management, etc.
    """
    
    def __init__(self):
        # Complex initialization
        pass
    
    def authenticate(self, username, password):
        # 50+ lines of logic
        pass
    
    def hash_password(self, password):
        # Password hashing logic
        pass
    
    def generate_token(self, user):
        # Token generation
        pass
    
    # ... many more methods
```

### 3. **Utility Functions and Classes Together**

Group utility functions with helper classes:

```python
# validators.py - Validation utilities

import re
from datetime import datetime

# Utility functions
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_phone(phone):
    pattern = r'^\+?1?\d{9,15}$'
    return re.match(pattern, phone) is not None

def is_valid_date(date_string, format="%Y-%m-%d"):
    try:
        datetime.strptime(date_string, format)
        return True
    except ValueError:
        return False

# Helper class
class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

# Validator class
class Validator:
    @staticmethod
    def validate_user_data(data):
        if not is_valid_email(data.get('email', '')):
            raise ValidationError("Invalid email")
        
        if not is_valid_phone(data.get('phone', '')):
            raise ValidationError("Invalid phone")
        
        return True
```

---

## Standard Python File Structure

### Recommended Order (PEP 8)

```python
"""
Module docstring - Brief description of what this module does.

This module contains classes and functions for user management,
including User model, UserService, and validation utilities.
"""

# 1. IMPORTS
# Standard library imports
import os
import sys
from datetime import datetime

# Third-party imports
import requests
from flask import Flask

# Local application imports
from .models import BaseModel
from .utils import logger

# 2. MODULE-LEVEL CONSTANTS
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
API_VERSION = "1.0.0"

# 3. MODULE-LEVEL VARIABLES (if needed)
_cache = {}
_initialized = False

# 4. EXCEPTION CLASSES
class UserNotFoundError(Exception):
    """Raised when a user is not found"""
    pass

class ValidationError(Exception):
    """Raised when validation fails"""
    pass

# 5. UTILITY FUNCTIONS
def validate_email(email):
    """Validate email format"""
    return "@" in email

def log_event(message):
    """Log an event"""
    print(f"[{datetime.now()}] {message}")

# 6. CLASSES
class User:
    """User model class"""
    
    def __init__(self, name, email):
        self.name = name
        self.email = email

class UserService:
    """Service class for user operations"""
    
    def __init__(self):
        self.users = []
    
    def create_user(self, name, email):
        if not validate_email(email):
            raise ValidationError("Invalid email")
        
        user = User(name, email)
        self.users.append(user)
        return user

# 7. MODULE-LEVEL EXECUTION CODE
def _initialize():
    """Initialize module"""
    global _initialized
    if not _initialized:
        log_event("Module initialized")
        _initialized = True

# 8. MAIN GUARD
if __name__ == "__main__":
    # Code that only runs when file is executed directly
    _initialize()
    service = UserService()
    user = service.create_user("Alice", "alice@example.com")
    print(f"Created user: {user.name}")
```

---

## Common File Organization Patterns

### Pattern 1: Models File

```python
# models.py - Data models

from datetime import datetime

class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.created_at = datetime.now()

class Post:
    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author  # User object
        self.created_at = datetime.now()

class Comment:
    def __init__(self, content, author, post):
        self.content = content
        self.author = author  # User object
        self.post = post      # Post object
        self.created_at = datetime.now()
```

### Pattern 2: Services File

```python
# services.py - Business logic

from .models import User, Post, Comment
from .validators import validate_email

class UserService:
    def __init__(self, repository):
        self.repository = repository
    
    def create_user(self, username, email):
        if not validate_email(email):
            raise ValueError("Invalid email")
        
        user = User(username, email)
        self.repository.save(user)
        return user

class PostService:
    def __init__(self, repository):
        self.repository = repository
    
    def create_post(self, title, content, author):
        post = Post(title, content, author)
        self.repository.save(post)
        return post
```

### Pattern 3: Single Large Class

```python
# database_manager.py - Single complex class

import sqlite3
from contextlib import contextmanager

class DatabaseManager:
    """
    Comprehensive database management class.
    This is large and complex enough to warrant its own file.
    """
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def execute_query(self, query, params=None):
        """Execute a query"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or [])
            return cursor.fetchall()
    
    # ... many more methods (50+ lines each)
```

---

## When to Split vs Keep Together

### ✅ Keep in Same File When:

1. **Classes are closely related**
   ```python
   # payment.py
   class Payment:
       pass
   
   class PaymentProcessor:
       pass
   
   class PaymentValidator:
       pass
   ```

2. **Small, simple classes**
   ```python
   # exceptions.py
   class ValidationError(Exception):
       pass
   
   class NotFoundError(Exception):
       pass
   
   class AuthenticationError(Exception):
       pass
   ```

3. **Helper classes for a main class**
   ```python
   # report_generator.py
   class ReportData:
       """Helper class for report data"""
       pass
   
   class ReportFormatter:
       """Helper class for formatting"""
       pass
   
   class ReportGenerator:
       """Main class that uses helpers"""
       pass
   ```

4. **Total file size is reasonable** (< 500 lines)

### ❌ Split into Separate Files When:

1. **Class is very large** (> 200 lines)
2. **Classes serve different purposes**
3. **File becomes too long** (> 500 lines)
4. **Classes are independently reusable**
5. **Testing would be easier with separation**

---

## Real-World Examples

### Example 1: Django Models File

```python
# models.py - Multiple related models
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date = models.DateField()

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
```

### Example 2: Flask Application

```python
# app.py - Application with routes, models, and utilities
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuration
DEBUG = True
DATABASE_URL = "sqlite:///app.db"

# Models
class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email

# Utilities
def validate_user_data(data):
    return 'username' in data and 'email' in data

# Routes
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not validate_user_data(data):
        return jsonify({"error": "Invalid data"}), 400
    
    user = User(data['username'], data['email'])
    return jsonify({"message": "User created"}), 201

if __name__ == '__main__':
    app.run(debug=DEBUG)
```

### Example 3: Large Project Structure

```
myproject/
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── user.py          # Single User class (large)
│   ├── product.py       # Single Product class (large)
│   └── order.py         # Single Order class (large)
├── services/
│   ├── __init__.py
│   ├── user_service.py
│   └── order_service.py
├── utils/
│   ├── __init__.py
│   ├── validators.py    # Multiple validation functions
│   └── helpers.py       # Multiple helper functions
└── exceptions.py        # All custom exceptions together
```

---

## Best Practices Summary

### DO:

✅ **Group related classes** in the same file
✅ **Keep files focused** on a single responsibility
✅ **Use descriptive file names** (plural for multiple classes: `validators.py`)
✅ **Follow PEP 8** structure (imports, constants, classes, main)
✅ **Add module docstrings** explaining the file's purpose
✅ **Keep files under 500 lines** when possible
✅ **Use `__init__.py`** to expose public API

### DON'T:

❌ **Don't mix unrelated classes** in one file
❌ **Don't create files with 1000+ lines**
❌ **Don't put everything in one file** (even if it works)
❌ **Don't split every class** into its own file (unless needed)
❌ **Don't ignore logical grouping** for the sake of "one class per file"

---

## Comparison Table

| Aspect | Java | Python |
|--------|------|--------|
| **Classes per file** | One public class | Multiple classes allowed |
| **File naming** | Must match class name | Descriptive, doesn't need to match |
| **Module-level code** | Not allowed | Allowed and common |
| **Functions outside classes** | Not allowed | Allowed and encouraged |
| **File size concern** | Less common (one class) | More important (multiple items) |
| **Organization principle** | Class-centric | Module-centric |

---

## Conclusion

**Python's Philosophy**: 
- Organize by **logical grouping** and **functionality**
- **Multiple related classes** in one file is perfectly fine
- **Flexibility** over strict rules
- **Readability** and **maintainability** are key

**Key Takeaway**: Unlike Java's strict one-class-per-file rule, Python encourages organizing code by **logical modules** where related classes, functions, and utilities live together. The goal is **clarity and maintainability**, not arbitrary file limits.
