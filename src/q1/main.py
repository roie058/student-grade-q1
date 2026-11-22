import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QVBoxLayout,
    QWidget,
)

try:
    from About import AboutWindow
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
    from About import AboutWindow


class GradeEditorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("GradeEditorWindow")
        self.setWindowTitle("Student Grade Editor")
        self.resize(700, 560)

        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ''

        self.about_window = None
        self.init_ui()
        self.load_stylesheet()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(14)

        # Top bar: Load File + About
        top_layout = QHBoxLayout()
        self.load_btn = QPushButton("Load Grades File")
        self.load_btn.setObjectName("load_btn")
        self.load_btn.clicked.connect(self.choose_file)

        self.about_btn = QPushButton("About")
        self.about_btn.setObjectName("about_btn")
        self.about_btn.clicked.connect(self.open_about)

        top_layout.addWidget(self.load_btn)
        top_layout.addStretch()
        top_layout.addWidget(self.about_btn)
        main_layout.addLayout(top_layout)

        # Table: 50 rows x 3 columns
        self.table = QTableWidget(50, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Original Grades", "Corrected Grades"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        main_layout.addWidget(self.table)

        # Bottom bar: Bonus input (ENTER) + Update File button
        bottom_layout = QHBoxLayout()

        bonus_label = QLabel("Bonus Points (Press ENTER):")
        self.bonus_input = QSpinBox()
        self.bonus_input.setObjectName("bonus_input")
        self.bonus_input.setRange(-100, 100)
        self.bonus_input.setValue(0)
        self.bonus_input.lineEdit().returnPressed.connect(self.on_bonus_entered)

        self.update_btn = QPushButton("Update File")
        self.update_btn.setObjectName("update_btn")
        self.update_btn.clicked.connect(self.on_update_file)

        bottom_layout.addWidget(bonus_label)
        bottom_layout.addWidget(self.bonus_input)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.update_btn)
        main_layout.addLayout(bottom_layout)

    def load_stylesheet(self):
        qss_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles.qss")
        if os.path.exists(qss_path):
            with open(qss_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())

    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Grades CSV File",
            "",
            "CSV Files (*.csv);;All Files (*)",
        )
        if file_path:
            self.on_load_file(file_path)

    def open_about(self):
        if self.about_window is None:
            self.about_window = AboutWindow()
        self.about_window.show()
        self.about_window.raise_()

    # --- Placeholders for your logic---

    def on_load_file(self, file_path: str):
        #Save file_path and load student IDs & grades
        pass

    def on_bonus_entered(self):
        #Update corrected_grades (max 100) and refresh table
        pass

    def on_update_file(self):
        #Overwrite CSV with corrected grades and open it
        pass


def main():
    app = QApplication(sys.argv)
    window = GradeEditorWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
