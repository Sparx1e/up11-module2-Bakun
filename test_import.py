import PySide6
import psycopg2
import PyInstaller
print("Все библиотеки работают!")

def check_login(login):
    conn = psycopg2.connect(
        dbname="cybersport",
        user="root",
        password="1234",
        host="127.0.0.1",
        port="3306"
    )
    cur = conn.cursor()
    cur.execute("SELECT role FROM users WHERE login = %s;", (login,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        role = row[0]
        return f"Вход разрешён. Роль: {role}"
    else:
        return "Ошибка: неверный логин"

def calculate_price(price: float, has_orders: bool) -> float:
    """
    Если заказов за месяц нет, применяется скидка 25%.
    """
    if not has_orders:
        return price * 0.75
    else:
        return price