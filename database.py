import mysql.connector
from mysql.connector import pooling, Error
from db_config import DB_CONFIG
class Database:

    def __init__(self):
        self.pool = None
        self._init_pool()

    def _init_pool(self):
        try:
            self.pool = pooling.MySQLConnectionPool(
                pool_name="esports_pool",
                pool_size=5,
                pool_reset_session=True,
                **DB_CONFIG
            )
            print("Пул соединений MySQL создан")
        except Error as e:
            print(f"Ошибка создания пула: {e}")
            self.pool = None

    def get_connection(self):
        if self.pool is None:
            print("Пул не создан")
            return None
        try:
            return self.pool.get_connection()
        except Error as e:
            print(f"Ошибка получения соединения из пула: {e}")
            return None

    def release_connection(self, conn):
        if conn is not None:
            conn.close()

    def close_all(self):
        if self.pool is None:
            return
        while True:
            try:
                conn = self.pool.get_connection()
                conn.close()
            except Error:
                break
        self.pool = None
        print("Пул соединений закрыт")

    def get_products(self):
        """Список моделей с суммарным остатком по всем вариантам."""
        conn = self.get_connection()
        if conn is None:
            return []

        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT
                    p.product_id,
                    p.name,
                    p.category,
                    p.manufacturer,
                    p.description,
                    p.composition,
                    p.base_price,
                    p.image_path,
                    COALESCE(s.total_quantity, 0) AS total_quantity
                FROM products p
                LEFT JOIN (
                    SELECT product_id, SUM(quantity) AS total_quantity
                    FROM stock_items
                    GROUP BY product_id
                ) s ON s.product_id = p.product_id
                ORDER BY p.product_id
            """)
            return cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Ошибка БД в get_products: {e}")
            return []
        finally:
            if cursor is not None:
                cursor.close()
            self.release_connection(conn)
db = Database()