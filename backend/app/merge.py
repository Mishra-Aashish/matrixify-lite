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

    if incoming is None:
        raise ValueError("Incoming product data cannot be None")

    for field in fields:
        if incoming.get(field):
            merged[field] = incoming[field]

    if existing and "id" in existing:
     merged["id"] = existing["id"]
     merged["action"] = "update"
    else:
        merged["action"] = "create"

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

    if incoming is None:
        raise ValueError("Incoming variant data cannot be None")

    for field in fields:
        if incoming.get(field) is not None:
            merged[field] = incoming[field]

    if existing and "id" in existing:
     merged["id"] = existing["id"]
     merged["action"] = "update"
    else:
       merged["action"] = "create"
    return merged
