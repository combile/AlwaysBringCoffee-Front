from PyQt5.QtWidgets import QTextEdit, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor
from ui.style_helper import StyleHelper

class MessageLog(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setReadOnly(True)
        self.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #e1e1e1;
                padding: 10px;
                font-size: 13px;
                color: #2c3e50;
            }
            QScrollBar:vertical {
                border: none;
                background: #f1f1f1;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #bdc3c7;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

    def append_message(self, message, message_type='info'):
        colors = StyleHelper.get_colors()
        color_map = {
            'info': colors['info'],
            'success': colors['success'],
            'warning': colors['warning'],
            'danger': colors['danger'],
            'normal': colors['text']
        }
        color = color_map.get(message_type, colors['text'])
        self.append(f'<span style="color:{color};">{message}</span>')