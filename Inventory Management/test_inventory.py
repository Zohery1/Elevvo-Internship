from datetime import date, timedelta
import pytest

from inventory import Inventory, Product, ProductWithExpiryDate


def test_product_creation_and_properties():
    p = Product("P001", "Mechanical Keyboard", 89.99, 10)
    assert p.product_id == "P001"
    assert p.name == "Mechanical Keyboard"
    assert p.price == 89.99
    assert p.stock == 10
    assert p.total_value == 899.90


def test_product_validation():
    with pytest.raises(ValueError, match="Product ID cannot be empty"):
        Product("", "Valid Name", 10.0, 5)

    with pytest.raises(ValueError, match="Product name cannot be empty"):
        Product("P002", "   ", 10.0, 5)

    with pytest.raises(ValueError, match="Price cannot be negative"):
        Product("P003", "Mouse", -5.0, 5)

    with pytest.raises(ValueError, match="Stock cannot be negative"):
        Product("P004", "Monitor", 200.0, -2)


def test_product_stock_operations():
    p = Product("P005", "USB-C Hub", 25.0, 10)
    p.add_stock(5)
    assert p.stock == 15

    p.remove_stock(4)
    assert p.stock == 11

    with pytest.raises(ValueError, match="Quantity to add must be positive"):
        p.add_stock(0)

    with pytest.raises(ValueError, match="Quantity to remove must be positive"):
        p.remove_stock(-1)

    with pytest.raises(ValueError, match="Insufficient stock"):
        p.remove_stock(20)


def test_product_str():
    p = Product("P006", "Headphones", 50.0, 4)
    assert str(p) == "[P006] Headphones - $50.00 (Stock: 4)"


def test_product_with_expiry_date():
    today = date(2026, 11, 24)
    past_date = date(2026, 11, 20)
    future_date = date(2026, 11, 28)

    expired_item = ProductWithExpiryDate("E001", "Milk", 3.50, 5, past_date)
    assert expired_item.is_expired(as_of=today)
    assert "EXPIRED" in str(expired_item)

    fresh_item = ProductWithExpiryDate("E002", "Cheese", 6.0, 8, "2026-11-28")
    assert not fresh_item.is_expired(as_of=today)
    assert fresh_item.days_until_expiry(as_of=today) == 4
    assert fresh_item.is_expiring_soon(days_threshold=5, as_of=today)
    assert not fresh_item.is_expiring_soon(days_threshold=3, as_of=today)
    assert "Expires: 2026-11-28" in str(fresh_item)

    with pytest.raises(TypeError, match="expiry_date must be a date object or ISO string"):
        ProductWithExpiryDate("E003", "Yogurt", 2.0, 3, 12345)


def test_inventory_add_remove():
    inv = Inventory()
    p1 = Product("P101", "Notebook", 5.0, 20)
    p2 = Product("P102", "Pen", 1.5, 50)

    inv.add_product(p1)
    inv.add_product(p2)

    assert inv.get_product("P101") == p1
    assert inv.total_value() == (5.0 * 20) + (1.5 * 50)

    with pytest.raises(ValueError, match="already exists"):
        inv.add_product(p1)

    with pytest.raises(TypeError, match="Expected Product instance"):
        inv.add_product("not-a-product")

    removed = inv.remove_product("P101")
    assert removed == p1
    assert inv.get_product("P101") is None

    with pytest.raises(KeyError, match="not found"):
        inv.remove_product("NONEXISTENT")


def test_inventory_stock_management():
    inv = Inventory()
    p = Product("P201", "Cable", 10.0, 5)
    inv.add_product(p)

    inv.add_stock("P201", 10)
    assert p.stock == 15

    inv.remove_stock("P201", 5)
    assert p.stock == 10

    with pytest.raises(KeyError, match="not found"):
        inv.add_stock("P999", 5)

    with pytest.raises(KeyError, match="not found"):
        inv.remove_stock("P999", 5)


def test_inventory_alerts_and_reporting():
    today = date(2026, 11, 24)
    inv = Inventory()

    low_stock_item = Product("A1", "Charger", 19.99, 2)
    normal_item = Product("A2", "Power Bank", 39.99, 20)
    expired_item = ProductWithExpiryDate("A3", "Sandwich", 5.0, 4, "2026-11-20")

    inv.add_product(low_stock_item)
    inv.add_product(normal_item)
    inv.add_product(expired_item)

    low_items = inv.check_low_inventory(threshold=5)
    assert low_stock_item in low_items
    assert expired_item in low_items
    assert normal_item not in low_items

    expired_items = inv.check_expired_products(as_of=today)
    assert expired_items == [expired_item]

    report = inv.generate_report(low_stock_threshold=5, as_of=today)
    assert "Inventory Summary (3 items" in report
    assert "Low Stock Alerts:" in report
    assert "Expired Products:" in report
    assert "Charger (ID: A1, Stock: 2)" in report
    assert "Sandwich (ID: A3, Expired on: 2026-11-20)" in report
