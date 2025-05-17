from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor

class DashboardItem(QFrame):
    def __init__(self, title, icon, parent=None):
        super().__init__(parent)
        self.setup_ui(title, icon)

    def setup_ui(self, title, icon):
        self.setMinimumSize(QSize(120, 120))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignCenter)

        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 32px;")

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")

        layout.addWidget(icon_label)
        layout.addWidget(title_label)

        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #e1e1e1;
            }
            QFrame:hover {
                background-color: #f8f9fa;
                border: 1px solid #3498db;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 3)
        self.setGraphicsEffect(shadow)