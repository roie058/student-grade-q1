import os
import subprocess
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
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

        # Bonus: Live Class Statistics Bar
        stats_frame = QFrame()
        stats_frame.setObjectName("stats_bar")
        stats_layout = QHBoxLayout(stats_frame)
        stats_layout.setContentsMargins(14, 10, 14, 10)
        stats_layout.setSpacing(16)

        self.orig_avg_label = QLabel("Original Avg: --")
        self.corr_avg_label = QLabel("Corrected Avg: --")
        self.pass_rate_label = QLabel("Pass Rate: --")
        self.perfect_label = QLabel("100s: --")

        for lbl in (self.orig_avg_label, self.corr_avg_label, self.pass_rate_label, self.perfect_label):
            lbl.setProperty("class", "stat-label")
            stats_layout.addWidget(lbl)

        main_layout.addWidget(stats_frame)

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

    def update_table(self):
        self.table.clearContents()
        row_count = max(50, len(self.student_ids))
        self.table.setRowCount(row_count)

        for row in range(len(self.student_ids)):
            values = [
                str(self.student_ids[row]),
                str(self.original_grades[row]),
                str(self.corrected_grades[row]) if row < len(self.corrected_grades) else "",
            ]
            for col, text in enumerate(values):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)

        self.update_stats()

    def update_stats(self):
        if len(self.original_grades) == 0 :
            return
        orig_avg = sum(self.original_grades)/len(self.original_grades)
        corr_avg = sum(self.corrected_grades)/len(self.corrected_grades)
        passed_count = 0
        perfect_count = 0
        for i in range(len(self.corrected_grades)):
            if self.corrected_grades[i]>=60:
                passed_count+=1
            if self.corrected_grades[i]==100:
                perfect_count+=1

        pass_rate = passed_count/len(self.corrected_grades)
        self.orig_avg_label.setText(f"Original Avg: {orig_avg:.2f}")
        self.corr_avg_label.setText(f"Corrected Avg: {corr_avg:.2f}")
        self.pass_rate_label.setText(f"Pass Rate: {pass_rate*100:.2f}%")
        self.perfect_label.setText(f"100s: {perfect_count}")


    def open_file_default(self, file_path: str):
        if sys.platform.startswith("win"):
            os.startfile(file_path)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", file_path])
        else:
            subprocess.Popen(["xdg-open", file_path])


    def on_load_file(self, file_path: str):
        #Save file_path and load student IDs & grades
        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        if file_path == '' :
            return

        self.selected_file = file_path
        try:
            with open(self.selected_file, "r") as rows:
                students = rows.readlines()
                
                for i in range(len(students)):
                    if i == 0 :
                        continue
                    student = students[i].strip().split(",")
                    self.student_ids.append(student[0])
                    self.original_grades.append(int(student[1]))
                    self.corrected_grades.append(int(student[1])) 
                self.update_table()
        except Exception as e:
            print(f"Error loading file: {e}")
                

    def on_bonus_entered(self):
        #Update corrected_grades (max 100) and refresh table
        bonus = self.bonus_input.value()
        for i in range(len(self.corrected_grades)):
            self.corrected_grades[i] = self.original_grades[i] + bonus
            if self.corrected_grades[i] > 100:
                self.corrected_grades[i] = 100
            if self.corrected_grades[i] < 0:
                self.corrected_grades[i] = 0
        self.update_table()

    def on_update_file(self):
        if self.selected_file:
            try:
                with open(self.selected_file, "w") as rows:
                    rows.write("ID,Grade\n")
                    for i in range(len(self.student_ids)):
                        rows.write(f"{self.student_ids[i]},{self.corrected_grades[i]}\n")
                self.bonus_input.setValue(0)
                self.on_load_file(self.selected_file)
                self.open_file_default(self.selected_file)

            except Exception as e:
                print(f"Error updating file: {e}")
        


def main():
    app = QApplication(sys.argv)
    window = GradeEditorWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
