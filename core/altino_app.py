import time
import speech_recognition as sr
from PyQt5.QtCore import Qt, QSize, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QStatusBar, QGraphicsDropShadowEffect)

from AltinoLite import *
from ui.style_helper import StyleHelper
from ui.message_log import MessageLog
from ui.dashboard_item import DashboardItem

class AltinoVoiceSafetyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 먼저 상태 변수 초기화
        self.connection_status = "연결 중..."
        self.current_speed = 0
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_count = 0
        self.is_listening = False
        self.recognizer = sr.Recognizer()

        self.initUI()  # 나중에 호출

        Open()  # Altino 차량 연결
        
    def initUI(self):
        self.setWindowTitle('Altino 안전 음성 시스템')
        self.setStyleSheet(f"background-color: {StyleHelper.get_colors()['background']};")
        
        # 중앙 위젯 설정
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        self.setCentralWidget(central_widget)
        
        # 상단 상태 프레임
        self.status_frame = QFrame()
        status_layout = QHBoxLayout(self.status_frame)
        status_layout.setContentsMargins(15, 15, 15, 15)
        
        # 상태 레이블
        self.status_label = QLabel("상태: " + self.connection_status)
        self.status_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #3498db;
        """)
        
        # 속도 레이블
        self.speed_label = QLabel(f"현재 속도: {self.current_speed} km/h")
        self.speed_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #2c3e50;
        """)
        
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        status_layout.addWidget(self.speed_label)
        
        # 대시보드 프레임
        dashboard_frame = QFrame()
        dashboard_layout = QHBoxLayout(dashboard_frame)
        dashboard_layout.setContentsMargins(0, 0, 0, 0)
        dashboard_layout.setSpacing(15)
        
        # 대시보드 아이템 추가
        self.dashboard_items = [
            DashboardItem("건강 상태", "❤️"),
            DashboardItem("비상 상황", "🚨"),
            DashboardItem("속도 제어", "🚗"),
            DashboardItem("음성 제어", "🎙️")
        ]
        
        for item in self.dashboard_items:
            dashboard_layout.addWidget(item)
        
        # 로그 메시지 영역
        self.text_area = MessageLog()
        self.text_area.setMinimumHeight(200)
        
        # 버튼 프레임
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(15)
        
        # 음성 인식 버튼
        self.btn_listen = QPushButton('🎙️ 음성 인식 시작')
        self.btn_listen.clicked.connect(self.run_voice_recognition)
        StyleHelper.set_button_style(self.btn_listen, 'primary')
        
        # 비상 정지 버튼
        self.btn_emergency = QPushButton('🚨 비상 정지')
        self.btn_emergency.clicked.connect(self.emergency_stop)
        StyleHelper.set_button_style(self.btn_emergency, 'danger')
        
        
        # 버튼 배치
        button_layout.addWidget(self.btn_listen)
        button_layout.addWidget(self.btn_emergency)
        
        # 레이아웃에 위젯 추가
        main_layout.addWidget(self.status_frame)
        main_layout.addWidget(dashboard_frame)
        main_layout.addWidget(self.text_area)
        main_layout.addWidget(button_frame)
        
        # 상태바 추가
        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet("""
            QStatusBar {
                background-color: #2c3e50;
                color: white;
                font-weight: bold;
            }
        """)
        self.statusBar.showMessage("시스템 준비 완료")
        self.setStatusBar(self.statusBar)
        
        # 창 크기 설정
        self.resize(600, 550)
        
        # 시작 메시지 추가
        self.text_area.append_message("✅ Altino 시스템이 시작되었습니다.", 'success')
        self.text_area.append_message("🔄 차량과 연결 중...", 'info')
        
        # 연결 시뮬레이션
        QTimer.singleShot(2000, self.simulate_connection)

    def simulate_connection(self):
        self.connection_status = "연결됨"
        self.status_label.setText("상태: " + self.connection_status)
        self.status_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #2ecc71;
        """)
        self.text_area.append_message("✓ 차량과 연결되었습니다.", 'success')
        self.statusBar.showMessage("차량 연결 성공 | 음성 인식 준비 완료")

    def update_animation(self):
        if self.is_listening:
            animation_texts = ["🎙️ 듣는 중", "🎙️ 듣는 중.", "🎙️ 듣는 중..", "🎙️ 듣는 중..."]
            self.btn_listen.setText(animation_texts[self.animation_count % len(animation_texts)])
            self.animation_count += 1

    def run_voice_recognition(self):
        if self.is_listening:
            return
        
        self.is_listening = True
        self.animation_count = 0
        self.animation_timer.start(300)
        self.btn_listen.setEnabled(False)
        StyleHelper.set_button_style(self.btn_listen, 'warning')
        
        self.text_area.append_message("🟡 음성 인식 중...", 'warning')
        
        QTimer.singleShot(100, self.perform_voice_recognition)
    
    def perform_voice_recognition(self):
        try:
            with sr.Microphone() as source:
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio, language='ko-KR')
                
                # 애니메이션 중지
                self.animation_timer.stop()
                self.is_listening = False
                self.btn_listen.setEnabled(True)
                StyleHelper.set_button_style(self.btn_listen, 'primary')
                self.btn_listen.setText('🎙️ 음성 인식 시작')
                
                self.text_area.append_message(f"🟢 인식된 말: {text}", 'success')
                self.handle_command(text)
                
        except Exception as e:
            # 애니메이션 중지
            self.animation_timer.stop()
            self.is_listening = False
            self.btn_listen.setEnabled(True)
            StyleHelper.set_button_style(self.btn_listen, 'primary')
            self.btn_listen.setText('🎙️ 음성 인식 시작')
            
            self.text_area.append_message(f"🔴 인식 실패: {str(e)}", 'danger')

    def handle_command(self, text):
        # 건강 이상 키워드
        if any(word in text for word in ["어지러워", "가슴 아파", "숨 막혀", "눈이 안 보여"]):
            self.text_area.append_message("🚨 건강 이상 감지됨! 차량 정지", 'danger')
            self.text_area.append_message("📞 주변 응급센터에 연결합니다.", 'info')
            self.stop_vehicle()
            
            # 대시보드 업데이트 - 건강 상태 아이템 강조
            self.dashboard_items[0].setStyleSheet("""
                QFrame {
                    background-color: #fef2f2;
                    border-radius: 10px;
                    border: 2px solid #e74c3c;
                }
            """)

        # 과속
        elif "과속" in text:
            self.text_area.append_message("⚠️ 과속 감지됨! 속도 증가", 'warning')
            self.update_speed(600)
            Go(600, 600)
            
            # 대시보드 업데이트 - 속도 제어 아이템 강조
            self.dashboard_items[2].setStyleSheet("""
                QFrame {
                    background-color: #fff8e6;
                    border-radius: 10px;
                    border: 2px solid #f39c12;
                }
            """)

        # 비상
        elif any(word in text for word in ["도와줘", "살려줘"]):
            self.text_area.append_message("🚨 비상 상황! 정지 및 경고음", 'danger')
            Led(15)
            sound(37)
            self.stop_vehicle()
            
            # 대시보드 업데이트 - 비상 상황 아이템 강조
            self.dashboard_items[1].setStyleSheet("""
                QFrame {
                    background-color: #fef2f2;
                    border-radius: 10px;
                    border: 2px solid #e74c3c;
                }
            """)

        # 정상 운전 복귀
        elif any(word in text for word in ["괜찮아", "아니야", "취소"]):
            self.text_area.append_message("✅ 비상 해제됨. 정상 주행", 'success')
            Led(0)
            self.update_speed(300)
            Go(300, 300)
            
            # 대시보드 초기화
            for item in self.dashboard_items:
                item.setStyleSheet("""
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

        else:
            self.text_area.append_message("ℹ️ 인식된 명령어에 대한 동작 없음", 'info')

    def emergency_stop(self):
        self.text_area.append_message("⚠️ 비상 정지 버튼이 눌렸습니다!", 'danger')
        self.stop_vehicle()
        
        # 비상 상황 시각적 효과
        self.flash_emergency()

    def flash_emergency(self):
        self.dashboard_items[1].setStyleSheet("""
            QFrame {
                background-color: #e74c3c;
                border-radius: 10px;
                border: 2px solid #c0392b;
                color: white;
            }
        """)
        
        # 0.5초 후 원래 상태로 복귀
        QTimer.singleShot(500, lambda: self.dashboard_items[1].setStyleSheet("""
            QFrame {
                background-color: #fef2f2;
                border-radius: 10px;
                border: 2px solid #e74c3c;
            }
        """))

    def stop_vehicle(self):
        # 점점 속도 줄이면서 정지 + 경고음
        for speed in range(500, 0, -100):
            self.update_speed(speed)
            Go(speed, speed)
            sound(61)
            Delay(100)
            sound(58)
            Delay(100)
            delay(500)
        Sound(0)
        self.update_speed(0)
        Go(0, 0)
        Steering(0)

    def update_speed(self, speed):
        self.current_speed = speed // 10  # 표시용 속도 변환
        self.speed_label.setText(f"현재 속도: {self.current_speed} km/h")
        
        # 속도에 따른 색상 변경
        if speed > 400:
            self.speed_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #e74c3c;")
        elif speed > 200:
            self.speed_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #f39c12;")
        else:
            self.speed_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")

    def closeEvent(self, event):
        # 창 닫을 때 Altino 종료
        self.text_area.append_message("👋 시스템을 종료합니다...", 'info')
        Close()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # 모던한 스타일 적용
    
    # 전체 앱 폰트 설정
    font = QFont("Segoe UI", 9)
    app.setFont(font)
    
    window = AltinoVoiceSafetyApp()
    window.show()
    sys.exit(app.exec_())