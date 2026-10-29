import os
import mysql.connector
from db_config import DB_CONFIG
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RESOURCES = os.path.join(BASE_DIR, "resources")
IMAGES = os.path.join(RESOURCES, "Images")
PLACEHOLDER = os.path.join(RESOURCES, "picture.png")


def main() -> None:
    print("=" * 70)
    print("ПРОВЕРКА ФАЙЛОВ ИЗОБРАЖЕНИЙ")
    print("=" * 70)

    print(f"\n[1] Заглушка picture.png")
    print(f"    Путь:    {PLACEHOLDER}")
    print(f"    Файл:    {'+ есть' if os.path.exists(PLACEHOLDER) else '- НЕТ'}")
    print(f"    Это файл: {'+ да' if os.path.isfile(PLACEHOLDER) else '- нет'}")

    conn = None
    cur = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(
            "SELECT product_id, name, image_path FROM products ORDER BY product_id;"
        )
        rows = cur.fetchall()

        print(f"\n[2] Проверка {len(rows)} путей из таблицы products")
        print(f"{'ID':<4} {'Наименование':<32} {'image_path':<20} {'Файл?':<6}")
        print("-" * 70)

        found, missing, empty = 0, 0, 0
        for product_id, name, image_path in rows:
            name_short = (name or "")[:30] # type: ignore
            if not image_path:
                empty += 1
                print(f"{product_id:<4} {name_short:<32} {'(пусто)':<20} {'—':<6}")
                continue
            full_path = os.path.join(IMAGES, image_path) # type: ignore
            exists = os.path.exists(full_path)
            if exists:
                found += 1
            else:
                missing += 1
            print(f"{product_id:<4} {name_short:<32} {image_path[:20]:<20} " # type: ignore
                  f"{'+' if exists else '-':<6}")

        print("-" * 70)
        print(f"Итого: файлов найдено {found}, отсутствует {missing}, "
              f"пустой путь {empty}")

    except mysql.connector.Error as e:
        print(f"Ошибка БД: {e}")
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

    sample = os.path.join(IMAGES, "IMG_21_001.png")
    print(f"\n[3] Точечная проверка IMG_21_001.png")
    print(f"    Существует: {'+ Да' if os.path.exists(sample) else '- Нет'}")


if __name__ == "__main__":
    main()