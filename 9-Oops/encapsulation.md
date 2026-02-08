# Encapsulation in Python

## What is Encapsulation?

**Encapsulation** is the bundling of data (attributes) and methods that operate on that data within a single unit (class), while restricting direct access to some of the object's components. It's about **hiding internal state** and requiring all interaction to be performed through an object's methods.

### Key Principles

1. **Data Hiding**: Hide internal implementation details
2. **Access Control**: Control how data is accessed and modified
3. **Public Interface**: Provide controlled access through methods
4. **Protection**: Prevent accidental modification of data

---

## Python's Approach to Encapsulation

Python uses **naming conventions** rather than strict access modifiers. It follows the philosophy: **"We're all consenting adults here"** - trusting developers to respect conventions.

### Access Levels in Python

| Convention | Meaning | Example |
|------------|---------|---------|
| `public` | No underscore - accessible everywhere | `self.name` |
| `_protected` | Single underscore - internal use (convention) | `self._age` |
| `__private` | Double underscore - name mangling | `self.__balance` |

---

## 1. Public Attributes (No Encapsulation)

```python
class Person:
    def __init__(self, name, age):
        self.name = name  # Public
        self.age = age    # Public

person = Person("Alice", 30)
print(person.name)  # Alice
person.age = -5     # No protection - can set invalid value!
print(person.age)   # -5 (problematic!)
```

**Issue**: No validation, anyone can modify data directly.

---

## 2. Protected Attributes (Single Underscore `_`)

```python
class BankAccount:
    def __init__(self, account_number, balance):
        self._account_number = account_number  # Protected (convention)
        self._balance = balance                # Protected (convention)
    
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return True
        return False
    
    def get_balance(self):
        return self._balance

account = BankAccount("123456", 1000)
print(account.get_balance())  # 1000 - proper access

# Can still access directly (but shouldn't - it's a convention)
print(account._balance)  # 1000 - works but violates convention
account._balance = -500  # Bad practice but Python allows it
```

**Note**: Single underscore is just a **convention** - not enforced by Python.

---

## 3. Private Attributes (Double Underscore `__`)

```python
class BankAccount:
    def __init__(self, account_number, balance):
        self.__account_number = account_number  # Private
        self.__balance = balance                # Private
    
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            return True
        return False
    
    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return True
        return False
    
    def get_balance(self):
        return self.__balance

account = BankAccount("123456", 1000)
print(account.get_balance())  # 1000

# Direct access fails
# print(account.__balance)  # AttributeError

# But can still access via name mangling (not recommended)
print(account._BankAccount__balance)  # 1000 (name mangling)
```

**Name Mangling**: Python renames `__attribute` to `_ClassName__attribute` internally.

---

## 4. Proper Encapsulation with `@property`

```python
class Person:
    def __init__(self, name, age):
        self.__name = name
        self.__age = age
    
    @property
    def name(self):
        """Getter for name"""
        return self.__name
    
    @property
    def age(self):
        """Getter for age"""
        return self.__age
    
    @age.setter
    def age(self, value):
        """Setter with validation"""
        if not isinstance(value, int):
            raise TypeError("Age must be an integer")
        if value < 0 or value > 150:
            raise ValueError("Age must be between 0 and 150")
        self.__age = value

person = Person("Alice", 30)
print(person.name)  # Alice
print(person.age)   # 30

person.age = 35     # OK - uses setter
print(person.age)   # 35

# person.age = -5   # ValueError: Age must be between 0 and 150
# person.name = "Bob"  # AttributeError: can't set attribute (no setter)
```

---

## 5. Complete Encapsulation Example

```python
class Employee:
    def __init__(self, name, employee_id, salary):
        self.__name = name
        self.__employee_id = employee_id
        self.__salary = salary
        self.__performance_rating = 0
    
    # Read-only property
    @property
    def name(self):
        return self.__name
    
    @property
    def employee_id(self):
        return self.__employee_id
    
    # Property with getter and setter
    @property
    def salary(self):
        return self.__salary
    
    @salary.setter
    def salary(self, value):
        if value < 0:
            raise ValueError("Salary cannot be negative")
        self.__salary = value
    
    @property
    def performance_rating(self):
        return self.__performance_rating
    
    @performance_rating.setter
    def performance_rating(self, value):
        if not 0 <= value <= 5:
            raise ValueError("Rating must be between 0 and 5")
        self.__performance_rating = value
    
    # Public methods
    def give_raise(self, percentage):
        """Controlled way to modify salary"""
        if percentage > 0:
            self.__salary *= (1 + percentage / 100)
    
    def get_details(self):
        return f"{self.__name} (ID: {self.__employee_id}) - Salary: ${self.__salary}"

# Usage
emp = Employee("Alice", "E001", 50000)
print(emp.get_details())  # Alice (ID: E001) - Salary: $50000

emp.give_raise(10)
print(emp.salary)  # 55000.0

emp.performance_rating = 4
print(emp.performance_rating)  # 4

# emp.performance_rating = 10  # ValueError
```

---

## Java vs Python Encapsulation

### Java's Approach (Strict Access Modifiers)

```java
public class BankAccount {
    // Private - strictly enforced
    private String accountNumber;
    private double balance;
    
    // Constructor
    public BankAccount(String accountNumber, double balance) {
        this.accountNumber = accountNumber;
        this.balance = balance;
    }
    
    // Public getter
    public double getBalance() {
        return balance;
    }
    
    // Public method with validation
    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
        }
    }
    
    // Private helper method
    private boolean validateAmount(double amount) {
        return amount > 0 && amount <= balance;
    }
}

// Usage
BankAccount account = new BankAccount("123456", 1000);
System.out.println(account.getBalance());  // 1000
// System.out.println(account.balance);    // Compile error - private!
```

