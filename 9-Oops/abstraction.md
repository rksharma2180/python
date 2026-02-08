# Abstraction in Python

## What is Abstraction?

**Abstraction** is the concept of hiding the complex implementation details and showing only the essential features of an object. It focuses on **what** an object does rather than **how** it does it.

### Real-World Analogy

When you drive a car:
- You use the **steering wheel, pedals, and gear shift** (abstract interface)
- You don't need to know **how the engine works internally** (hidden complexity)

---

## How Python Achieves Abstraction

Python provides abstraction through:

1. **Abstract Base Classes (ABC)** - Using the `abc` module
2. **Encapsulation** - Using private/protected attributes
3. **Interfaces** - Through abstract methods
4. **Duck Typing** - Python's natural abstraction

---

## 1. Abstract Base Classes (ABC)

### Basic Abstract Class

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    """Abstract base class - cannot be instantiated"""
    
    @abstractmethod
    def speak(self):
        """Abstract method - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def move(self):
        """Abstract method - must be implemented by subclasses"""
        pass

# This will raise an error
# animal = Animal()  # TypeError: Can't instantiate abstract class

class Dog(Animal):
    def speak(self):
        return "Woof!"
    
    def move(self):
        return "Running on four legs"

class Bird(Animal):
    def speak(self):
        return "Chirp!"
    
    def move(self):
        return "Flying"

# Now we can create instances
dog = Dog()
print(dog.speak())  # Woof!
print(dog.move())   # Running on four legs

bird = Bird()
print(bird.speak())  # Chirp!
print(bird.move())   # Flying
```

### Why Use Abstract Classes?

- **Enforce structure**: Subclasses must implement specific methods
- **Prevent instantiation**: Can't create objects of abstract class
- **Define contracts**: Specify what methods subclasses must have

---

## 2. Practical Example: Payment System

```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    """Abstract payment processor"""
    
    @abstractmethod
    def process_payment(self, amount):
        """Process payment - must be implemented"""
        pass
    
    @abstractmethod
    def refund(self, transaction_id, amount):
        """Process refund - must be implemented"""
        pass
    
    def validate_amount(self, amount):
        """Concrete method - shared by all subclasses"""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return True

class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount):
        self.validate_amount(amount)
        return f"Processing ${amount} via Credit Card"
    
    def refund(self, transaction_id, amount):
        self.validate_amount(amount)
        return f"Refunding ${amount} to Credit Card (Transaction: {transaction_id})"

class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount):
        self.validate_amount(amount)
        return f"Processing ${amount} via PayPal"
    
    def refund(self, transaction_id, amount):
        self.validate_amount(amount)
        return f"Refunding ${amount} to PayPal (Transaction: {transaction_id})"

class CryptoProcessor(PaymentProcessor):
    def process_payment(self, amount):
        self.validate_amount(amount)
        return f"Processing ${amount} via Cryptocurrency"
    
    def refund(self, transaction_id, amount):
        self.validate_amount(amount)
        return f"Refunding ${amount} to Crypto Wallet (Transaction: {transaction_id})"

# Using abstraction - we don't care about implementation details
def checkout(processor: PaymentProcessor, amount: float):
    """Works with any PaymentProcessor"""
    print(processor.process_payment(amount))

# All work the same way - abstraction in action
checkout(CreditCardProcessor(), 100)
checkout(PayPalProcessor(), 50)
checkout(CryptoProcessor(), 75)
```

**Output:**
```
Processing $100 via Credit Card
Processing $50 via PayPal
Processing $75 via Cryptocurrency
```

---

## 3. The `@property` Decorator in Detail

### What is `@property`?

The `@property` decorator allows you to define methods that can be accessed like attributes. It provides a way to implement **getters**, **setters**, and **deleters** for class attributes.

### Why Use `@property`?

1. **Encapsulation**: Control access to private attributes
2. **Validation**: Add validation logic when setting values
3. **Computed attributes**: Calculate values on-the-fly
4. **Backward compatibility**: Change internal implementation without breaking external code
5. **Read-only attributes**: Create attributes that can't be modified

### Basic Property Example

```python
class Person:
    def __init__(self, name):
        self._name = name  # Private attribute
    
    @property
    def name(self):
        """Getter - access like an attribute"""
        print("Getting name")
        return self._name
    
    @name.setter
    def name(self, value):
        """Setter - set like an attribute"""
        print(f"Setting name to {value}")
        self._name = value
    
    @name.deleter
    def name(self):
        """Deleter - delete the attribute"""
        print("Deleting name")
        del self._name

# Usage - looks like attribute access, but uses methods
person = Person("Alice")
print(person.name)      # Calls getter - Output: Getting name, Alice
person.name = "Bob"     # Calls setter - Output: Setting name to Bob
del person.name         # Calls deleter - Output: Deleting name
```

### Property with Validation

```python
class BankAccount:
    def __init__(self, balance):
        self._balance = balance
    
    @property
    def balance(self):
        """Get current balance"""
        return self._balance
    
    @balance.setter
    def balance(self, amount):
        """Set balance with validation"""
        if amount < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = amount

account = BankAccount(1000)
print(account.balance)  # 1000

account.balance = 1500  # OK
print(account.balance)  # 1500

# account.balance = -100  # Raises ValueError
```

### Read-Only Property

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        """Read-only radius"""
        return self._radius
    
    @property
    def area(self):
        """Computed property - calculated on access"""
        return 3.14159 * self._radius ** 2
    
    @property
    def circumference(self):
        """Another computed property"""
        return 2 * 3.14159 * self._radius

circle = Circle(5)
print(circle.radius)         # 5
print(circle.area)           # 78.53975
print(circle.circumference)  # 31.4159

# circle.area = 100  # AttributeError - no setter defined
```

### Property with Complex Validation

```python
class User:
    def __init__(self, email, age):
        self.email = email  # Uses setter
        self.age = age      # Uses setter
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        """Validate email format"""
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        if "@" not in value or "." not in value:
            raise ValueError("Invalid email format")
        self._email = value
    
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, value):
        """Validate age range"""
        if not isinstance(value, int):
            raise TypeError("Age must be an integer")
        if value < 0 or value > 150:
            raise ValueError("Age must be between 0 and 150")
        self._age = value

# Valid user
user = User("alice@example.com", 25)
print(user.email)  # alice@example.com
print(user.age)    # 25

# Invalid email
# user.email = "invalid"  # Raises ValueError

# Invalid age
# user.age = -5  # Raises ValueError
# user.age = 200  # Raises ValueError
```

### Property for Lazy Loading

```python
class DataProcessor:
    def __init__(self, filename):
        self.filename = filename
        self._data = None  # Not loaded yet
    
    @property
    def data(self):
        """Lazy load data only when accessed"""
        if self._data is None:
            print(f"Loading data from {self.filename}...")
            # Simulate loading data
            self._data = [1, 2, 3, 4, 5]
        return self._data

processor = DataProcessor("data.txt")
print("Processor created")
# Data not loaded yet

print(processor.data)  # Loading data from data.txt... [1, 2, 3, 4, 5]
print(processor.data)  # [1, 2, 3, 4, 5] (no loading message - cached)
```

### Property with Dependent Attributes

```python
class Rectangle:
    def __init__(self, width, height):
        self._width = width
        self._height = height
    
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value):
        if value <= 0:
            raise ValueError("Width must be positive")
        self._width = value
    
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        if value <= 0:
            raise ValueError("Height must be positive")
        self._height = value
    
    @property
    def area(self):
        """Computed from width and height"""
        return self._width * self._height
    
    @property
    def perimeter(self):
        """Computed from width and height"""
        return 2 * (self._width + self._height)

rect = Rectangle(5, 10)
print(rect.area)       # 50
print(rect.perimeter)  # 30

rect.width = 8
print(rect.area)       # 80 (automatically updated)
print(rect.perimeter)  # 36 (automatically updated)
```

### Using `property()` Function (Alternative Syntax)

```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius
    
    def get_celsius(self):
        return self._celsius
    
    def set_celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero")
        self._celsius = value
    
    def del_celsius(self):
        del self._celsius
    
    # Using property() function instead of decorator
    celsius = property(get_celsius, set_celsius, del_celsius, 
                      "Temperature in Celsius")
    
    @property
    def fahrenheit(self):
        """Convert to Fahrenheit"""
        return self._celsius * 9/5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        """Set temperature using Fahrenheit"""
        self._celsius = (value - 32) * 5/9

temp = Temperature(25)
print(temp.celsius)     # 25
print(temp.fahrenheit)  # 77.0

temp.fahrenheit = 32
print(temp.celsius)     # 0.0
```

---

## 4. Abstract Properties

```python
from abc import ABC, abstractmethod

class Vehicle(ABC):
    @property
    @abstractmethod
    def max_speed(self):
        """Abstract property - must be implemented"""
        pass
    
    @abstractmethod
    def start_engine(self):
        pass

class Car(Vehicle):
    def __init__(self):
        self._max_speed = 200
    
    @property
    def max_speed(self):
        return self._max_speed
    
    def start_engine(self):
        return "Motorcycle engine started"

car = Car()
print(car.max_speed)      # 200
print(car.start_engine()) # Car engine started

bike = Motorcycle()
print(bike.max_speed)      # 180
print(bike.start_engine()) # Motorcycle engine started
```

### Abstract Property with Setter

```python
from abc import ABC, abstractmethod

class Product(ABC):
    @property
    @abstractmethod
    def price(self):
        """Abstract property getter"""
        pass
    
    @price.setter
    @abstractmethod
    def price(self, value):
        """Abstract property setter"""
        pass

class Book(Product):
    def __init__(self, title, initial_price):
        self.title = title
        self._price = initial_price
    
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value

book = Book("Python Guide", 29.99)
print(book.price)  # 29.99
book.price = 34.99
print(book.price)  # 34.99
```

---

## 5. Multiple Abstract Methods

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    """Abstract shape class"""
    
    @abstractmethod
    def area(self):
        """Calculate area"""
        pass
    
    @abstractmethod
    def perimeter(self):
        """Calculate perimeter"""
        pass
    
    def description(self):
        """Concrete method - available to all shapes"""
        return f"I am a {self.__class__.__name__}"

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2
    
    def perimeter(self):
        return 2 * 3.14159 * self.radius

# Using abstraction
shapes = [Rectangle(5, 10), Circle(7)]

for shape in shapes:
    print(f"{shape.description()}")
    print(f"  Area: {shape.area():.2f}")
    print(f"  Perimeter: {shape.perimeter():.2f}")
    print()
```

**Output:**
```
I am a Rectangle
  Area: 50.00
  Perimeter: 30.00

I am a Circle
  Area: 153.94
  Perimeter: 43.98
```

---

## 6. Encapsulation for Abstraction

```python
class BankAccount:
    """Abstraction through encapsulation"""
    
    def __init__(self, account_number, initial_balance):
        self.__account_number = account_number  # Private
        self.__balance = initial_balance        # Private
        self.__transactions = []                # Private
    
    # Public interface - abstraction
    def deposit(self, amount):
        """User doesn't need to know internal implementation"""
        if amount > 0:
            self.__balance += amount
            self.__record_transaction("deposit", amount)
            return True
        return False
    
    def withdraw(self, amount):
        """User doesn't need to know internal validation logic"""
        if self.__validate_withdrawal(amount):
            self.__balance -= amount
            self.__record_transaction("withdrawal", amount)
            return True
        return False
    
    def get_balance(self):
        """Public method to access private data"""
        return self.__balance
    
    # Private methods - hidden complexity
    def __validate_withdrawal(self, amount):
        """Hidden validation logic"""
        return amount > 0 and amount <= self.__balance
    
    def __record_transaction(self, type, amount):
        """Hidden transaction recording"""
        self.__transactions.append({
            'type': type,
            'amount': amount
        })

