# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_main.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QTabWidget,
    QTextBrowser, QTextEdit, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(640, 480)
        MainWindow.setMinimumSize(QSize(640, 480))
        MainWindow.setMaximumSize(QSize(640, 480))
        MainWindow.setStyleSheet(u"MainWindow\n"
"{\n"
"	background-color: #282828;\n"
"	color: ccdad1;\n"
"	\n"
"	font-family: Montserrat ExtraBold;\n"
"}")
        MainWindow.setTabShape(QTabWidget.TabShape.Rounded)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget_messages = QWidget(self.centralwidget)
        self.widget_messages.setObjectName(u"widget_messages")
        self.widget_messages.setGeometry(QRect(9, 10, 361, 391))
        self.widget_messages.setStyleSheet(u"color: #f4f3ee;\n"
"background-color: #3C3836;\n"
"border-radius: 15px;                     /* <----  \u0437\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u0435 \u043a\u0440\u0430\u0435\u0432  */ \n"
"/*border: 2px solid #094065; <----- \u0446\u0432\u0435\u0442 \u0433\u0440\u0430\u043d\u0438\u0446\u044b*/ ")
        self.text_browser = QTextBrowser(self.widget_messages)
        self.text_browser.setObjectName(u"text_browser")
        self.text_browser.setGeometry(QRect(5, 31, 351, 351))
        self.label_17 = QLabel(self.widget_messages)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QRect(90, 5, 161, 16))
        self.label_17.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_17.setStyleSheet(u"\n"
"color: #FBF1C7;\n"
"\n"
"border-radius: 0px;                     /* <----  \u0437\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u0435 \u043a\u0440\u0430\u0435\u0432  */ \n"
"font-weight: bold;\n"
"font-size: 12pt;\n"
"font-family: Montserrat ExtraBold;\n"
"border: 0px solid #38302e; /*<----- \u0446\u0432\u0435\u0442 \u0433\u0440\u0430\u043d\u0438\u0446\u044b*/\n"
"")
        self.label_17.setFrameShape(QFrame.Shape.NoFrame)
        self.label_17.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.widget_message_edit = QWidget(self.centralwidget)
        self.widget_message_edit.setObjectName(u"widget_message_edit")
        self.widget_message_edit.setGeometry(QRect(10, 410, 361, 61))
        self.widget_message_edit.setStyleSheet(u"color: #f4f3ee;\n"
"background-color: #3C3836;\n"
"border-radius: 15px;                     /* <----  \u0437\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u0435 \u043a\u0440\u0430\u0435\u0432  */ \n"
"/*border: 2px solid #094065; <----- \u0446\u0432\u0435\u0442 \u0433\u0440\u0430\u043d\u0438\u0446\u044b*/ ")
        self.button_send_message = QPushButton(self.widget_message_edit)
        self.button_send_message.setObjectName(u"button_send_message")
        self.button_send_message.setGeometry(QRect(310, 10, 41, 41))
        self.button_send_message.setStyleSheet(u"QPushButton {\n"
"color: #FBF1C7;\n"
"background-color: #D79921;\n"
"border-radius: 15px;                     /* <----  \u0437\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u0435 \u043a\u0440\u0430\u0435\u0432  */ \n"
"font-weight: bold;\n"
"font-size: 10pt;\n"
"font-family: Montserrat ExtraBold;\n"
"border: 2px solid #38302e; /*<----- \u0446\u0432\u0435\u0442 \u0433\u0440\u0430\u043d\u0438\u0446\u044b*/\n"
"}\n"
"QPushButton:hover {\n"
"color: #FBF1C7;\n"
"background-color: #FFB62A;\n"
"}\n"
"QPushButton:pressed {\n"
"color: #FBF1C7;\n"
"background-color: #B57614;\n"
"}\n"
"")
        icon = QIcon()
        icon.addFile(u":/icons/resources/icons/wing.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.button_send_message.setIcon(icon)
        self.button_send_message.setIconSize(QSize(28, 28))
        self.text_edit_message = QTextEdit(self.widget_message_edit)
        self.text_edit_message.setObjectName(u"text_edit_message")
        self.text_edit_message.setGeometry(QRect(10, 10, 291, 41))
        self.text_edit_message.setStyleSheet(u"color: #FBF1C7;\n"
"background-color: #665C54;\n"
"border-radius: 15px;                     /* <----  \u0437\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u0435 \u043a\u0440\u0430\u0435\u0432  */ \n"
"font-weight: bold;\n"
"font-size: 10pt;\n"
"font-family: Montserrat ExtraBold;\n"
"border: 2px solid #38302e; /*<----- \u0446\u0432\u0435\u0442 \u0433\u0440\u0430\u043d\u0438\u0446\u044b*/")
        self.widget_control_panel_2 = QWidget(self.centralwidget)
        self.widget_control_panel_2.setObjectName(u"widget_control_panel_2")
        self.widget_control_panel_2.setGeometry(QRect(380, 10, 251, 461))
        self.widget_control_panel_2.setStyleSheet(u"color: #f4f3ee;\n"
"background-color: #3C3836;\n"
"border-radius: 15px;                     /* <----  \u0437\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u0435 \u043a\u0440\u0430\u0435\u0432  */ \n"
"/*border: 2px solid #094065; <----- \u0446\u0432\u0435\u0442 \u0433\u0440\u0430\u043d\u0438\u0446\u044b*/ ")
        self.line_ip_address = QLineEdit(self.widget_control_panel_2)
        self.line_ip_address.setObjectName(u"line_ip_address")
        self.line_ip_address.setGeometry(QRect(10, 30, 231, 41))
        self.line_ip_address.setStyleSheet(u"color: #FBF1C7;\n"
"background-color: #665C54;\n"
"border-radius: 15px;                     /* <----  \u0437\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u0435 \u043a\u0440\u0430\u0435\u0432  */ \n"
"font-weight: bold;\n"
"font-size: 10pt;\n"
"font-family: Montserrat ExtraBold;\n"
"border: 2px solid #38302e; /*<----- \u0446\u0432\u0435\u0442 \u0433\u0440\u0430\u043d\u0438\u0446\u044b*/")
        self.label_18 = QLabel(self.widget_control_panel_2)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setGeometry(QRect(40, 0, 171, 31))
        self.label_18.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_18.setStyleSheet(u"\n"
"color: #FBF1C7;\n"
"\n"
"border-radius: 0px;                     /* <----  \u0437\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u0435 \u043a\u0440\u0430\u0435\u0432  */ \n"
"font-weight: bold;\n"
"font-size: 12pt;\n"
"font-family: Montserrat ExtraBold;\n"
"border: 0px solid #38302e; /*<----- \u0446\u0432\u0435\u0442 \u0433\u0440\u0430\u043d\u0438\u0446\u044b*/\n"
"")
        self.label_18.setFrameShape(QFrame.Shape.NoFrame)
        self.label_18.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.line_port = QLineEdit(self.widget_control_panel_2)
        self.line_port.setObjectName(u"line_port")
        self.line_port.setGeometry(QRect(10, 80, 231, 41))
        self.line_port.setStyleSheet(u"color: #FBF1C7;\n"
"background-color: #665C54;\n"
"border-radius: 15px;                     /* <----  \u0437\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u0435 \u043a\u0440\u0430\u0435\u0432  */ \n"
"font-weight: bold;\n"
"font-size: 10pt;\n"
"font-family: Montserrat ExtraBold;\n"
"border: 2px solid #38302e; /*<----- \u0446\u0432\u0435\u0442 \u0433\u0440\u0430\u043d\u0438\u0446\u044b*/")
        self.line_your_name = QLineEdit(self.widget_control_panel_2)
        self.line_your_name.setObjectName(u"line_your_name")
        self.line_your_name.setGeometry(QRect(10, 130, 231, 41))
        self.line_your_name.setStyleSheet(u"color: #FBF1C7;\n"
"background-color: #665C54;\n"
"border-radius: 15px;                     /* <----  \u0437\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u0435 \u043a\u0440\u0430\u0435\u0432  */ \n"
"font-weight: bold;\n"
"font-size: 10pt;\n"
"font-family: Montserrat ExtraBold;\n"
"border: 2px solid #38302e; /*<----- \u0446\u0432\u0435\u0442 \u0433\u0440\u0430\u043d\u0438\u0446\u044b*/")
        self.button_apply = QPushButton(self.widget_control_panel_2)
        self.button_apply.setObjectName(u"button_apply")
        self.button_apply.setGeometry(QRect(10, 180, 231, 41))
        self.button_apply.setStyleSheet(u"QPushButton {\n"
"color: #FBF1C7;\n"
"background-color: #D79921;\n"
"border-radius: 15px;                     /* <----  \u0437\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u0435 \u043a\u0440\u0430\u0435\u0432  */ \n"
"font-weight: bold;\n"
"font-size: 10pt;\n"
"font-family: Montserrat ExtraBold;\n"
"border: 2px solid #38302e; /*<----- \u0446\u0432\u0435\u0442 \u0433\u0440\u0430\u043d\u0438\u0446\u044b*/\n"
"}\n"
"QPushButton:hover {\n"
"color: #FBF1C7;\n"
"background-color: #FFB62A;\n"
"}\n"
"QPushButton:pressed {\n"
"color: #FBF1C7;\n"
"background-color: #B57614;\n"
"}\n"
"")
        self.button_apply.setIconSize(QSize(28, 28))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Torna Messenger", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"\u0427\u0430\u0442", None))
        self.button_send_message.setText("")
        self.line_ip_address.setText(QCoreApplication.translate("MainWindow", u"IP \u0430\u0434\u0440\u0435\u0441", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.line_port.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0440\u0442", None))
        self.line_your_name.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0430\u0448\u0435 \u041e\u0442\u043e\u0431\u0440\u0430\u0436\u0430\u0435\u043c\u043e\u0435 \u0438\u043c\u044f", None))
        self.button_apply.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u044c", None))
    # retranslateUi

