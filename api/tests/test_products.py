import pytest

def test_get_products(client):
    response = client.get("/products")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 10  # From updated seed data
    
    # Check structure
    product = data[0]
    assert "id" in product
    assert "slot_no" in product
    assert "name" in product
    assert "price" in product
    assert "stock" in product
    
    # Check specific product
    mineral_water = next(p for p in data if p["name"] == "Mineral Water")
    assert mineral_water["price"] == 10
    assert mineral_water["slot_no"] == "A1"