from database import db

def main():
    conn = db.get_connection()
    if conn is None:
        print("Не удалось получить соединение")
        return

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM products")
        count = cursor.fetchone()[0]
        print(f"Количество товаров: {count}")
        cursor.close()
    except Exception as e:
        print(f"Ошибка запроса: {e}")
    finally:
        db.release_connection(conn)
        db.close_all()

if __name__ == "__main__":
    main()