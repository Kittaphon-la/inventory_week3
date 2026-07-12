import json

import pytest

from test_app import (
    DEFAULT_INVENTORY,
    add_or_update_product,
    calculate_inventory_summary,
    cut_stock,
    load_inventory,
    normalize_inventory,
    save_inventory,
)


@pytest.fixture
def inventory():
    return {
        product_id: product.copy()
        for product_id, product in DEFAULT_INVENTORY.items()
    }


def test_load_default_inventory_when_file_does_not_exist(tmp_path):
    result = load_inventory(str(tmp_path / "missing.json"))

    assert result == DEFAULT_INVENTORY
    assert result is not DEFAULT_INVENTORY


def test_normalize_original_short_keys():
    old_data = {
        "101": {"n": "Mama Noodles", "q": 50, "p": 6.0, "c": "Food"}
    }

    result = normalize_inventory(old_data)

    assert result["101"] == {
        "name": "Mama Noodles",
        "qty": 50,
        "price": 6.0,
        "category": "Food",
    }


def test_save_and_load_inventory(tmp_path, inventory):
    db_file = tmp_path / "data.json"

    save_inventory(inventory, str(db_file))
    loaded = load_inventory(str(db_file))

    assert loaded == inventory


def test_saved_json_is_readable(tmp_path, inventory):
    db_file = tmp_path / "data.json"

    save_inventory(inventory, str(db_file))

    with db_file.open("r", encoding="utf-8") as file:
        saved = json.load(file)

    assert saved["101"]["name"] == "Mama Noodles"


def test_add_new_product(inventory):
    add_or_update_product(
        inventory, "104", "Pepsi", 12, 15.0, "Drink"
    )

    assert inventory["104"] == {
        "name": "Pepsi",
        "qty": 12,
        "price": 15.0,
        "category": "Drink",
    }


def test_update_existing_product(inventory):
    add_or_update_product(
        inventory, "101", "Mama New", 60, 7.0, "Food"
    )

    assert inventory["101"]["name"] == "Mama New"
    assert inventory["101"]["qty"] == 60
    assert inventory["101"]["price"] == 7.0


@pytest.mark.parametrize(
    ("product_id", "name", "qty", "price", "category"),
    [
        ("", "Pepsi", 10, 15.0, "Drink"),
        ("104", "", 10, 15.0, "Drink"),
        ("104", "Pepsi", -1, 15.0, "Drink"),
        ("104", "Pepsi", 10, -1.0, "Drink"),
        ("104", "Pepsi", 10, 15.0, ""),
    ],
)
def test_add_or_update_rejects_invalid_data(
    inventory, product_id, name, qty, price, category
):
    with pytest.raises(ValueError):
        add_or_update_product(
            inventory, product_id, name, qty, price, category
        )


def test_cut_stock_success(inventory):
    success, message = cut_stock(inventory, "101", 10)

    assert success is True
    assert message == "Stock updated."
    assert inventory["101"]["qty"] == 40


def test_cut_stock_low_stock_warning(inventory):
    inventory["101"]["qty"] = 6

    success, message = cut_stock(inventory, "101", 2)

    assert success is True
    assert "WARNING" in message
    assert inventory["101"]["qty"] == 4


def test_cut_stock_rejects_insufficient_stock(inventory):
    success, message = cut_stock(inventory, "102", 25)

    assert success is False
    assert message == "Not enough stock."
    assert inventory["102"]["qty"] == 20


def test_cut_stock_rejects_unknown_product(inventory):
    success, message = cut_stock(inventory, "999", 1)

    assert success is False
    assert message == "Product not found."


@pytest.mark.parametrize("amount", [0, -1])
def test_cut_stock_rejects_non_positive_amount(inventory, amount):
    success, message = cut_stock(inventory, "101", amount)

    assert success is False
    assert message == "Amount must be greater than zero."
    assert inventory["101"]["qty"] == 50


def test_calculate_inventory_summary(inventory):
    total_types, total_value, low_stock = calculate_inventory_summary(inventory)

    assert total_types == 3
    assert total_value == pytest.approx(1540.0)
    assert low_stock == []


def test_calculate_low_stock_list(inventory):
    inventory["101"]["qty"] = 4
    inventory["102"]["qty"] = 9

    _, _, low_stock = calculate_inventory_summary(inventory)

    assert low_stock == ["Mama Noodles", "Lactasoy Milk"]
