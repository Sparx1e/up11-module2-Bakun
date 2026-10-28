from decimal import Decimal
from typing import cast, Tuple
import mysql.connector
from db_config import DB_CONFIG


def calculate_price(product_id, base_price):
    if not isinstance(product_id, int) or product_id <= 0:
        print("Ошибка: product_id должен быть положительным целым числом")
        return None

    if not isinstance(base_price, (int, float, Decimal)):
        print("Ошибка: base_price должен быть числом")
        return None

    base_price = float(base_price)

    if base_price <= 0:
        print("Ошибка: цена должна быть > 0")
        return None

    conn = None
    cursor = None

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        sql = """
            SELECT COUNT(*)
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.order_id
            WHERE oi.product_id = %s
              AND o.order_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
        """

        cursor.execute(sql, (product_id,))
        result = cursor.fetchone()

        if result is not None:
            orders_count = cast(Tuple[int], result)[0]
        else:
            orders_count = 0

        if orders_count == 0:
            return base_price * 0.75
        return base_price

    except mysql.connector.Error as e:
        print(f"Ошибка БД: {e}")
        return None
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        return None
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()