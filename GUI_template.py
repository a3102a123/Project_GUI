# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_template.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from Class.image import MyLabel

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1853, 837)
        self.img_label1 = MyLabel(Dialog)
        self.img_label1.setGeometry(QtCore.QRect(390, 80, 600, 600))
        self.img_label1.setText("")
        self.img_label1.setPixmap(QtGui.QPixmap("im0/out_0.jpg"))
        self.img_label1.setScaledContents(True)
        self.img_label1.setAlignment(QtCore.Qt.AlignCenter)
        self.img_label1.setWordWrap(False)
        self.img_label1.setOpenExternalLinks(False)
        self.img_label1.setObjectName("img_label1")
        self.Right_Button = QtWidgets.QPushButton(Dialog)
        self.Right_Button.setGeometry(QtCore.QRect(1060, 720, 93, 28))
        self.Right_Button.setAutoDefault(False)
        self.Right_Button.setFlat(False)
        self.Right_Button.setObjectName("Right_Button")
        self.Left_Button = QtWidgets.QPushButton(Dialog)
        self.Left_Button.setGeometry(QtCore.QRect(910, 720, 93, 28))
        self.Left_Button.setAutoDefault(False)
        self.Left_Button.setObjectName("Left_Button")
        self.img_label2 = QtWidgets.QLabel(Dialog)
        self.img_label2.setGeometry(QtCore.QRect(990, 80, 600, 600))
        self.img_label2.setText("")
        self.img_label2.setPixmap(QtGui.QPixmap("im0/out_1.jpg"))
        self.img_label2.setScaledContents(True)
        self.img_label2.setAlignment(QtCore.Qt.AlignCenter)
        self.img_label2.setWordWrap(False)
        self.img_label2.setOpenExternalLinks(False)
        self.img_label2.setObjectName("img_label2")
        self.img_text2 = QtWidgets.QTextBrowser(Dialog)
        self.img_text2.setEnabled(False)
        self.img_text2.setGeometry(QtCore.QRect(1270, 710, 256, 41))
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
        self.img_text1.setGeometry(QtCore.QRect(540, 710, 256, 41))
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
        self.SIFT_Button.setGeometry(QtCore.QRect(1610, 290, 85, 19))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.SIFT_Button.setFont(font)
        self.SIFT_Button.setObjectName("SIFT_Button")
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(1610, 140, 191, 41))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser_2 = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser_2.setGeometry(QtCore.QRect(1610, 240, 191, 41))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.textBrowser_3 = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser_3.setGeometry(QtCore.QRect(1610, 340, 191, 41))
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.Distance_Limit = QtWidgets.QSpinBox(Dialog)
        self.Distance_Limit.setGeometry(QtCore.QRect(1610, 390, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.Distance_Limit.setFont(font)
        self.Distance_Limit.setMaximum(1000)
        self.Distance_Limit.setProperty("value", 100)
        self.Distance_Limit.setObjectName("Distance_Limit")
        self.Limit_Button = QtWidgets.QCheckBox(Dialog)
        self.Limit_Button.setGeometry(QtCore.QRect(1610, 450, 85, 19))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.Limit_Button.setFont(font)
        self.Limit_Button.setObjectName("Limit_Button")
        self.textBrowser_4 = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser_4.setGeometry(QtCore.QRect(1610, 490, 191, 41))
        self.textBrowser_4.setObjectName("textBrowser_4")
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(1611, 181, 191, 31))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.BF_Flow_Button = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.BF_Flow_Button.setFont(font)
        self.BF_Flow_Button.setObjectName("BF_Flow_Button")
        self.horizontalLayout.addWidget(self.BF_Flow_Button)
        self.BF_Line_Button = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.BF_Line_Button.setFont(font)
        self.BF_Line_Button.setObjectName("BF_Line_Button")
        self.horizontalLayout.addWidget(self.BF_Line_Button)
        self.layoutWidget1 = QtWidgets.QWidget(Dialog)
        self.layoutWidget1.setGeometry(QtCore.QRect(1600, 540, 212, 48))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.Ratio_Test = QtWidgets.QSlider(self.layoutWidget1)
        self.Ratio_Test.setMaximum(10)
        self.Ratio_Test.setProperty("value", 10)
        self.Ratio_Test.setOrientation(QtCore.Qt.Horizontal)
        self.Ratio_Test.setObjectName("Ratio_Test")
        self.verticalLayout.addWidget(self.Ratio_Test)
        self.label = QtWidgets.QLabel(self.layoutWidget1)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.Ratio_Test_Display = QtWidgets.QLCDNumber(self.layoutWidget1)
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
        self.target_label = QtWidgets.QLabel(Dialog)
        self.target_label.setGeometry(QtCore.QRect(50, 90, 300, 300))
        self.target_label.setStyleSheet("background-color:white;")
        self.target_label.setText("")
        self.target_label.setScaledContents(True)
        self.target_label.setAlignment(QtCore.Qt.AlignCenter)
        self.target_label.setObjectName("target_label")
        self.Target_Button = QtWidgets.QPushButton(Dialog)
        self.Target_Button.setGeometry(QtCore.QRect(50, 410, 111, 28))
        self.Target_Button.setObjectName("Target_Button")
        self.Target_BF_Button = QtWidgets.QPushButton(Dialog)
        self.Target_BF_Button.setGeometry(QtCore.QRect(50, 450, 111, 28))
        self.Target_BF_Button.setObjectName("Target_BF_Button")
        self.Target_Hungarian_Button = QtWidgets.QPushButton(Dialog)
        self.Target_Hungarian_Button.setGeometry(QtCore.QRect(50, 490, 111, 28))
        self.Target_Hungarian_Button.setObjectName("Target_Hungarian_Button")
        self.textBrowser_5 = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser_5.setGeometry(QtCore.QRect(1610, 610, 191, 41))
        self.textBrowser_5.setObjectName("textBrowser_5")
        self.Optical_Flow_Button = QtWidgets.QCheckBox(Dialog)
        self.Optical_Flow_Button.setGeometry(QtCore.QRect(1610, 660, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.Optical_Flow_Button.setFont(font)
        self.Optical_Flow_Button.setObjectName("Optical_Flow_Button")
        self.Result_Data_Text = QtWidgets.QTextBrowser(Dialog)
        self.Result_Data_Text.setEnabled(False)
        self.Result_Data_Text.setGeometry(QtCore.QRect(10, 570, 351, 31))
        self.Result_Data_Text.setStyleSheet("font-size:14pt;\n"
"margin-top:0px;\n"
"margin-bottom:0px;\n"
"margin-left:0px; \n"
"margin-right:0px; \n"
"-qt-block-indent:0; \n"
"text-indent:0px; \n"
"background-color:#ffffff;\n"
"p{text-align:center;}")
        self.Result_Data_Text.setObjectName("Result_Data_Text")
        self.Result_Data = QtWidgets.QComboBox(Dialog)
        self.Result_Data.setGeometry(QtCore.QRect(70, 610, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.Result_Data.setFont(font)
        self.Result_Data.setObjectName("Result_Data")
        self.Result_Data.addItem("")
        self.Result_Data.addItem("")
        self.Result_Data.addItem("")
        self.Result_Data.addItem("")
        self.Result_Data.addItem("")
        self.Dispaly_Button = QtWidgets.QPushButton(Dialog)
        self.Dispaly_Button.setGeometry(QtCore.QRect(220, 610, 81, 31))
        self.Dispaly_Button.setObjectName("Dispaly_Button")
        self.FileName = QtWidgets.QTextEdit(Dialog)
        self.FileName.setGeometry(QtCore.QRect(20, 530, 199, 31))
        self.FileName.setObjectName("FileName")
        self.SaveFileButton = QtWidgets.QPushButton(Dialog)
        self.SaveFileButton.setGeometry(QtCore.QRect(240, 530, 93, 28))
        self.SaveFileButton.setObjectName("SaveFileButton")
        self.Result_Right_Button = QtWidgets.QPushButton(Dialog)
        self.Result_Right_Button.setGeometry(QtCore.QRect(180, 660, 93, 28))
        self.Result_Right_Button.setAutoDefault(False)
        self.Result_Right_Button.setFlat(False)
        self.Result_Right_Button.setObjectName("Result_Right_Button")
        self.Result_Left_Button = QtWidgets.QPushButton(Dialog)
        self.Result_Left_Button.setGeometry(QtCore.QRect(90, 660, 93, 28))
        self.Result_Left_Button.setAutoDefault(False)
        self.Result_Left_Button.setObjectName("Result_Left_Button")
        self.Image_Selector = QtWidgets.QSpinBox(Dialog)
        self.Image_Selector.setGeometry(QtCore.QRect(940, 770, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.Image_Selector.setFont(font)
        self.Image_Selector.setMaximum(2000)
        self.Image_Selector.setProperty("value", 0)
        self.Image_Selector.setObjectName("Image_Selector")
        self.Motion_Type = QtWidgets.QComboBox(Dialog)
        self.Motion_Type.setGeometry(QtCore.QRect(1640, 90, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.Motion_Type.setFont(font)
        self.Motion_Type.setObjectName("Motion_Type")
        self.Motion_Type.addItem("")
        self.Motion_Type.addItem("")
        self.Motion_Type.addItem("")
        self.textBrowser_6 = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser_6.setGeometry(QtCore.QRect(1610, 40, 191, 41))
        self.textBrowser_6.setObjectName("textBrowser_6")
        self.textBrowser_7 = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser_7.setGeometry(QtCore.QRect(180, 410, 191, 41))
        self.textBrowser_7.setObjectName("textBrowser_7")
        self.KL_Chart_Button = QtWidgets.QCheckBox(Dialog)
        self.KL_Chart_Button.setGeometry(QtCore.QRect(180, 460, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.KL_Chart_Button.setFont(font)
        self.KL_Chart_Button.setObjectName("KL_Chart_Button")
        self.Load_Yolo_Button = QtWidgets.QPushButton(Dialog)
        self.Load_Yolo_Button.setGeometry(QtCore.QRect(630, 760, 81, 31))
        self.Load_Yolo_Button.setObjectName("Load_Yolo_Button")
        self.textBrowser_8 = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser_8.setGeometry(QtCore.QRect(1610, 710, 191, 41))
        self.textBrowser_8.setObjectName("textBrowser_8")
        self.Yolo_Result_Button = QtWidgets.QCheckBox(Dialog)
        self.Yolo_Result_Button.setGeometry(QtCore.QRect(1610, 760, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.Yolo_Result_Button.setFont(font)
        self.Yolo_Result_Button.setObjectName("Yolo_Result_Button")
        self.Detect_Button = QtWidgets.QPushButton(Dialog)
        self.Detect_Button.setGeometry(QtCore.QRect(180, 490, 141, 28))
        self.Detect_Button.setObjectName("Detect_Button")
        self.FileName.raise_()
        self.SaveFileButton.raise_()
        self.layoutWidget.raise_()
        self.layoutWidget.raise_()
        self.img_label1.raise_()
        self.Right_Button.raise_()
        self.Left_Button.raise_()
        self.img_label2.raise_()
        self.img_text2.raise_()
        self.img_text1.raise_()
        self.SIFT_Button.raise_()
        self.textBrowser.raise_()
        self.textBrowser_2.raise_()
        self.textBrowser_3.raise_()
        self.Distance_Limit.raise_()
        self.Limit_Button.raise_()
        self.textBrowser_4.raise_()
        self.target_label.raise_()
        self.Target_Button.raise_()
        self.Target_BF_Button.raise_()
        self.Target_Hungarian_Button.raise_()
        self.textBrowser_5.raise_()
        self.Optical_Flow_Button.raise_()
        self.Result_Data_Text.raise_()
        self.Result_Data.raise_()
        self.Dispaly_Button.raise_()
        self.Result_Right_Button.raise_()
        self.Result_Left_Button.raise_()
        self.Image_Selector.raise_()
        self.Motion_Type.raise_()
        self.textBrowser_6.raise_()
        self.textBrowser_7.raise_()
        self.KL_Chart_Button.raise_()
        self.Load_Yolo_Button.raise_()
        self.textBrowser_8.raise_()
        self.Yolo_Result_Button.raise_()
        self.Detect_Button.raise_()

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
        self.Target_Button.setText(_translate("Dialog", "Target"))
        self.Target_BF_Button.setText(_translate("Dialog", "BF_match"))
        self.Target_Hungarian_Button.setText(_translate("Dialog", "Hungarian_match"))
        self.textBrowser_5.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'PMingLiU\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Optical Flow</span></p></body></html>"))
        self.Optical_Flow_Button.setText(_translate("Dialog", "Show Optical Flow"))
        self.Result_Data_Text.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'PMingLiU\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#ffffff;\"><span style=\" background-color:#ffffff;\">Display Detect Result Data</span></p></body></html>"))
        self.Result_Data.setItemText(0, _translate("Dialog", "Bus"))
        self.Result_Data.setItemText(1, _translate("Dialog", "Car1"))
        self.Result_Data.setItemText(2, _translate("Dialog", "Car2"))
        self.Result_Data.setItemText(3, _translate("Dialog", "Autobike1"))
        self.Result_Data.setItemText(4, _translate("Dialog", "Autobike2"))
        self.Dispaly_Button.setText(_translate("Dialog", "Display"))
        self.SaveFileButton.setText(_translate("Dialog", "Save"))
        self.Result_Right_Button.setText(_translate("Dialog", ">"))
        self.Result_Left_Button.setText(_translate("Dialog", "<"))
        self.Motion_Type.setItemText(0, _translate("Dialog", "Kalman"))
        self.Motion_Type.setItemText(1, _translate("Dialog", "Origin"))
        self.Motion_Type.setItemText(2, _translate("Dialog", "Complex"))
        self.textBrowser_6.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'PMingLiU\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Motion type</span></p></body></html>"))
        self.textBrowser_7.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'PMingLiU\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Show Info option</span></p></body></html>"))
        self.KL_Chart_Button.setText(_translate("Dialog", "Show kalman chart"))
        self.Load_Yolo_Button.setText(_translate("Dialog", "Load yolo"))
        self.textBrowser_8.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'PMingLiU\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Yolo Result</span></p></body></html>"))
        self.Yolo_Result_Button.setText(_translate("Dialog", "Show Yolo Result"))
        self.Detect_Button.setText(_translate("Dialog", "Detect without image"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

