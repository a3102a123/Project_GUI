# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_subwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1339, 867)
        self.Image_Label = QtWidgets.QLabel(Dialog)
        self.Image_Label.setGeometry(QtCore.QRect(70, 110, 1200, 600))
        self.Image_Label.setStyleSheet("background-color:white;\n"
"")
        self.Image_Label.setText("")
        self.Image_Label.setObjectName("Image_Label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

