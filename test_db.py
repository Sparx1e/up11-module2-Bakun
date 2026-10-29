from database import db


def main():
    products = db.get_products()
    print(f"Количество товаров: {len(products)}")

    for p in products[:3]:
        print(
            p["product_id"],
            p["manufacturer"],
            "|", p["name"],
            "|", p["base_price"],
            "| остаток:", p["total_quantity"],
        )

    db.close_all()


if __name__ == "__main__":
    main()