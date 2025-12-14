#!/usr/bin/env python3
"""
Test script to verify CRUD endpoints for stock management
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_product_crud():
    print("Testing Product CRUD endpoints...")

    # Test GET /products
    print("\n1. GET /products")
    response = requests.get(f"{BASE_URL}/products")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        products = response.json()
        print(f"Found {len(products)} products")
        if products:
            print(f"Sample product: {products[0]}")

    # Test GET /products/all
    print("\n2. GET /products/all")
    response = requests.get(f"{BASE_URL}/products/all")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        all_products = response.json()
        print(f"Found {len(all_products)} total products")

    # Test POST /products (Create)
    print("\n3. POST /products (Create)")
    new_product = {
        "name": "Test Product",
        "price": 50,
        "stock_qty": 10,
        "slot_no": "D1",
        "image_url": "https://example.com/test.jpg"
    }
    response = requests.post(f"{BASE_URL}/products", json=new_product)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        created = response.json()
        product_id = created["id"]
        print(f"Created product with ID: {product_id}")
    else:
        print(f"Error: {response.text}")
        return

    # Test GET /products/{id}
    print(f"\n4. GET /products/{product_id}")
    response = requests.get(f"{BASE_URL}/products/{product_id}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        product = response.json()
        print(f"Retrieved product: {product['name']}")

    # Test PUT /products/{id} (Update)
    print(f"\n5. PUT /products/{product_id} (Update)")
    update_data = {
        "name": "Updated Test Product",
        "price": 60,
        "stock_qty": 15
    }
    response = requests.put(f"{BASE_URL}/products/{product_id}", json=update_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        updated = response.json()
        print(f"Updated product: {updated['name']}, price: {updated['price']}, stock: {updated['stock']}")

    # Test DELETE /products/{id}
    print(f"\n6. DELETE /products/{product_id}")
    response = requests.delete(f"{BASE_URL}/products/{product_id}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("Product deleted successfully")

def test_money_stock_crud():
    print("\n\nTesting Money Stock CRUD endpoints...")

    # Test GET /money-stock
    print("\n1. GET /money-stock")
    response = requests.get(f"{BASE_URL}/money-stock")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        stocks = response.json()
        print(f"Found {len(stocks)} money stock denominations")
        if stocks:
            print(f"Sample stock: {stocks[0]}")

    # Test POST /money-stock (Create)
    print("\n2. POST /money-stock (Create)")
    new_stock = {
        "denom": 200,
        "quantity": 5,
        "type": "banknote"
    }
    response = requests.post(f"{BASE_URL}/money-stock", json=new_stock)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        created = response.json()
        print(f"Created money stock: {created}")
    else:
        print(f"Error: {response.text}")
        return

    # Test PUT /money-stock/{denom} (Update)
    print("\n3. PUT /money-stock/200 (Update)")
    update_data = {"quantity": 10}
    response = requests.put(f"{BASE_URL}/money-stock/200", json=update_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        updated = response.json()
        print(f"Updated money stock: {updated}")

    # Test DELETE /money-stock/{denom}
    print("\n4. DELETE /money-stock/200")
    response = requests.delete(f"{BASE_URL}/money-stock/200")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("Money stock deleted successfully")

if __name__ == "__main__":
    print("Stock Management CRUD API Test")
    print("=" * 40)

    try:
        test_product_crud()
        test_money_stock_crud()
        print("\n✅ All CRUD tests completed!")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API server. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")