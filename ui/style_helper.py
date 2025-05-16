from PyQt5.QtWidgets import QPushButton, QFrame, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class StyleHelper:
    @staticmethod
    def get_colors():
        return {
            'primary': '#3498db',
            'success': '#2ecc71',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'info': '#9b59b6',
            'background': '#f5f6fa',
            'text': '#2c3e50',
            'secondary_text': '#7f8c8d'
        }

    @staticmethod
    def set_button_style(button, color_name='primary', is_outlined=False):
        colors = StyleHelper.get_colors()
        color = colors.get(color_name, colors['primary'])
        if is_outlined:
            button.setStyleSheet(f"""
                QPushButton {{
                    color: {color};
                    background-color: transparent;
                    border-radius: 18px;
                    padding: 10px 15px;
                    font-size: 14px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {color};
                    color: white;
                }}
                QPushButton:pressed {{
                    background-color: {color};
                    color: white;
                }}
            """)
        else:
            button.setStyleSheet(f"""
                QPushButton {{
                    color: white;
                    background-color: {color};
                    border: none;
                    border-radius: 18px;
                    padding: 10px 15px;
                    font-size: 14px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {color}, stop:1 #2980b9);
                }}
                QPushButton:pressed {{
                    background-color: #2980b9;
                }}
            """)
        button.setCursor(Qt.PointingHandCursor)
        button.setMinimumHeight(45)

    @staticmethod
    def set_frame_style(frame, color_name='primary', radius=10):
        colors = StyleHelper.get_colors()
        color = colors.get(color_name, colors['primary'])
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: {radius}px;
                border: 1px solid #e1e1e1;
            }}
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 3)
        frame.setGraphicsEffect(shadow)