from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QFont, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, QFileDialog, QDialog, QDialogButtonBox, QLabel, QVBoxLayout

class DialogBox(QDialog):
    def __init__(self):
        super().__init__()
        ...
        
    def open_dialog(self):
        ...
    
    def quit_dialog(self):
        self.setWindowTitle("Notepad")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.No | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept_save)
        self.buttonBox.rejected.connect(self.reject_save)
        self.buttonBox.rejected.connect(self.cancel_save)

        self.layout = QVBoxLayout()
        message = QLabel("Do you want to save changes to " + str(self.windowTitle()) + "?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        self.exec()
    
    def accept_save(self):
        super.save_document()
        super.destroy()
        
    def reject_save(self):
        super.destroy()
    
    def cancel_save(self):
        self.close()