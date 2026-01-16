from app.merge import merge_product


def test_merge_creates_product_when_not_exists():
    incoming_product = {
        "handle": "test-product",
        "title": "Test Product"
    }

    existing_product = None

    result = merge_product(existing_product, incoming_product)

    assert result["action"] == "create"

def test_merge_updates_product_when_exists():
    incoming_product = {
        "handle": "test-product",
        "title": "Updated Product Title"
    }

    existing_product = {
        "id": 123,
        "handle": "test-product",
        "title": "Old Product Title"
    }

    result = merge_product(existing_product, incoming_product)

    assert result["action"] == "update"

