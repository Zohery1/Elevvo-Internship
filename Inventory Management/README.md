# Inventory Management System

An object-oriented inventory system in Python designed to manage products, validate stock updates, track shelf life, and generate inventory summaries.

## Architecture

```mermaid
classDiagram
    class Product {
        +str product_id
        +str name
        +float price
        +int stock
        +float total_value
        +add_stock(quantity)
        +remove_stock(quantity)
        +__str__()
    }

    class ProductWithExpiryDate {
        +date expiry_date
        +is_expired(as_of) bool
        +days_until_expiry(as_of) int
        +is_expiring_soon(days_threshold, as_of) bool
        +__str__()
    }

    class Inventory {
        -dict products
        +add_product(product)
        +remove_product(product_id)
        +get_product(product_id)
        +add_stock(product_id, quantity)
        +remove_stock(product_id, quantity)
        +check_low_inventory(threshold)
        +check_expired_products(as_of)
        +total_value() float
        +generate_report() str
        +__str__()
    }

    Product <|-- ProductWithExpiryDate : inherits
    Inventory o-- Product : aggregates
```

## Features

- Attribute validation via `@property` getters and setters (blocks negative prices, negative stock, and empty identifiers).
- Expiration tracking with `ProductWithExpiryDate` to identify expired products and items approaching shelf-life limits.
- Stock adjustments with bounds checking to prevent stock depletion below zero.
- Inventory queries including low-stock alerts, expiration checks, and total valuation.
- Clean string representations via `__str__` for logging and inspection.

## Usage

```python
from datetime import date
from inventory import Inventory, Product, ProductWithExpiryDate

# Initialize inventory
inv = Inventory()

# Add standard and perishable products
p1 = Product("P01", "Mechanical Keyboard", 79.99, stock=12)
p2 = ProductWithExpiryDate("P02", "Whole Milk", 3.49, stock=4, expiry_date=date(2026, 12, 1))

inv.add_product(p1)
inv.add_product(p2)

# Adjust stock
inv.add_stock("P01", 5)
inv.remove_stock("P02", 2)

# Print inventory report with low-stock and expiration alerts
print(inv.generate_report(low_stock_threshold=5))
```

## Running tests

Run the test suite with pytest:

```bash
pytest test_inventory.py
```
