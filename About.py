
import os
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame
from PySide6.QtGui import QPixmap, QFont, QPainter, QPainterPath, QColor, QPen, QDesktopServices
from PySide6.QtCore import Qt, QUrl


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("AboutWindow")
        self.setWindowTitle("About Me")
        self.setFixedSize(370, 520)
        self.init_ui()

    def get_circular_avatar(self, image_path: str, size: int = 140) -> QPixmap:
        src = QPixmap(image_path).scaled(
            size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )

        x_offset = max(0, (src.width() - size) // 2)
        y_offset = max(0, (src.height() - size) // 2)
        cropped = src.copy(x_offset, y_offset, size, size)

        out = QPixmap(size, size)
        out.fill(Qt.transparent)

        painter = QPainter(out)
        painter.setRenderHint(QPainter.Antialiasing)


        path = QPainterPath()
        path.addEllipse(3, 3, size - 6, size - 6)
        painter.setClipPath(path)
        painter.drawPixmap(3, 3, cropped)


        painter.setClipping(False)
        painter.setPen(QPen(QColor(255, 255, 255, 240), 3))
        painter.drawEllipse(3, 3, size - 6, size - 6)

        painter.setPen(QPen(QColor("#cbd5e1"), 1.5))
        painter.drawEllipse(1, 1, size - 2, size - 2)

        painter.end()
        return out

    def init_ui(self):
        self.setStyleSheet("""
            QWidget#AboutWindow {
                background-color: #f8fafc;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            }
            QFrame#card {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 18px;
            }
            QLabel {
                background: transparent;
                border: none;
            }
            QPushButton.social-btn {
                border-radius: 10px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton#linkedin_btn {
                color: #0a66c2;
                border: 1px solid #bae6fd;
                background-color: #f0f9ff;
            }
            QPushButton#linkedin_btn:hover {
                background-color: #e0f2fe;
                border-color: #0284c7;
            }
            QPushButton#github_btn {
                color: #1e293b;
                border: 1px solid #e2e8f0;
                background-color: #f8fafc;
            }
            QPushButton#github_btn:hover {
                background-color: #f1f5f9;
                border-color: #94a3b8;
            }
            QPushButton#close_btn {
                background-color: #ffffff;
                color: #475569;
                border: 1px solid #cbd5e1;
                border-radius: 10px;
                padding: 9px 20px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton#close_btn:hover {
                background-color: #f1f5f9;
                color: #0f172a;
                border-color: #94a3b8;
            }
            QPushButton#close_btn:pressed {
                background-color: #e2e8f0;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 20, 18, 18)
        main_layout.setSpacing(12)


        card = QFrame(self)
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 22, 20, 20)
        card_layout.setSpacing(8)
        card_layout.setAlignment(Qt.AlignCenter)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "profile.png")
        if os.path.exists(image_path):
            avatar = self.get_circular_avatar(image_path, size=132)
            self.image_label.setPixmap(avatar)
        else:
            self.image_label.setText("[No Profile Image]")

        card_layout.addWidget(self.image_label)
        card_layout.addSpacing(4)

 
        self.name_label = QLabel("רועי לבוביץ | Roie", self)
        name_font = QFont()
        name_font.setPointSize(17)
        name_font.setBold(True)
        self.name_label.setFont(name_font)
        self.name_label.setStyleSheet("color: #0f172a; font-weight: 800;")
        self.name_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.name_label)


        self.field_label = QLabel("Mechanical Engineering Student", self)
        self.field_label.setStyleSheet("color: #0284c7; font-size: 13px; font-weight: 600;")
        self.field_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.field_label)


        self.college_label = QLabel("Afeka College of Engineering", self)
        self.college_label.setStyleSheet("color: #64748b; font-size: 12px; font-weight: 500;")
        self.college_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.college_label)

        card_layout.addSpacing(6)


        self.email_label = QLabel(
            '<a href="mailto:roie058@gmail.com" style="color: #475569; text-decoration: none; font-size: 13px; font-weight: 500;">✉ roie058@gmail.com</a>',
            self
        )
        self.email_label.setAlignment(Qt.AlignCenter)
        self.email_label.setOpenExternalLinks(True)
        card_layout.addWidget(self.email_label)

        card_layout.addSpacing(6)


        social_layout = QHBoxLayout()
        social_layout.setSpacing(10)
        social_layout.setAlignment(Qt.AlignCenter)

        self.linkedin_btn = QPushButton("in LinkedIn", self)
        self.linkedin_btn.setObjectName("linkedin_btn")
        self.linkedin_btn.setProperty("class", "social-btn")
        self.linkedin_btn.setCursor(Qt.PointingHandCursor)
        self.linkedin_btn.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://www.linkedin.com/in/roie-lebovich/"))
        )
        social_layout.addWidget(self.linkedin_btn)

        self.github_btn = QPushButton("GitHub", self)
        self.github_btn.setObjectName("github_btn")
        self.github_btn.setProperty("class", "social-btn")
        self.github_btn.setCursor(Qt.PointingHandCursor)
        self.github_btn.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://github.com/roie058"))
        )
        social_layout.addWidget(self.github_btn)

        card_layout.addLayout(social_layout)

        card_layout.addSpacing(10)


        divider = QFrame(self)
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Plain)
        divider.setStyleSheet("background-color: #f1f5f9; border: none; max-height: 1px;")
        card_layout.addWidget(divider)


        course_meta = QLabel("OOP in Python • PySide6 • Dr. Tal Alon", self)
        course_meta.setStyleSheet("color: #94a3b8; font-size: 11px;")
        course_meta.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(course_meta)

        main_layout.addWidget(card)


        self.close_btn = QPushButton("Close", self)
        self.close_btn.setObjectName("close_btn")
        self.close_btn.setCursor(Qt.PointingHandCursor)
        self.close_btn.clicked.connect(self.close)
        main_layout.addWidget(self.close_btn)


if __name__ == "__main__":
    app = QApplication()
    window = AboutWindow()
    window.show()
    app.exec()
