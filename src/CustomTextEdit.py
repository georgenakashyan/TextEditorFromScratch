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
        key = event.key()
        key_text = event.text()
        modifiers = QApplication.keyboardModifiers()
        
        if modifiers == Qt.ShiftModifier:
            print('Shift')
        if modifiers == Qt.ControlModifier:
            print('Control')
        if modifiers == Qt.AltModifier:
            print('Alt')
        
        key_actions = {
            Qt.Key_Backspace: self.handle_backspace,
            Qt.Key_Return: self.handle_return,
            Qt.Key_Enter: self.handle_return,
            Qt.Key_Left: self.handle_left,
            Qt.Key_Right: self.handle_right,
            Qt.Key_Up: self.handle_up,
            Qt.Key_Down: self.handle_down
        }
        
        action = key_actions.get(key)
        
        if action:
            action(key_text)
            self.set_unsaved_title()
        else:
            self.handle_insert(key_text)
            self.set_unsaved_title()

    def handle_insert(self, key_text):
        row, col = self.cursor_pos
        self.text[row] = self.text[row][:col] + key_text + self.text[row][col:]
        self.set_blinker_and_true_col(row, col+1)
        self.reset_cursor_blink()
    
    def handle_backspace(self, key_text):
        row, col = self.cursor_pos
        first_row = row == 0
        first_col = col == 0
        
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

    def handle_return(self, key_text):
        row, col = self.cursor_pos
        new_row = row + 1
        left_line = self.text[row][:col]
        right_line = self.text[row][col:]
        
        self.text[row] = left_line
        self.text.insert(new_row, right_line)
        self.set_blinker_and_true_col(new_row, 0)
        self.reset_cursor_blink()
        
    def handle_left(self, key_text):
        row, col = self.cursor_pos
        first_row = row == 0
        first_col = col == 0
        
        if (not first_col):
            self.set_blinker_and_true_col(row, col-1)
            self.reset_cursor_blink()
        elif (not first_row):
            self.set_blinker_and_true_col(row-1, len(self.text[row-1]))
            self.reset_cursor_blink()
    
    def handle_right(self, key_text):
        row, col = self.cursor_pos
        last_row = row == len(self.text) - 1
        last_col = col == len(self.text[row])
        
        if (not last_col):
            self.set_blinker_and_true_col(row, col+1)
            self.reset_cursor_blink()
        elif (not last_row):
            self.set_blinker_and_true_col(row+1, 0)
            self.reset_cursor_blink()

    def handle_up(self, key_text):
        row, col = self.cursor_pos
        first_row = row == 0
        
        if (not first_row):
            new_row = row - 1
            new_col_len = len(self.text[new_row])
            new_col = self.true_col if (self.true_col < new_col_len) else new_col_len
            self.cursor_pos = (new_row, new_col)
            self.reset_cursor_blink()

    def handle_down(self, key_text):
        row, col = self.cursor_pos
        last_row = row == len(self.text) - 1
        
        if (not last_row):
            new_row = row + 1
            new_col_len = len(self.text[new_row])
            new_col = self.true_col if (self.true_col < new_col_len) else new_col_len
            self.cursor_pos = (new_row, new_col)
            self.reset_cursor_blink()
    
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
        self.update()
    
    def set_blinker_and_true_col(self, row, col):
        self.cursor_pos = (row, col)
        self.true_col = col
        
    def set_text(self, file_text):
        self.text = file_text
        self.update()