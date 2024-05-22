import sys
from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow
from CustomTextEdit import CustomTextEdit
from DialogBox import DialogBox

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