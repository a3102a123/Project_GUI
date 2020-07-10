# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_template.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1511, 869)
        self.img_label1 = QtWidgets.QLabel(Dialog)
        self.img_label1.setGeometry(QtCore.QRect(70, 20, 681, 681))
        self.img_label1.setText("")
        self.img_label1.setPixmap(QtGui.QPixmap("im0/out_0.jpg"))
        self.img_label1.setScaledContents(True)
        self.img_label1.setAlignment(QtCore.Qt.AlignCenter)
        self.img_label1.setWordWrap(False)
        self.img_label1.setOpenExternalLinks(False)
        self.img_label1.setObjectName("img_label1")
        self.Right_Button = QtWidgets.QPushButton(Dialog)
        self.Right_Button.setGeometry(QtCore.QRect(830, 720, 93, 28))
        self.Right_Button.setObjectName("Right_Button")
        self.Left_Button = QtWidgets.QPushButton(Dialog)
        self.Left_Button.setGeometry(QtCore.QRect(680, 720, 93, 28))
        self.Left_Button.setObjectName("Left_Button")
        self.img_label2 = QtWidgets.QLabel(Dialog)
        self.img_label2.setGeometry(QtCore.QRect(750, 20, 681, 681))
        self.img_label2.setText("")
        self.img_label2.setPixmap(QtGui.QPixmap("im0/out_1.jpg"))
        self.img_label2.setScaledContents(True)
        self.img_label2.setAlignment(QtCore.Qt.AlignCenter)
        self.img_label2.setWordWrap(False)
        self.img_label2.setOpenExternalLinks(False)
        self.img_label2.setObjectName("img_label2")
        self.img_text2 = QtWidgets.QTextBrowser(Dialog)
        self.img_text2.setEnabled(False)
        self.img_text2.setGeometry(QtCore.QRect(990, 710, 256, 41))
        self.img_text2.setObjectName("img_text2")
        self.img_text1 = QtWidgets.QTextBrowser(Dialog)
        self.img_text1.setEnabled(False)
        self.img_text1.setGeometry(QtCore.QRect(260, 710, 256, 41))
        self.img_text1.setObjectName("img_text1")
        self.SIFT_Button = QtWidgets.QCheckBox(Dialog)
        self.SIFT_Button.setGeometry(QtCore.QRect(680, 770, 85, 19))
        self.SIFT_Button.setObjectName("SIFT_Button")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.Right_Button.setText(_translate("Dialog", ">"))
        self.Left_Button.setText(_translate("Dialog", "<"))
        self.img_text2.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'PMingLiU\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#ffffff;\"><span style=\" font-size:14pt;\">out_1.jpg</span></p></body></html>"))
        self.img_text1.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'PMingLiU\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#ffffff;\"><span style=\" font-size:14pt;\">out_0.jpg</span></p></body></html>"))
        self.SIFT_Button.setText(_translate("Dialog", "SIFT"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

