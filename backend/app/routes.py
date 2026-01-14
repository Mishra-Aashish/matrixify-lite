from fastapi import APIRouter, UploadFile, File, HTTPException
from .parser import parse_file
from .shopify import (
    find_product_by_handle,
    create_product,
    update_product,
    get_variants,
    create_variant,
    update_variant,
)
from .merge import merge_product, merge_variant

router = APIRouter()


@router.post("/import/products")
async def import_products(file: UploadFile = File(...)):
    if not file.filename.endswith((".csv", ".xlsx")):
        raise HTTPException(status_code=400, detail="Only CSV or Excel supported")

    products = await parse_file(file)

    created = 0
    updated = 0

    for product in products:
        handle = product.get("handle")

        existing = None
        if handle:
            existing = find_product_by_handle(handle)

        product_payload = {
            "title": product.get("title"),
            "handle": product.get("handle"),
            "body_html": product.get("body_html"),
            "vendor": product.get("vendor"),
            "product_type": product.get("product_type"),
            "tags": product.get("tags"),
        }

        product_payload = {k: v for k, v in product_payload.items() if v}

        if existing:
            merged_payload = merge_product(existing, product_payload)
            product_obj = update_product(existing["id"], merged_payload)
            updated += 1
        else:
            product_obj = create_product(product_payload)
            created += 1

        existing_variants = get_variants(product_obj["id"])

        for v in product.get("variants", []):
            sku = v.get("sku")

            if not sku:
                continue

            match = next(
                (ev for ev in existing_variants if ev.get("sku") == sku),
                None,
            )

            variant_payload = {
                "sku": sku,
                "price": v.get("price"),
                "option1": v.get("option1_value"),
                "inventory_quantity": v.get("inventory_quantity"),
            }

            if match:
                merged_variant = merge_variant(match, variant_payload)
                update_variant(match["id"], merged_variant)
            else:
                create_variant(product_obj["id"], variant_payload)

    return {
        "products_created": created,
        "products_updated": updated,
    }
