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
        self.true_col = 0
        self.font = QFont('Courier', 12)
        
        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.blink_cursor)
        self.blink_timer.start(500)  # Blink cursor every 500ms
        
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFont(self.font)

    def keyPressEvent(self, event):
        row, col = self.cursor_pos
        key = event.key()
        
        first_row = row == 0
        first_col = col == 0
        last_row = row == len(self.text) - 1
        last_col = col == len(self.text[row])
        
        if key == Qt.Key_Backspace:
            self.text[row] = self.text[row][:col-1] + self.text[row][col:]
            self.cursor_pos = (row, col-1)
            self.cursor_visible = True
        elif key == Qt.Key_Return or key == Qt.Key_Enter:
            new_row = row + 1
            self.text.insert(new_row, "")
            self.cursor_pos = (new_row, 0)
            self.true_col = 0
            self.cursor_visible = True
        elif key == Qt.Key_Left:
            if (not first_col):
                self.cursor_pos = (row, col-1)
                self.true_col = col-1
                self.cursor_visible = True
            elif (not first_row):
                self.cursor_pos = (row-1, len(self.text[row-1]))
                self.true_col = len(self.text[row-1])
                self.cursor_visible = True
        elif key == Qt.Key_Right:
            if (not last_col):
                self.cursor_pos = (row, col+1)
                self.true_col = col+1
                self.cursor_visible = True
            elif (not last_row):
                self.cursor_pos = (row+1, len(self.text[row+1]))
                self.true_col = len(self.text[row+1])
                self.cursor_visible = True
        elif key == Qt.Key_Up:
            if (not first_row):
                new_row = row - 1
                new_col_len = len(self.text[new_row])
                new_col = self.true_col if (self.true_col < new_col_len) else new_col_len
                self.cursor_pos = (new_row, new_col)
                self.cursor_visible = True
        elif key == Qt.Key_Down:
            if (not last_row):
                new_row = row + 1
                new_col_len = len(self.text[new_row])
                new_col = self.true_col if (self.true_col < new_col_len) else new_col_len
                self.cursor_pos = (new_row, new_col)
                self.cursor_visible = True
        else:
            self.text[row] = self.text[row][:col] + event.text() + self.text[row][col:]
            self.cursor_pos = (row, col+1)
            self.true_col = col+1
        
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