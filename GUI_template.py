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
        Dialog.resize(1731, 869)
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
        self.Right_Button.setGeometry(QtCore.QRect(780, 720, 93, 28))
        self.Right_Button.setAutoDefault(False)
        self.Right_Button.setFlat(False)
        self.Right_Button.setObjectName("Right_Button")
        self.Left_Button = QtWidgets.QPushButton(Dialog)
        self.Left_Button.setGeometry(QtCore.QRect(630, 720, 93, 28))
        self.Left_Button.setAutoDefault(False)
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
        self.img_text2.setStyleSheet("font-size:14pt;\n"
"margin-top:0px;\n"
"margin-bottom:0px;\n"
"margin-left:0px; \n"
"margin-right:0px; \n"
"-qt-block-indent:0; \n"
"text-indent:0px; \n"
"background-color:#ffffff;\n"
"p{text-align:center;}")
        self.img_text2.setObjectName("img_text2")
        self.img_text1 = QtWidgets.QTextBrowser(Dialog)
        self.img_text1.setEnabled(False)
        self.img_text1.setGeometry(QtCore.QRect(260, 710, 256, 41))
        self.img_text1.setStyleSheet("font-size:14pt;\n"
"margin-top:0px;\n"
"margin-bottom:0px;\n"
"margin-left:0px; \n"
"margin-right:0px; \n"
"-qt-block-indent:0; \n"
"text-indent:0px; \n"
"background-color:#ffffff;\n"
"p{text-align:center;}")
        self.img_text1.setObjectName("img_text1")
        self.SIFT_Button = QtWidgets.QCheckBox(Dialog)
        self.SIFT_Button.setGeometry(QtCore.QRect(1450, 240, 85, 19))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.SIFT_Button.setFont(font)
        self.SIFT_Button.setObjectName("SIFT_Button")
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(1450, 90, 191, 41))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser_2 = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser_2.setGeometry(QtCore.QRect(1450, 190, 191, 41))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.textBrowser_3 = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser_3.setGeometry(QtCore.QRect(1450, 290, 191, 41))
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.Distance_Limit = QtWidgets.QSpinBox(Dialog)
        self.Distance_Limit.setGeometry(QtCore.QRect(1450, 340, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.Distance_Limit.setFont(font)
        self.Distance_Limit.setMaximum(1000)
        self.Distance_Limit.setProperty("value", 100)
        self.Distance_Limit.setObjectName("Distance_Limit")
        self.Limit_Button = QtWidgets.QCheckBox(Dialog)
        self.Limit_Button.setGeometry(QtCore.QRect(1450, 400, 85, 19))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.Limit_Button.setFont(font)
        self.Limit_Button.setObjectName("Limit_Button")
        self.textBrowser_4 = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser_4.setGeometry(QtCore.QRect(1450, 440, 191, 41))
        self.textBrowser_4.setObjectName("textBrowser_4")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(1451, 131, 191, 31))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.BF_Flow_Button = QtWidgets.QCheckBox(self.widget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.BF_Flow_Button.setFont(font)
        self.BF_Flow_Button.setObjectName("BF_Flow_Button")
        self.horizontalLayout.addWidget(self.BF_Flow_Button)
        self.BF_Line_Button = QtWidgets.QCheckBox(self.widget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.BF_Line_Button.setFont(font)
        self.BF_Line_Button.setObjectName("BF_Line_Button")
        self.horizontalLayout.addWidget(self.BF_Line_Button)
        self.widget1 = QtWidgets.QWidget(Dialog)
        self.widget1.setGeometry(QtCore.QRect(1440, 490, 212, 48))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.Ratio_Test = QtWidgets.QSlider(self.widget1)
        self.Ratio_Test.setMaximum(10)
        self.Ratio_Test.setProperty("value", 10)
        self.Ratio_Test.setOrientation(QtCore.Qt.Horizontal)
        self.Ratio_Test.setObjectName("Ratio_Test")
        self.verticalLayout.addWidget(self.Ratio_Test)
        self.label = QtWidgets.QLabel(self.widget1)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.Ratio_Test_Display = QtWidgets.QLCDNumber(self.widget1)
        font = QtGui.QFont()
        font.setFamily("AR CENA")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.Ratio_Test_Display.setFont(font)
        self.Ratio_Test_Display.setAcceptDrops(False)
        self.Ratio_Test_Display.setToolTipDuration(2)
        self.Ratio_Test_Display.setAutoFillBackground(False)
        self.Ratio_Test_Display.setStyleSheet("background-color:black;\n"
"color:rgb(0, 255, 0);\n"
"\n"
"")
        self.Ratio_Test_Display.setSmallDecimalPoint(True)
        self.Ratio_Test_Display.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.Ratio_Test_Display.setProperty("value", 1.0)
        self.Ratio_Test_Display.setObjectName("Ratio_Test_Display")
        self.horizontalLayout_2.addWidget(self.Ratio_Test_Display)
        self.widget.raise_()
        self.img_label1.raise_()
        self.Right_Button.raise_()
        self.Left_Button.raise_()
        self.img_label2.raise_()
        self.img_text2.raise_()
        self.img_text1.raise_()
        self.SIFT_Button.raise_()
        self.BF_Flow_Button.raise_()
        self.BF_Line_Button.raise_()
        self.textBrowser.raise_()
        self.textBrowser_2.raise_()
        self.textBrowser_3.raise_()
        self.Distance_Limit.raise_()
        self.Limit_Button.raise_()
        self.Ratio_Test.raise_()
        self.textBrowser_4.raise_()
        self.label.raise_()
        self.Ratio_Test_Display.raise_()

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
"</style></head><body style=\" font-family:\'PMingLiU\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#ffffff;\"><span style=\" background-color:#ffffff;\">out_1.jpg</span></p></body></html>"))
        self.img_text1.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'PMingLiU\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#ffffff;\"><span style=\" background-color:#ffffff;\">out_0.jpg</span></p></body></html>"))
        self.SIFT_Button.setText(_translate("Dialog", "SIFT"))
        self.textBrowser.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'PMingLiU\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Brute force match</span></p></body></html>"))
        self.textBrowser_2.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'PMingLiU\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Show key points</span></p></body></html>"))
        self.textBrowser_3.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'PMingLiU\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Distance Limit</span></p></body></html>"))
        self.Limit_Button.setText(_translate("Dialog", "Limit"))
        self.textBrowser_4.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'PMingLiU\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Ratio test</span></p></body></html>"))
        self.BF_Flow_Button.setText(_translate("Dialog", "flow field"))
        self.BF_Line_Button.setText(_translate("Dialog", "line"))
        self.label.setText(_translate("Dialog", "0                                 1"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

