import mysql.connector
from discount import calculate_price

try:
    conn = mysql.connector.connect(
        host="127.0.0.1", 
        database="esports_db",
        user="root", 
        password="wrong"
    )
    cursor = conn.cursor()

    cursor.execute("SELECT product_id, name, base_price FROM products")
    products = cursor.fetchall()

    print(f"{'ID':<5} | {'Название':<20} | {'База':<8} | {'Итог':<8} | Скидка?")
    print("-" * 60)

    for prod in products:
        product_id, name, price = prod
        final_price = calculate_price(product_id, price)

        discount_applied = "Да" if final_price < price else "Нет" # type: ignore
        
        print(f"{product_id:<5} | {name:<20} | {price:<8} | {final_price:<8} | {discount_applied}")

except mysql.connector.Error as e:
    print(f"Ошибка: {e}")
finally:
    if 'cursor' in locals(): cursor.close()
    if 'conn' in locals(): conn.close()