# User interacts with simple interface
account = BankAccount("123456", 1000)
account.deposit(500)
account.withdraw(200)
print(f"Balance: ${account.get_balance()}")  # Balance: $1300

# Internal details are hidden
# account.__balance  # AttributeError - can't access directly
```

---

## 7. Database Connection Example

```python
from abc import ABC, abstractmethod

class DatabaseConnection(ABC):
    """Abstract database connection"""
    
    @abstractmethod
    def connect(self):
        pass
    
    @abstractmethod
    def disconnect(self):
        pass
    
    @abstractmethod
    def execute_query(self, query):
        pass
    
    def log(self, message):
        """Concrete method - shared functionality"""
        print(f"[LOG] {message}")

class MySQLConnection(DatabaseConnection):
    def connect(self):
        self.log("Connecting to MySQL database...")
        return "MySQL connected"
    
    def disconnect(self):
        self.log("Disconnecting from MySQL...")
        return "MySQL disconnected"
    
    def execute_query(self, query):
        self.log(f"Executing MySQL query: {query}")
        return f"MySQL result for: {query}"

class PostgreSQLConnection(DatabaseConnection):
    def connect(self):
        self.log("Connecting to PostgreSQL database...")
        return "PostgreSQL connected"
    
    def disconnect(self):
        self.log("Disconnecting from PostgreSQL...")
        return "PostgreSQL disconnected"
    
    def execute_query(self, query):
        self.log(f"Executing PostgreSQL query: {query}")
        return f"PostgreSQL result for: {query}"

