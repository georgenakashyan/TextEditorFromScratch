from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtWidgets import QWidget, QApplication
class CustomTextEdit(QWidget):
    def __init__(self):
        super().__init__()
        
        self.text = [""] #TODO: Right now this is an array but we should use a data struct instead
        self.cursor_pos = (0, 0) # (row, col)
        self.cursor_visible = True
        self.true_col = 0
        self.font = QFont('Consolas', 11)
        
        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.blink_cursor)
        self.blink_timer.start(500)  # Blink cursor every 500ms
        
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFont(self.font)
        
        self.unsaved = False

    def keyPressEvent(self, event):
        row, col = self.cursor_pos
        key = event.key()
        
        first_row = row == 0
        first_col = col == 0
        last_row = row == len(self.text) - 1
        last_col = col == len(self.text[row])
        
        if key == Qt.Key_Backspace:
            if (first_col and not first_row):
                prev_row = row-1
                prev_row_len = len(self.text[prev_row])
                curr_row_len = len(self.text[row])
                self.text[prev_row] = self.text[prev_row][:prev_row_len] + self.text[row][:curr_row_len]
                self.text.pop(row)
                self.set_blinker_and_true_col(prev_row, prev_row_len)
            elif (not first_col):
                self.text[row] = self.text[row][:col-1] + self.text[row][col:]
                self.set_blinker_and_true_col(row, col-1)
            self.reset_cursor_blink()
        elif key == Qt.Key_Return or key == Qt.Key_Enter:
            new_row = row + 1
            left_line = self.text[row][:col]
            right_line = self.text[row][col:]
            self.text[row] = left_line
            self.text.insert(new_row, right_line)
            self.set_blinker_and_true_col(new_row, 0)
            self.reset_cursor_blink()
        elif key == Qt.Key_Left:
            if (not first_col):
                self.set_blinker_and_true_col(row, col-1)
                self.reset_cursor_blink()
            elif (not first_row):
                self.set_blinker_and_true_col(row-1, len(self.text[row-1]))
                self.reset_cursor_blink()
        elif key == Qt.Key_Right:
            if (not last_col):
                self.set_blinker_and_true_col(row, col+1)
                self.reset_cursor_blink()
            elif (not last_row):
                self.set_blinker_and_true_col(row+1, 0)
                self.reset_cursor_blink()
        elif key == Qt.Key_Up:
            if (not first_row):
                new_row = row - 1
                new_col_len = len(self.text[new_row])
                new_col = self.true_col if (self.true_col < new_col_len) else new_col_len
                self.cursor_pos = (new_row, new_col)
                self.reset_cursor_blink()
        elif key == Qt.Key_Down:
            if (not last_row):
                new_row = row + 1
                new_col_len = len(self.text[new_row])
                new_col = self.true_col if (self.true_col < new_col_len) else new_col_len
                self.cursor_pos = (new_row, new_col)
                self.reset_cursor_blink()
        else:
            self.text[row] = self.text[row][:col] + event.text() + self.text[row][col:]
            self.set_blinker_and_true_col(row, col+1)
            self.reset_cursor_blink()
        
        self.update()
    
    def undo(self):
        print("Pressed shortcut for undo")
        ...
    
    def redo(self):
        print("Pressed shortcut for redo")
        ...
        
    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setFont(self.font)
        metrics = qp.fontMetrics()
        row_height = metrics.height()
        for row, line in enumerate(self.text):
            qp.drawText(4, ((row+1) * row_height)-4, line)
        
        if self.cursor_visible:
            row, col = self.cursor_pos
            x = metrics.horizontalAdvance(self.text[row][:col]) + 4
            y = row * row_height
            qp.drawLine(x, y, x, y + row_height)
    
    def blink_cursor(self):
        self.cursor_visible = not self.cursor_visible
        self.update()
    
    def reset_cursor_blink(self):
        self.cursor_visible = True
        self.blink_timer.start(500)
    
    def set_blinker_and_true_col(self, row, col):
        self.cursor_pos = (row, col)
        self.true_col = col
        
    def setText(self, file_text):
        self.text = file_text
        self.update()