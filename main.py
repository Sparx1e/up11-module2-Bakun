import sys
from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QScrollArea, QFrame, QSizePolicy
)
from database import db

BASE_DIR = Path(__file__).resolve().parent
RESOURCES = BASE_DIR / "resources"

LOW_STOCK_THRESHOLD = 3
RESOURCES = Path(__file__).resolve().parent / "resources"


def resource_path(*names: str) -> Path:
    for name in names:
        path = RESOURCES / name
        if path.exists():
            return path
    return RESOURCES / names[0]

def load_product_pixmap(product: dict) -> QPixmap:
    """
    Возвращает QPixmap: сначала пробует image_path из БД,
    затем — заглушку picture.png. Если и её нет — null-QPixmap.
    """
    image_name = (product.get("image_path") or "").strip()
    candidates = []

    if image_name:
        candidates.append(RESOURCES / "Images" / image_name)
        candidates.append(RESOURCES / image_name)

    candidates.append(RESOURCES / "picture.png")

    for path in candidates:
        if not path.exists():
            continue
        pixmap = QPixmap(str(path))
        if not pixmap.isNull():
            return pixmap
    return QPixmap()

def product_image_path(product: dict) -> Path:
    image_name = (product.get("image_path") or "").strip()
    candidates = []

    if image_name:
        candidates.append(RESOURCES / "Images" / image_name)
        candidates.append(RESOURCES / image_name)

    candidates.append(RESOURCES / "picture.png")

    for path in candidates:
        if path.exists():
            return path
    return RESOURCES / "picture.png"


def create_card(product: dict) -> QFrame:
    total = int(product.get("total_quantity") or 0)

    bg = "#ff8080" if total <= LOW_STOCK_THRESHOLD else "#FFFFFF"

    card = QFrame()
    card.setObjectName("card")
    card.setStyleSheet(
        f"QFrame#card {{ background-color: {bg}; "
        f"border: 1px solid #CCCCCC; border-radius: 8px; }}"
    )
    card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed) # type: ignore

    layout = QHBoxLayout(card)
    layout.setContentsMargins(12, 12, 12, 12)
    layout.setSpacing(12)

    image_label = QLabel()
    image_label.setFixedSize(120, 120)
    image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    pixmap = QPixmap(str(product_image_path(product)))
    if not pixmap.isNull():
        image_label.setPixmap(
            pixmap.scaled(
                120, 120,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
    layout.addWidget(image_label)
    image_label = QLabel()
    image_label.setFixedSize(120, 120)
    image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    pixmap = load_product_pixmap(product)
    if not pixmap.isNull():
        image_label.setPixmap(
            pixmap.scaled(
                120, 120,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
    layout.addWidget(image_label)

    text_layout = QVBoxLayout()
    text_layout.setSpacing(4)

    title = QLabel(f"{product.get('manufacturer', '')} | {product.get('name', '')}")
    title.setStyleSheet("font-size: 16px; font-weight: bold;")

    category = QLabel(str(product.get("category") or ""))

    if total <= 0:
        qty_text = "Недоступно для заказа"
    else:
        qty_text = f"Доступно: {total} шт."
    quantity = QLabel(qty_text)

    composition = QLabel(f"Состав: {product.get('composition') or '—'}")
    composition.setWordWrap(True)

    text_layout.addWidget(title)
    text_layout.addWidget(category)
    text_layout.addWidget(quantity)
    text_layout.addWidget(composition)
    text_layout.addStretch()

    layout.addLayout(text_layout, 1)

    price = QLabel(f"от {float(product.get('base_price') or 0):.2f} ₽")
    price.setStyleSheet("font-size: 18px; font-weight: bold;")
    price.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
    layout.addWidget(price)

    return card


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = db

        self.setWindowTitle("Мир киберспорта — Каталог")
        self.resize(900, 700)

        icon_path = resource_path("icon.ico", "Мир киберспорта.ico")
        self.setWindowIcon(QIcon(str(icon_path)))

        self.setStyleSheet("""
            QMainWindow { background-color: #FFFFFF; font-family: Calibri; }
            QLabel { color: #000000; font-family: Calibri; }
            QLabel#title {
                font-size: 24px;
                font-weight: bold;
                background-color: #D2F6E7;
                padding: 10px;
                border-radius: 6px;
            }
            QFrame#card QLabel { background: transparent; }
        """)

        central = QWidget()
        root = QVBoxLayout(central)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(12)

        self.logo = QLabel()
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_path = resource_path("logo.png", "Мир киберспорта.png")
        pixmap = QPixmap(str(logo_path))
        if pixmap.isNull():
            pixmap = QPixmap(str(RESOURCES / "picture.png"))

        if not pixmap.isNull():
            self.logo.setPixmap(
                pixmap.scaled(
                    420, 180,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )

        title = QLabel("Мир киберспорта — Каталог")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        root.addWidget(self.logo)
        root.addWidget(title)

        self.scroll = QScrollArea() # type: ignore
        self.scroll.setWidgetResizable(True) # type: ignore

        self.container = QWidget()
        self.catalog_layout = QVBoxLayout(self.container)
        self.catalog_layout.setSpacing(10)

        self.scroll.setWidget(self.container) # type: ignore
        root.addWidget(self.scroll, 1) # type: ignore

        self.setCentralWidget(central)
        self.load_catalog()

    def load_catalog(self):
        while self.catalog_layout.count():
            item = self.catalog_layout.takeAt(0)
            assert item is not None
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        products = self.db.get_products()
        print(f"Загружено моделей: {len(products)}")

        for product in products:
            self.catalog_layout.addWidget(create_card(product))

        self.catalog_layout.addStretch()
        products = self.db.get_products()

    def closeEvent(self, event):
        self.db.close_all()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())