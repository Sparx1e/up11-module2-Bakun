import mysql.connector
from typing import cast, Tuple

def calculate_price_mir_kibersporta(item_id, base_price):
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            database="esports_db",
            user="root",
            password="1234"
        )
        cursor = conn.cursor()

        sql = """
            SELECT COUNT(*) 
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.order_id
            WHERE oi.product_id = %s 
              AND o.order_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
        """
        
        cursor.execute(sql, (item_id,))
        result = cursor.fetchone()
        
        if result is not None:
            orders_count = cast(Tuple[int], result)[0]
        else:
            orders_count = 0

        if orders_count == 0:
            final_price = base_price * 0.75
        else:
            final_price = base_price

        return final_price

    except mysql.connector.Error as e:
        print(f"Ошибка БД: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

if __name__ == "__main__":
    test_item_id = 1
    test_base_price = 1490.0
    
    print(f"--- Тестирование функции для темы 'Мир киберспорта' ---")
    print(f"Товар ID: {test_item_id}, Базовая цена: {test_base_price} руб.")
    
    result = calculate_price_mir_kibersporta(test_item_id, test_base_price)
    
    if result is not None:
        discount_status = "ПРИМЕНЕНА (25%)" if result < test_base_price else "НЕ ПРИМЕНЕНА"
        print(f"Итоговая цена: {result} руб. (Скидка: {discount_status})")
    else:
        print("Программа не смогла рассчитать цену (см. ошибку выше).")