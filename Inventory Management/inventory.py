#!/usr/bin/env python3
from datetime import date


class Product:
    def __init__(self, product_id: str, name: str, price: float, stock: int = 0) -> None:
        self.product_id = str(product_id).strip()
        if not self.product_id:
            raise ValueError("Product ID cannot be empty.")

        self.name = str(name).strip()
        if not self.name:
            raise ValueError("Product name cannot be empty.")

        self._price = 0.0
        self._stock = 0

        self.price = price
        self.stock = stock

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value < 0:
            raise ValueError(f"Price cannot be negative: {value}")
        self._price = float(value)

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, value: int) -> None:
        if value < 0:
            raise ValueError(f"Stock cannot be negative: {value}")
        self._stock = int(value)

    def add_stock(self, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError(f"Quantity to add must be positive: {quantity}")
        self.stock += quantity

    def remove_stock(self, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError(f"Quantity to remove must be positive: {quantity}")
        if quantity > self._stock:
            raise ValueError(
                f"Insufficient stock for {self.name} (ID: {self.product_id}): "
                f"available {self._stock}, requested {quantity}"
            )
        self.stock -= quantity

    @property
    def total_value(self) -> float:
        return self._price * self._stock

    def __str__(self) -> str:
        return f"[{self.product_id}] {self.name} - ${self.price:.2f} (Stock: {self.stock})"


class ProductWithExpiryDate(Product):
    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        expiry_date: date | str,
    ) -> None:
        super().__init__(product_id, name, price, stock)
        if isinstance(expiry_date, str):
            self._expiry_date = date.fromisoformat(expiry_date)
        elif isinstance(expiry_date, date):
            self._expiry_date = expiry_date
        else:
            raise TypeError("expiry_date must be a date object or ISO string (YYYY-MM-DD)")

    @property
    def expiry_date(self) -> date:
        return self._expiry_date

    def is_expired(self, as_of: date | None = None) -> bool:
        current = as_of or date.today()
        return current > self._expiry_date

    def days_until_expiry(self, as_of: date | None = None) -> int:
        current = as_of or date.today()
        return (self._expiry_date - current).days

    def is_expiring_soon(self, days_threshold: int = 7, as_of: date | None = None) -> bool:
        days_left = self.days_until_expiry(as_of)
        return 0 <= days_left <= days_threshold

    def __str__(self) -> str:
        status = "EXPIRED" if self.is_expired() else f"Expires: {self._expiry_date}"
        return f"{super().__str__()} [{status}]"


class Inventory:
    def __init__(self) -> None:
        self._products: dict[str, Product] = {}

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError(f"Expected Product instance, got {type(product).__name__}")
        if product.product_id in self._products:
            raise ValueError(f"Product with ID '{product.product_id}' already exists.")
        self._products[product.product_id] = product

    def remove_product(self, product_id: str) -> Product:
        if product_id not in self._products:
            raise KeyError(f"Product ID '{product_id}' not found.")
        return self._products.pop(product_id)

    def get_product(self, product_id: str) -> Product | None:
        return self._products.get(product_id)

    def add_stock(self, product_id: str, quantity: int) -> None:
        product = self.get_product(product_id)
        if not product:
            raise KeyError(f"Product ID '{product_id}' not found.")
        product.add_stock(quantity)

    def remove_stock(self, product_id: str, quantity: int) -> None:
        product = self.get_product(product_id)
        if not product:
            raise KeyError(f"Product ID '{product_id}' not found.")
        product.remove_stock(quantity)

    def check_low_inventory(self, threshold: int = 5) -> list[Product]:
        return [p for p in self._products.values() if p.stock <= threshold]

    def check_expired_products(self, as_of: date | None = None) -> list[ProductWithExpiryDate]:
        return [
            p
            for p in self._products.values()
            if isinstance(p, ProductWithExpiryDate) and p.is_expired(as_of)
        ]

    def total_value(self) -> float:
        return sum(p.total_value for p in self._products.values())

    def generate_report(self, low_stock_threshold: int = 5, as_of: date | None = None) -> str:
        if not self._products:
            return "Inventory is empty."

        lines = [
            f"Inventory Summary ({len(self._products)} items, Total Value: ${self.total_value():.2f}):"
        ]
        for p in sorted(self._products.values(), key=lambda item: item.product_id):
            lines.append(f"  {p}")

        low_stock = self.check_low_inventory(low_stock_threshold)
        if low_stock:
            lines.append("Low Stock Alerts:")
            for p in low_stock:
                lines.append(f"  - {p.name} (ID: {p.product_id}, Stock: {p.stock})")

        expired = self.check_expired_products(as_of)
        if expired:
            lines.append("Expired Products:")
            for p in expired:
                lines.append(f"  - {p.name} (ID: {p.product_id}, Expired on: {p.expiry_date})")

        return "\n".join(lines)

    def __str__(self) -> str:
        return f"Inventory({len(self._products)} products, total value: ${self.total_value():.2f})"
