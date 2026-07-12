import json
import os
from typing import Any

DB_FILE = "data.json"

DEFAULT_INVENTORY: dict[str, dict[str, Any]] = {
    "101": {"name": "Mama Noodles", "qty": 50, "price": 6.0, "category": "Food"},
    "102": {"name": "Lactasoy Milk", "qty": 20, "price": 12.0, "category": "Drink"},
    "103": {"name": "Singha Water", "qty": 100, "price": 10.0, "category": "Drink"},
}


def load_inventory(db_file: str = DB_FILE) -> dict[str, dict[str, Any]]:
    """Load inventory from JSON, or return a fresh copy of the default inventory."""
    if not os.path.exists(db_file):
        return {product_id: product.copy() for product_id, product in DEFAULT_INVENTORY.items()}

    try:
        with open(db_file, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"Cannot load inventory file: {error}") from error

    return normalize_inventory(data)


def normalize_inventory(data: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Support both the original short keys and the refactored descriptive keys."""
    normalized: dict[str, dict[str, Any]] = {}

    for product_id, product in data.items():
        normalized[str(product_id)] = {
            "name": product.get("name", product.get("n", "")),
            "qty": int(product.get("qty", product.get("q", 0))),
            "price": float(product.get("price", product.get("p", 0.0))),
            "category": product.get("category", product.get("c", "")),
        }

    return normalized


def save_inventory(inventory: dict[str, dict[str, Any]], db_file: str = DB_FILE) -> None:
    """Save inventory safely by writing a temporary file before replacing the database."""
    temp_file = f"{db_file}.tmp"

    try:
        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump(inventory, file, ensure_ascii=False, indent=2)
        os.replace(temp_file, db_file)
    except OSError as error:
        if os.path.exists(temp_file):
            os.remove(temp_file)
        raise RuntimeError(f"Cannot save inventory file: {error}") from error


def add_or_update_product(
    inventory: dict[str, dict[str, Any]],
    product_id: str,
    name: str,
    qty: int,
    price: float,
    category: str,
) -> None:
    product_id = product_id.strip()
    name = name.strip()
    category = category.strip()

    if not product_id:
        raise ValueError("Product ID cannot be empty.")
    if not name:
        raise ValueError("Product name cannot be empty.")
    if qty < 0:
        raise ValueError("Quantity cannot be negative.")
    if price < 0:
        raise ValueError("Price cannot be negative.")
    if not category:
        raise ValueError("Category cannot be empty.")

    inventory[product_id] = {
        "name": name,
        "qty": qty,
        "price": float(price),
        "category": category,
    }


def cut_stock(
    inventory: dict[str, dict[str, Any]],
    product_id: str,
    amount: int,
) -> tuple[bool, str]:
    if product_id not in inventory:
        return False, "Product not found."
    if amount <= 0:
        return False, "Amount must be greater than zero."
    if inventory[product_id]["qty"] < amount:
        return False, "Not enough stock."

    inventory[product_id]["qty"] -= amount

    if inventory[product_id]["qty"] < 5:
        return True, "Stock updated. WARNING: Item is running very low in stock."

    return True, "Stock updated."


def calculate_inventory_summary(
    inventory: dict[str, dict[str, Any]],
    low_stock_threshold: int = 10,
) -> tuple[int, float, list[str]]:
    total_product_types = len(inventory)
    total_value = sum(product["qty"] * product["price"] for product in inventory.values())
    low_stock = [
        product["name"]
        for product in inventory.values()
        if product["qty"] < low_stock_threshold
    ]
    return total_product_types, total_value, low_stock


def show_all(inventory: dict[str, dict[str, Any]]) -> None:
    print("-" * 75)

    if not inventory:
        print("No products found.")
    else:
        for product_id, product in inventory.items():
            print(
                f"ID: {product_id} | Name: {product['name']} | "
                f"Stock: {product['qty']} | Price: {product['price']:.2f} THB | "
                f"Type: {product['category']}"
            )

    print("-" * 75)


def read_integer(prompt: str, minimum: int = 0) -> int:
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter an integer.")
            continue

        if value < minimum:
            print(f"Value must be at least {minimum}.")
            continue

        return value


def read_float(prompt: str, minimum: float = 0.0) -> float:
    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if value < minimum:
            print(f"Value must be at least {minimum}.")
            continue

        return value


def add_or_update_menu(inventory: dict[str, dict[str, Any]]) -> None:
    product_id = input("Enter ID: ").strip()
    name = input("Enter Name: ").strip()
    qty = read_integer("Enter Qty: ", minimum=0)
    price = read_float("Enter Price: ", minimum=0.0)
    category = input("Enter Category: ").strip()

    try:
        add_or_update_product(inventory, product_id, name, qty, price, category)
    except ValueError as error:
        print(f"Error: {error}")
        return

    save_inventory(inventory)
    print("Product saved.")


def cut_stock_menu(inventory: dict[str, dict[str, Any]]) -> None:
    product_id = input("Enter product ID to cut stock: ").strip()
    amount = read_integer("How many items out?: ", minimum=1)

    success, message = cut_stock(inventory, product_id, amount)
    print(message)

    if success:
        save_inventory(inventory)


def check_inventory_menu(inventory: dict[str, dict[str, Any]]) -> None:
    total_types, total_value, low_stock = calculate_inventory_summary(inventory)

    print(f"Total product types: {total_types}")
    print(f"Total inventory value: {total_value:.2f} THB")
    print(f"Alert low stock (<10): {', '.join(low_stock) if low_stock else 'None'}")


def main() -> None:
    try:
        inventory = load_inventory()
    except RuntimeError as error:
        print(error)
        return

    while True:
        print("\n=== INVENTORY SYSTEM v2.0 ===")
        print("1. Show all")
        print("2. Add or Update")
        print("3. Out")
        print("4. Check Inventory")
        print("5. Exit")

        choice = input("Select menu: ").strip()

        try:
            if choice == "1":
                show_all(inventory)
            elif choice == "2":
                add_or_update_menu(inventory)
            elif choice == "3":
                cut_stock_menu(inventory)
            elif choice == "4":
                check_inventory_menu(inventory)
            elif choice == "5":
                print("Bye")
                break
            else:
                print("Invalid choice, try again.")
        except RuntimeError as error:
            print(f"File error: {error}")


if __name__ == "__main__":
    main()
