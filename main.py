import sys
from PyQt5.QtWidgets import QApplication
from core.altino_app import AltinoVoiceSafetyApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    from PyQt5.QtGui import QFont
    font = QFont("Segoe UI", 9)
    app.setFont(font)
    
    window = AltinoVoiceSafetyApp()
    window.show()
    sys.exit(app.exec_())