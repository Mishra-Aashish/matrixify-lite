def merge_product(existing: dict, incoming: dict) -> dict:
    merged = {}

    fields = [
        "title",
        "body_html",
        "vendor",
        "product_type",
        "tags",
        "handle",
    ]

    for field in fields:
        if incoming.get(field):
            merged[field] = incoming[field]

    merged["id"] = existing["id"]
    return merged


def merge_variant(existing: dict, incoming: dict) -> dict:
    merged = {}

    fields = [
        "price",
        "sku",
        "option1",
        "option2",
        "option3",
        "inventory_quantity",
    ]

    for field in fields:
        if incoming.get(field) is not None:
            merged[field] = incoming[field]

    merged["id"] = existing["id"]
    return merged
