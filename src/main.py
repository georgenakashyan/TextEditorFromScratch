import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QFont, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction

class CustomTextEdit(QWidget):
    def __init__(self):
        super().__init__()
        
        self.text = [] #TODO: Right now this is an array but we should use a data struct instead
        self.cursor_pos = (0, 0) # (row, col)
        self.cursor_visible = True
        self.true_col = 0
        self.font = QFont('Consolas', 11)
        
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
            qp.drawText(0, (row+1) * row_height, line)
        
        if self.cursor_visible:
            row, col = self.cursor_pos
            x = metrics.horizontalAdvance(self.text[row][:col])
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
class MainWindow(QMainWindow):
    def __init__(self, editor):
        super().__init__()
        self.setWindowTitle("Untitled - Notepad")
        self.setWindowIcon(QIcon('./assets/editor.png'))
        self.text_edit = editor
        self.setCentralWidget(editor)
        self.add_menu_bar()
        self.filters = 'Text Files (*.txt)'
    
    def add_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        edit_menu = menu_bar.addMenu('&Edit')
        help_menu = menu_bar.addMenu('&Help')
        
        # new menu item
        new_action = QAction('&New', self)
        new_action.setStatusTip('Create a new document')
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_document)
        file_menu.addAction(new_action)

        # open menu item
        open_action = QAction('&Open...', self)
        open_action.triggered.connect(self.open_document)
        open_action.setStatusTip('Open a document')
        open_action.setShortcut('Ctrl+O')
        file_menu.addAction(open_action)

        # save menu item
        save_action = QAction('&Save', self)
        save_action.setStatusTip('Save the document')
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_document)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()

        # exit menu item
        exit_action = QAction('&Exit', self)
        exit_action.setStatusTip('Exit')
        exit_action.setShortcut('Alt+F4')
        exit_action.triggered.connect(self.quit)
        file_menu.addAction(exit_action)

        # edit menu
        undo_action = QAction('&Undo', self)
        undo_action.setStatusTip('Undo')
        undo_action.setShortcut('Ctrl+Z')
        undo_action.triggered.connect(self.text_edit.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction('&Redo', self)
        redo_action.setStatusTip('Redo')
        redo_action.setShortcut('Ctrl+Y')
        redo_action.triggered.connect(self.text_edit.redo)
        edit_menu.addAction(redo_action)

        about_action = QAction('About', self)
        help_menu.addAction(about_action)
        about_action.setStatusTip('About')
        about_action.setShortcut('F1')
        
    def new_document(self):
        if (self.confirm_save()):
            self.text_edit.clear()
            self.set_title()

    def save_document(self):
        # save the currently openned file
        if (self.path):
            return self.path.write_text(self.text_edit.toPlainText())

        # save a new file
        filename, _ = QFileDialog.getSaveFileName(
            self, 'Save File', filter=self.filters
        )

        if not filename:
            return

        self.path = Path(filename)
        self.path.write_text(self.text_edit.toPlainText())
        self.set_title(filename)

    def open_document(self):
        filename, _ = QFileDialog.getOpenFileName(self, filter=self.filters)
        if filename:
            self.path = Path(filename)
            self.text_edit.setText(self.path.read_text())
            self.set_title(filename)

    def quit(self):
        if self.confirm_save():
            self.destroy()

def main():
    app = QApplication(sys.argv)
    editor = CustomTextEdit()
    editor.text = [""]  # Start with an empty line
    window = MainWindow(editor)
    window.resize(800, 600)
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()