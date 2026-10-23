import mysql.connector

def calculate_price(product_id, base_price):
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

        cursor.execute(sql, (product_id,))

        result = cursor.fetchone()
        orders_count = result[0] # type: ignore

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
    result = calculate_price(1, 1000)
    print(f"Результат: {result}")