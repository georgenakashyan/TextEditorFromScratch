from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QFont, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, QFileDialog, QDialog, QDialogButtonBox, QLabel, QVBoxLayout

class DialogBox(QDialogButtonBox):
    def __init__():
        super().__init__()
        ...
    
    def OpenDialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Notepad")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.No | QDialogButtonBox.Cancel

        dlg.buttonBox = QDialogButtonBox(QBtn)
        dlg.buttonBox.accepted.connect(self.accept_save)
        dlg.buttonBox.rejected.connect(self.reject_save)
        dlg.buttonBox.rejected.connect(self.cancel_save)

        dlg.layout = QVBoxLayout()
        message = QLabel("Do you want to save changes to " + str(self.windowTitle()) + "?")
        dlg.layout.addWidget(message)
        dlg.layout.addWidget(dlg.buttonBox)
        dlg.setLayout(dlg.layout)
        dlg.exec()
    
    def accept_save(self):
        self.save_document()
        self.destroy()
        
    def reject_save(self):
        self.destroy()
    
    def cancel_save(self):
        dialog.close()