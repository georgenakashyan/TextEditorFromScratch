import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtWidgets import QApplication, QWidget

class CustomTextEdit(QWidget):
    def __init__(self):
        super().__init__()
        self.text = [] #TODO: Right now this is an array but we should use a data struct instead
        self.cursor_pos = (0, 0) # (row, col)
        self.cursor_visible = True
        self.font = QFont('Courier', 12)
        
        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.blink_cursor)
        self.blink_timer.start(500)  # Blink cursor every 500ms
        
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFont(self.font)

    def keyPressEvent(self, event):
        row, col = self.cursor_pos
        key = event.key()
        not_first_row = row > 0
        not_last_row = row < len(self.text) - 1
        
        if key == Qt.Key_Backspace:
            ...
        elif key == Qt.Key_Return or key == Qt.Key_Enter:
            ...
        elif key == Qt.Key_Left:
            ...
        elif key == Qt.Key_Right:
            ...
        elif key == Qt.Key_Up and not_first_row:
            ...
        elif key == Qt.Key_Down and not_last_row:
            ...
        else:
            self.text[row] = self.text[row][:col] + event.text() + self.text[row][col:]
            self.cursor_pos = (row, col+1)
        
        self.update()
        
    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setFont(self.font)
        metrics = qp.fontMetrics()
        row_height = metrics.height()
        for row, line in enumerate(self.text):
            qp.drawText(0, (row+1) * row_height, line)
        
        if self.cursor_visible:
            row, col = self.cursor_pos
            x = metrics.horizontalAdvance(self.text[row][:col])
            y = row * row_height
            qp.drawLine(x, y, x, y + row_height)
    
    def blink_cursor(self):
        self.cursor_visible = not self.cursor_visible
        self.update()

def main():
    app = QApplication(sys.argv)
    editor = CustomTextEdit()
    editor.text = [""]  # Start with an empty line
    editor.resize(800, 600)
    editor.show()
    app.exec_()

if __name__ == '__main__':
    main()