class MongoDBConnection(DatabaseConnection):
    def connect(self):
        self.log("Connecting to MongoDB...")
        return "MongoDB connected"
    
    def disconnect(self):
        self.log("Disconnecting from MongoDB...")
        return "MongoDB disconnected"
    
    def execute_query(self, query):
        self.log(f"Executing MongoDB query: {query}")
        return f"MongoDB result for: {query}"

# Abstraction in action - same interface, different implementations
def run_database_operations(db: DatabaseConnection):
    """Works with any database - we don't care about implementation"""
    db.connect()
    result = db.execute_query("SELECT * FROM users")
    print(result)
    db.disconnect()
    print()

# All databases work the same way from user's perspective
run_database_operations(MySQLConnection())
run_database_operations(PostgreSQLConnection())
run_database_operations(MongoDBConnection())
```

---

## 8. Partial Implementation (Concrete Methods in Abstract Class)

```python
from abc import ABC, abstractmethod

class Employee(ABC):
    """Abstract employee class with some concrete methods"""
    
    def __init__(self, name, employee_id):
        self.name = name
        self.employee_id = employee_id
    
    @abstractmethod
    def calculate_salary(self):
        """Must be implemented by subclasses"""
        pass
    
    def get_details(self):
        """Concrete method - shared by all employees"""
        return f"Employee: {self.name} (ID: {self.employee_id})"
    
    def display_info(self):
        """Concrete method using abstract method"""
        print(self.get_details())
        print(f"Salary: ${self.calculate_salary()}")

