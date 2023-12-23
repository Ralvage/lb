from PyQt5 import QtWidgets
from qt import Ui_MainWindow
import sys
import noekeon

class mywindow(QtWidgets.QMainWindow):
    def __init__(self, picture_path = None):
        self.picture_path = picture_path
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.browse_folder)
        self.ui.pushButton_2.clicked.connect(self.encrypt)
        self.ui.pushButton_3.clicked.connect(self.decrypt)

    def browse_folder(self):
        self.ui.lineEdit.clear()
        self.ui.label_2.clear()
        self.ui.label_3.clear()
        self.ui.pushButton_2.setEnabled(True)
        self.ui.pushButton_3.setEnabled(True)

        self.file = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл")
        self.ui.lineEdit.setText(self.file[0])

    def encrypt(self):
        self.ui.pushButton_3.setEnabled(False)

        if noekeon.enc(self.file[0]) == True:
            self.ui.label_2.setText("Готово")

    def decrypt(self):
        self.ui.pushButton_2.setEnabled(False)

        if noekeon.dec(self.file[0]) == True:
            self.ui.label_3.setText("Готово")

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()