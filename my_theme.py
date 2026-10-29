from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout, QWidget
)

BASE_DIR = Path(__file__).resolve().parent
RESOURCES = BASE_DIR / "resources"

LOW_STOCK_THRESHOLD = 3


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

    background = "#ff8080" if total <= LOW_STOCK_THRESHOLD else "#FFFFFF"

    card = QFrame()
    card.setObjectName("card")
    card.setStyleSheet(
        f"""
        QFrame#card {{
            background-color: {background};
            border: 1px solid #CCCCCC;
            border-radius: 8px;
        }}
        """
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
                120,
                120,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

    layout.addWidget(image_label)

    text_layout = QVBoxLayout()
    text_layout.setSpacing(4)

    title = QLabel(
        f"{product.get('manufacturer', '')} | {product.get('name', '')}"
    )
    title.setStyleSheet("font-size: 16px; font-weight: bold;")

    category = QLabel(str(product.get("category") or ""))

    if total <= 0:
        quantity_text = "Недоступно для заказа"
    else:
        quantity_text = f"Доступно: {total} шт."

    quantity = QLabel(quantity_text)

    composition = QLabel(
        f"Состав: {product.get('composition') or '—'}"
    )
    composition.setWordWrap(True)

    text_layout.addWidget(title)
    text_layout.addWidget(category)
    text_layout.addWidget(quantity)
    text_layout.addWidget(composition)
    text_layout.addStretch()

    layout.addLayout(text_layout, 1)

    price = QLabel(
        f"от {float(product.get('base_price') or 0):.2f} ₽"
    )
    price.setStyleSheet("font-size: 18px; font-weight: bold;")
    price.setAlignment(
        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
    )

    layout.addWidget(price)

    return card