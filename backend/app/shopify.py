import requests
from .config import SHOPIFY_STORE_URL, SHOPIFY_API_VERSION, HEADERS


BASE_URL = f"https://{SHOPIFY_STORE_URL}/admin/api/{SHOPIFY_API_VERSION}"


def find_product_by_handle(handle: str):
    url = f"{BASE_URL}/products.json?handle={handle}"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()

    products = resp.json().get("products", [])
    return products[0] if products else None


def create_product(product_payload: dict):
    url = f"{BASE_URL}/products.json"
    resp = requests.post(url, headers=HEADERS, json={"product": product_payload})
    resp.raise_for_status()
    return resp.json()["product"]


def update_product(product_id: int, product_payload: dict):
    url = f"{BASE_URL}/products/{product_id}.json"
    resp = requests.put(url, headers=HEADERS, json={"product": product_payload})
    resp.raise_for_status()
    return resp.json()["product"]


def get_variants(product_id: int):
    url = f"{BASE_URL}/products/{product_id}/variants.json"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json().get("variants", [])


def create_variant(product_id: int, payload: dict):
    url = f"{BASE_URL}/products/{product_id}/variants.json"
    resp = requests.post(
        url,
        headers=HEADERS,
        json={"variant": payload},
    )
    resp.raise_for_status()
    return resp.json()["variant"]


def update_variant(variant_id: int, payload: dict):
    url = f"{BASE_URL}/variants/{variant_id}.json"
    resp = requests.put(
        url,
        headers=HEADERS,
        json={"variant": payload},
    )
    resp.raise_for_status()
    return resp.json()["variant"]
