import mysql.connector
from decimal import Decimal
from typing import cast, Tuple
from venv.db_config import DB_CONFIG
from discount import calculate_price

def main():
    conn = None
    cursor = None

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("SELECT product_id, name, base_price FROM products")
        raw_products = cursor.fetchall()

        if not raw_products:
            print("В таблице products нет данных.")
            return

        print(f"{'ID':<5} | {'Название':<20} | {'База':<8} | {'Итог':<8} | Скидка?")
        print("-" * 60)

        for raw_row in raw_products:
            product_id, name, price = cast(Tuple[int, str, Decimal], raw_row)
            price_f = float(price)

            final_price = calculate_price(product_id, price_f)

            if final_price is None:
                print(
                    f"{product_id:<5} | {name:<20} | "
                    f"{price_f:<8.2f} | {'—':<8} | ошибка"
                )
                continue

            discount_applied = "Да" if final_price < price_f else "Нет"
            print(
                f"{product_id:<5} | {name:<20} | {price_f:<8.2f} | "
                f"{final_price:<8.2f} | {discount_applied}"
            )

    except mysql.connector.Error as e:
        print(f"Ошибка БД: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    main()