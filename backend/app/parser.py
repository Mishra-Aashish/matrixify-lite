import pandas as pd


async def parse_file(file):
    if file.filename.endswith(".csv"):
        df = pd.read_csv(file.file)
    else:
        df = pd.read_excel(file.file)

    df = df.fillna("")

    products = {}

    for _, row in df.iterrows():
        handle = row.get("Handle")
        title = row.get("Title")

        if not handle and not title:
            continue

        key = handle or title

        if key not in products:
            products[key] = {
                "handle": handle,
                "title": title,
                "variants": []
            }

        products[key]["variants"].append({
            "sku": row.get("Variant SKU"),
            "price": to_float(row.get("Variant Price")),
            "inventory_quantity": to_int(row.get("Variant Inventory Qty")),
            "option1_name": row.get("Option1 Name"),
            "option1_value": row.get("Option1 Value"),
        })

    return list(products.values())


def to_float(val):
    try:
        return float(val)
    except:
        return None


def to_int(val):
    try:
        return int(val)
    except:
        return None
