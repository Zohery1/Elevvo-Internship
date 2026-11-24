# Inventory Management System

An object-oriented inventory system in Python designed to manage products, validate stock updates, and generate inventory summaries.

## Core architecture

- `Product`: Base class storing product ID, name, unit price, and stock count. Uses Python `@property` getters and setters to enforce business rules (such as blocking negative stock quantities and invalid price updates).
- `ProductWithExpiryDate`: Subclass inheriting from `Product` that tracks expiration dates, checks if an item has expired, and flags products approaching shelf-life limits.
- `Inventory`: Container class managing the product collection, supporting stock additions, stock reductions, low-inventory alerts, and summary reports.

## Features

- Controlled attribute access using `@property` decorators.
- Low-stock threshold detection to flag items that need reordering.
- Formatted console reports listing active items, quantities, and values.
- Clean string representation via `__str__` for debugging and logging.

## Tech stack

- Python 3 (OOP: classes, inheritance, properties)
- Testing: `pytest`
