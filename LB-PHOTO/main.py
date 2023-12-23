from PyQt5 import QtWidgets
from prog import Ui_MainWindow
from PyQt5.QtGui import QPixmap
import sys
import funk

class mywindow(QtWidgets.QMainWindow):
    def __init__(self, picture_path = None):
        self.picture_path = picture_path
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.browse_folder)
        self.ui.pushButton_3.clicked.connect(self.encrypt)
        self.ui.pushButton_4.clicked.connect(self.decrypt)

        self.ui.textEdit.setEnabled(False)
        self.ui.pushButton_3.setEnabled(False)
        self.ui.pushButton_4.setEnabled(False)

    def browse_folder(self):
        self.ui.textEdit.clear()
        self.ui.label.clear()
        self.ui.label_2.clear()

        self.ui.textEdit.setEnabled(True)
        self.ui.pushButton_3.setEnabled(True)
        self.ui.pushButton_4.setEnabled(True)

        self.picture_path = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл")
        pixmap = QPixmap(self.picture_path[0])
        pixmap = pixmap.scaled(200, 200, aspectRatioMode= 1)
        self.ui.label.setPixmap(pixmap)

    def encrypt(self):
        self.ui.pushButton_4.setEnabled(False)
        self.save, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Выберете куда сохранить файл", '.', 'Изображение (*.png)')

        self.im = funk.cod(self.picture_path[0], self.ui.textEdit.toPlainText(), self.save)

        pixmap = QPixmap(self.im)
        pixmap = pixmap.scaled(200, 200, aspectRatioMode= 1)
        self.ui.label_2.setPixmap(pixmap)

    def decrypt(self):
        self.ui.pushButton_3.setEnabled(False)
        self.txt = funk.decod(self.picture_path[0])
        self.ui.textEdit.setPlainText(self.txt)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()