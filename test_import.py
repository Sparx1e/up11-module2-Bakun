import PySide6
import mysql.connector
import PyInstaller
from venv.db_config import DB_CONFIG
from typing import Any, cast, Tuple

print("Все библиотеки работают!")


def check_login(login):
    conn = None
    cur = None

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("SELECT role FROM users WHERE login = %s;", (login,))
        row = cur.fetchone()

        if row is not None:
            row_t = cast(Tuple[str], row)
            return f"Вход разрешён. Роль: {row_t[0]}"
        return "Ошибка: неверный логин"

    except mysql.connector.Error as e:
        return f"Ошибка БД: {e}"
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def calculate_price(price: float, has_orders: bool) -> float:
    """
    Если заказов за месяц нет, применяется скидка 25%.
    """
    if not has_orders:
        return price * 0.75
    return price


if __name__ == "__main__":
    print(check_login("admin"))
    print(check_login("unknown_login"))