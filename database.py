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
        """Закрывает все соединения пула (эмуляция closeall)."""
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
        ...
db = Database()