class FullTimeEmployee(Employee):
    def __init__(self, name, employee_id, monthly_salary):
        super().__init__(name, employee_id)
        self.monthly_salary = monthly_salary
    
    def calculate_salary(self):
        return self.monthly_salary

class HourlyEmployee(Employee):
    def __init__(self, name, employee_id, hourly_rate, hours_worked):
        super().__init__(name, employee_id)
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked
    
    def calculate_salary(self):
        return self.hourly_rate * self.hours_worked

# Using abstraction
employees = [
    FullTimeEmployee("Alice", "E001", 5000),
    HourlyEmployee("Bob", "E002", 25, 160)
]

for emp in employees:
    emp.display_info()
    print()
```

---

## Benefits of Abstraction

### 1. **Hides Complexity**
```python
# User sees simple interface
account.deposit(100)

# Hidden complexity:
# - Validation
# - Transaction recording
# - Balance updates
# - Error handling
```

### 2. **Enforces Structure**
```python
# All payment processors MUST implement these methods
class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass
```

### 3. **Reduces Code Duplication**
```python
# Common functionality in abstract class
class Shape(ABC):
    def description(self):  # Shared by all shapes
        return f"I am a {self.__class__.__name__}"
```

### 4. **Improves Maintainability**
```python
# Change implementation without changing interface
def checkout(processor: PaymentProcessor, amount):
    processor.process_payment(amount)  # Works with any processor
```

---

## Abstraction vs Encapsulation

| Aspect | Abstraction | Encapsulation |
|--------|-------------|---------------|
| **Focus** | What to show | What to hide |
| **Purpose** | Hide complexity | Protect data |
| **Implementation** | Abstract classes, interfaces | Private attributes, methods |
| **Example** | `PaymentProcessor` interface | `__balance` private attribute |

```python
from abc import ABC, abstractmethod

class BankAccount(ABC):
    # Encapsulation - hiding data
    def __init__(self):
        self.__balance = 0  # Private
    
    # Abstraction - showing only essential interface
    @abstractmethod
    def deposit(self, amount):
        pass
    
    @abstractmethod
    def withdraw(self, amount):
        pass
```

---

## Summary

### How Python Achieves Abstraction

1. **ABC Module** - Create abstract base classes
2. **@abstractmethod** - Define methods that must be implemented
3. **@property** - Create abstract properties
4. **Encapsulation** - Hide implementation details
5. **Duck Typing** - Natural abstraction through interfaces

### Key Concepts

✅ **Abstract classes cannot be instantiated**  
✅ **Subclasses must implement all abstract methods**  
✅ **Abstract classes can have concrete methods**  
✅ **Abstraction hides complexity, shows only essentials**  
✅ **Improves code maintainability and reusability**

### When to Use Abstraction

- Defining common interfaces for related classes
- Enforcing implementation of specific methods
- Creating frameworks or libraries
- Building plugin systems
- Implementing design patterns (Strategy, Factory, etc.)
