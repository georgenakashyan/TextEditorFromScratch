import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtWidgets import QApplication, QWidget

class CustomTextEdit(QWidget):
    def __init__(self):
        super().__init__()
        self.text = [] # Right now this is an array but we should use a data struct instead
        self.cursor_pos = (0, 0) # (row, col)
        self.cursor_visible = True
        self.font = QFont('Courier', 12)


def main():
    app = QApplication(sys.argv)
    editor = CustomTextEdit()
    editor.text = [""]  # Start with an empty line
    editor.resize(800, 600)
    editor.show()
    app.exec_()

if __name__ == '__main__':
    main()