### Python Equivalent

```python
class BankAccount:
    def __init__(self, account_number, balance):
        self.__account_number = account_number  # "Private" via name mangling
        self.__balance = balance
    
    @property
    def balance(self):
        """Getter"""
        return self.__balance
    
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
    
    def __validate_amount(self, amount):
        """Private helper method"""
        return amount > 0 and amount <= self.__balance

# Usage
account = BankAccount("123456", 1000)
print(account.balance)  # 1000
# print(account.__balance)  # AttributeError

# But can still access via name mangling (Python allows it)
print(account._BankAccount__balance)  # 1000
```

---

## Key Differences: Python vs Java

| Aspect | Java | Python |
|--------|------|--------|
| **Access Modifiers** | `private`, `protected`, `public` | Naming conventions (`_`, `__`) |
| **Enforcement** | Compile-time (strict) | Runtime (convention-based) |
| **Private Access** | Impossible from outside | Possible via name mangling |
| **Philosophy** | "Force protection" | "We're all adults" |
| **Getters/Setters** | Explicit methods | `@property` decorator |
| **Verbosity** | More verbose | More concise |
| **Default Access** | Package-private | Public |

### Java Access Modifiers

```java
public class Example {
    public int publicVar;        // Accessible everywhere
    protected int protectedVar;  // Accessible in subclasses and package
    int defaultVar;              // Package-private (no modifier)
    private int privateVar;      // Only within this class
}
```

### Python Naming Conventions

```python
class Example:
    def __init__(self):
        self.public_var = 1      # Public (convention)
        self._protected_var = 2  # Protected (convention)
        self.__private_var = 3   # Private (name mangling)
```

---

## Practical Comparison Examples

### Example 1: Getters and Setters

**Java:**
```java
public class Person {
    private String name;
    private int age;
    
    // Getter
    public String getName() {
        return name;
    }
    
    // Setter with validation
    public void setAge(int age) {
        if (age >= 0 && age <= 150) {
            this.age = age;
        } else {
            throw new IllegalArgumentException("Invalid age");
        }
    }
    
    // Getter
    public int getAge() {
        return age;
    }
}

// Usage
Person person = new Person();
person.setAge(30);
System.out.println(person.getAge());
```

**Python:**
```python
class Person:
    def __init__(self):
        self.__name = None
        self.__age = None
    
    @property
    def name(self):
        return self.__name
    
    @property
    def age(self):
        return self.__age
    
    @age.setter
    def age(self, value):
        if 0 <= value <= 150:
            self.__age = value
        else:
            raise ValueError("Invalid age")

# Usage - looks like attribute access
person = Person()
person.age = 30
print(person.age)
```

### Example 2: Read-Only Properties

**Java:**
```java
public class Circle {
    private final double radius;  // final = can't change after construction
    
    public Circle(double radius) {
        this.radius = radius;
    }
    
    public double getRadius() {
        return radius;
    }
    
    public double getArea() {
        return Math.PI * radius * radius;
    }
    
    // No setRadius() - read-only
}
```

**Python:**
```python
class Circle:
    def __init__(self, radius):
        self.__radius = radius
    
    @property
    def radius(self):
        return self.__radius
    
    @property
    def area(self):
        return 3.14159 * self.__radius ** 2
    
    # No setter - read-only
```

---

## Best Practices

### Python Encapsulation Best Practices

✅ **Use `@property` for controlled access**
```python
@property
def balance(self):
    return self.__balance
```

✅ **Use single underscore for internal/protected**
```python
self._internal_value = 10  # Convention: don't access from outside
```

✅ **Use double underscore for truly private**
```python
self.__secret = "hidden"  # Name mangling applied
```

✅ **Validate in setters**
```python
@age.setter
def age(self, value):
    if value < 0:
        raise ValueError("Age cannot be negative")
    self.__age = value
```

✅ **Provide public interface**
```python
def deposit(self, amount):
    """Public method for controlled modification"""
    if amount > 0:
        self.__balance += amount
```

### When to Use Each

| Use Case | Convention |
|----------|------------|
| Public API | `self.attribute` |
| Internal implementation | `self._attribute` |
| Avoid name conflicts in subclasses | `self.__attribute` |
| Read-only access | `@property` without setter |
| Validated access | `@property` with setter |

---

## Common Patterns

### 1. Lazy Loading with Encapsulation

```python
class DataLoader:
    def __init__(self, filename):
        self.__filename = filename
        self.__data = None
    
    @property
    def data(self):
        """Lazy load data"""
        if self.__data is None:
            print(f"Loading {self.__filename}...")
            self.__data = self.__load_data()
        return self.__data
    
    def __load_data(self):
        """Private helper method"""
        return [1, 2, 3, 4, 5]
```

### 2. Computed Properties

```python
class Rectangle:
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
    
    @property
    def area(self):
        """Computed on access"""
        return self.__width * self.__height
    
    @property
    def perimeter(self):
        """Computed on access"""
        return 2 * (self.__width + self.__height)
```

### 3. Immutable Objects

```python
class Point:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
    
    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y
    
    # No setters - immutable after creation
```

---

## Summary

### Python Encapsulation
- **Convention-based** rather than enforced
- Uses naming conventions (`_`, `__`)
- `@property` for elegant getters/setters
- Philosophy: trust developers
- More concise syntax

### Java Encapsulation
- **Strictly enforced** at compile time
- Uses access modifiers (`private`, `protected`, `public`)
- Explicit getter/setter methods
- Philosophy: enforce protection
- More verbose but explicit

### Key Takeaway
Python provides encapsulation through **conventions and tools** (`@property`, name mangling), trusting developers to follow best practices, while Java **enforces** encapsulation through strict access modifiers at compile time.
