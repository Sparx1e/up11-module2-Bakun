import sys
from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
)

BASE_DIR = Path(__file__).resolve().parent
RESOURCES = BASE_DIR / "resources"


def resource_path(*names: str) -> Path:
    """Ищет файл в resources/ по нескольким возможным именам."""
    for name in names:
        path = RESOURCES / name
        if path.exists():
            return path
    return RESOURCES / names[0]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Мир киберспорта — Каталог")
        self.resize(800, 600)

        icon_path = resource_path("icon.ico", "Мир киберспорта.ico")
        self.setWindowIcon(QIcon(str(icon_path)))

        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFFFFF;
                font-family: Calibri;
            }
            QLabel {
                color: #000000;
                font-family: Calibri;
            }
            QLabel#title {
                font-size: 24px;
                font-weight: bold;
                color: #000000;
                background-color: #D2F6E7;
                padding: 10px;
                border-radius: 6px;
            }
            QLabel#version {
                font-size: 12px;
                color: #000000;
            }
        """)

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        self.logo = QLabel()
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_path = resource_path("logo.png", "Мир киберспорта.png")
        pixmap = QPixmap(str(logo_path))

        if pixmap.isNull():
            placeholder = RESOURCES / "picture.png"
            pixmap = QPixmap(str(placeholder))

        if not pixmap.isNull():
            self.logo.setPixmap(
                pixmap.scaled(
                    420,
                    220,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )

        self.logo.setScaledContents(False)

        title = QLabel("Мир киберспорта — Каталог")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        version = QLabel("v1.0")
        version.setObjectName("version")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.logo)
        layout.addWidget(title)
        layout.addWidget(version)
        layout.addStretch()

        self.setCentralWidget(central)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())