from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QDialog, QDialogButtonBox, QLabel, QVBoxLayout
from DialogBox import DialogBox

class MainWindow(QMainWindow):
    def __init__(self, editor):
        super().__init__()
        self.setWindowTitle("Untitled - Notepad")
        self.setWindowIcon(QIcon('./assets/editor.png'))
        self.text_edit = editor
        self.setCentralWidget(editor)
        self.add_menu_bar()
        self.filters = 'Text Files (*.txt)'
        self.dialog_box = DialogBox()
        self.path = ""
    
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
        #exit_action.triggered.connect(self.dialog_box.quit_dialog)
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
            self.setWindowTitle("Untitled - Notepad")

    def open_document(self):
        filename, _ = QFileDialog.getOpenFileName(self, filter=self.filters)
        if filename:
            self.path = Path(filename) #bug
            self.text_edit.set_text(self.path.read_text())
            self.set_title(filename)
         
    def confirm_save(self):
        return True
        ...
    
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

        self.path = Path(filename) #bug
        self.path.write_text(self.text_edit.toPlainText())
        self.set_title(filename)