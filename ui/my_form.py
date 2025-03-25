# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'my_form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGroupBox,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QScrollArea, QSizePolicy, QVBoxLayout, QWidget)
import resourse_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(893, 846)
        font = QFont()
        font.setPointSize(11)
        MainWindow.setFont(font)
        MainWindow.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        MainWindow.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        MainWindow.setStyleSheet(u" QMainWindow {\n"
"                    background-color: #FFFFE4; \n"
"                    color: #5A9656;\n"
"                }\n"
"                 \n"
"				QGroupBox {\n"
"    				border: 4px solid #402f1d;\n"
"    				border-radius: 10px;\n"
"    				margin-top: 10px;\n"
"				}\n"
"                \n"
"                QGroupBox::title {\n"
"                    subcontrol-origin: margin;\n"
"                    left: 10px;\n"
"                    padding: 0 3px 0 3px;\n"
"                    color: black;\n"
"                }\n"
"                \n"
"                QLabel#title {\n"
"                color: #B38B6D;\n"
"				background-color: none;\n"
"                }\n"
"				\n"
"				QLabel#leaf_image, QLabel#leaf_image_2 {\n"
"				background-color: none;\n"
"				}\n"
"\n"
"				QPushButton#complete_button {\n"
"				background-color: #997950;\n"
"                } \n"
"	\n"
"				QPushButton#complete_button:hover {\n"
"				background-color: #362312;\n"
"                } \n"
"                \n"
"         "
                        "       QPushButton#add_button {\n"
"                    color: white;\n"
"                    font-weight: bold;\n"
"                    font-size: 14px;\n"
"                    border: none;\n"
"                    padding: 2px 16px;\n"
"                    border-radius: 5px;\n"
"                }\n"
"				\n"
"				 QPushButton#add_catagory_button {\n"
"				 padding: 0px 0px;\n"
"				 }\n"
"				\n"
"				 QPushButton#add_catagory_button:hover {\n"
"				 background-color: #5A9656;\n"
"				 }\n"
"		\n"
"				 QPushButton#remove_catagory_button {\n"
"				 padding: 0px 0px;\n"
"				 }\n"
"				\n"
"				 QPushButton#remove_catagory_button:hover {\n"
"				 color: black;\n"
"                background-color: #ff7770;\n"
"				 }\n"
"                \n"
"                QPushButton#add_button:hover {\n"
"                background-color: #5A9656;\n"
"                }\n"
"                \n"
"                QPushButton#remove_button {\n"
"                    color: white;\n"
"                    font-weight: bold;\n"
" "
                        "                   font-size: 14px;\n"
"                    border: none;\n"
"                    padding: 2px 10px;\n"
"                    border-radius: 5px;\n"
"                }\n"
"                \n"
"                QPushButton#remove_button:hover {\n"
"				 color: black;\n"
"                background-color: #ff7770;\n"
"                }\n"
"\n"
"                QPushButton#remove_button_2 {\n"
"                    color: white;\n"
"                    font-weight: bold;\n"
"                    font-size: 14px;\n"
"                    border: none;\n"
"                    padding: 2px 10px;\n"
"                    border-radius: 5px;\n"
"                }\n"
"                \n"
"                QPushButton#remove_button_2:hover {\n"
"				 color: black;\n"
"                background-color: #ff7770;\n"
"                }\n"
"                \n"
"                QPushButton {\n"
"                    background-color: #555;\n"
"                    color: white;\n"
"                    border: none;\n"
""
                        "                    padding: 2px 16px;\n"
"                    border-radius: 5px;\n"
"                }\n"
"                QPushButton:hover {\n"
"                    background-color: #362312;\n"
"                }\n"
"                QLineEdit {\n"
"                    background-color: #444;\n"
"                    color: #eee;\n"
"                    border: 1px solid #555;\n"
"                    border-radius: 3px;\n"
"                    padding: 2px;\n"
"                }\n"
"\n"
"				QLabel {\n"
"    				font-weight: bold;\n"
"                }\n"
"\n"
"				QCheckBox {\n"
"    				font-weight: bold;\n"
"				}\n"
"\n"
"				QScrollArea#in_progress_scroll,\n"
"				QScrollArea#completed_scroll {\n"
"    				background-color: #48260D;\n"
"   					border-radius: 10px; \n"
"				}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.title = QLabel(self.centralwidget)
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(290, 40, 291, 101))
        font1 = QFont()
        font1.setFamilies([u"DynaPuff Condensed"])
        font1.setPointSize(60)
        font1.setBold(True)
        font1.setUnderline(True)
        self.title.setFont(font1)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.in_progress_group = QGroupBox(self.centralwidget)
        self.in_progress_group.setObjectName(u"in_progress_group")
        self.in_progress_group.setGeometry(QRect(20, 220, 401, 591))
        font2 = QFont()
        font2.setPointSize(11)
        font2.setBold(True)
        self.in_progress_group.setFont(font2)
        self.verticalLayoutWidget = QWidget(self.in_progress_group)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 50, 361, 501))
        self.in_progress_v_layout = QVBoxLayout(self.verticalLayoutWidget)
        self.in_progress_v_layout.setSpacing(0)
        self.in_progress_v_layout.setObjectName(u"in_progress_v_layout")
        self.in_progress_v_layout.setContentsMargins(0, 0, 0, 0)
        self.in_progress_scroll = QScrollArea(self.verticalLayoutWidget)
        self.in_progress_scroll.setObjectName(u"in_progress_scroll")
        self.in_progress_scroll.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 359, 499))
        self.scrollAreaWidgetContents.setAutoFillBackground(True)
        self.in_progress_scroll.setWidget(self.scrollAreaWidgetContents)

        self.in_progress_v_layout.addWidget(self.in_progress_scroll)

        self.lineEdit = QLineEdit(self.in_progress_group)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(10, 560, 161, 22))
        self.add_button = QPushButton(self.in_progress_group)
        self.add_button.setObjectName(u"add_button")
        self.add_button.setGeometry(QRect(180, 560, 91, 24))
        self.progress_catagory = QComboBox(self.in_progress_group)
        self.progress_catagory.setObjectName(u"progress_catagory")
        self.progress_catagory.setGeometry(QRect(10, 20, 241, 24))
        self.add_catagory_button = QPushButton(self.in_progress_group)
        self.add_catagory_button.setObjectName(u"add_catagory_button")
        self.add_catagory_button.setGeometry(QRect(260, 20, 51, 21))
        font3 = QFont()
        font3.setFamilies([u"Fira Code"])
        font3.setPointSize(20)
        font3.setBold(True)
        self.add_catagory_button.setFont(font3)
        self.add_catagory_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.add_catagory_button.setIconSize(QSize(16, 16))
        self.remove_catagory_button = QPushButton(self.in_progress_group)
        self.remove_catagory_button.setObjectName(u"remove_catagory_button")
        self.remove_catagory_button.setGeometry(QRect(320, 20, 51, 21))
        self.remove_catagory_button.setFont(font3)
        self.remove_catagory_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.remove_catagory_button.setIconSize(QSize(16, 16))
        self.remove_button_2 = QPushButton(self.in_progress_group)
        self.remove_button_2.setObjectName(u"remove_button_2")
        self.remove_button_2.setGeometry(QRect(280, 560, 91, 24))
        font4 = QFont()
        font4.setBold(True)
        self.remove_button_2.setFont(font4)
        self.completed_group = QGroupBox(self.centralwidget)
        self.completed_group.setObjectName(u"completed_group")
        self.completed_group.setGeometry(QRect(460, 220, 401, 591))
        self.completed_group.setFont(font2)
        self.verticalLayoutWidget_2 = QWidget(self.completed_group)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 50, 361, 501))
        self.completed_v_layout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.completed_v_layout.setObjectName(u"completed_v_layout")
        self.completed_v_layout.setContentsMargins(0, 0, 0, 0)
        self.completed_scroll = QScrollArea(self.verticalLayoutWidget_2)
        self.completed_scroll.setObjectName(u"completed_scroll")
        self.completed_scroll.setFrameShape(QFrame.Shape.StyledPanel)
        self.completed_scroll.setFrameShadow(QFrame.Shadow.Sunken)
        self.completed_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.completed_scroll.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 359, 499))
        self.scrollAreaWidgetContents_2.setAutoFillBackground(True)
        self.completed_scroll.setWidget(self.scrollAreaWidgetContents_2)

        self.completed_v_layout.addWidget(self.completed_scroll)

        self.remove_button = QPushButton(self.completed_group)
        self.remove_button.setObjectName(u"remove_button")
        self.remove_button.setGeometry(QRect(280, 560, 91, 24))
        self.search_box = QLineEdit(self.completed_group)
        self.search_box.setObjectName(u"search_box")
        self.search_box.setGeometry(QRect(10, 560, 161, 22))
        self.search_button = QPushButton(self.completed_group)
        self.search_button.setObjectName(u"search_button")
        self.search_button.setGeometry(QRect(180, 560, 91, 24))
        self.completed_catagory = QComboBox(self.completed_group)
        self.completed_catagory.setObjectName(u"completed_catagory")
        self.completed_catagory.setGeometry(QRect(10, 20, 361, 24))
        self.complete_button = QPushButton(self.centralwidget)
        self.complete_button.setObjectName(u"complete_button")
        self.complete_button.setGeometry(QRect(300, 140, 271, 41))
        font5 = QFont()
        font5.setFamilies([u"DynaPuff Condensed"])
        font5.setPointSize(16)
        self.complete_button.setFont(font5)
        self.leaf_image = QLabel(self.centralwidget)
        self.leaf_image.setObjectName(u"leaf_image")
        self.leaf_image.setEnabled(True)
        self.leaf_image.setGeometry(QRect(50, 20, 181, 141))
        self.leaf_image.setPixmap(QPixmap(u":/images/images/leaf.png"))
        self.leaf_image.setScaledContents(True)
        self.leaf_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.leaf_image.setWordWrap(False)
        self.leaf_image_2 = QLabel(self.centralwidget)
        self.leaf_image_2.setObjectName(u"leaf_image_2")
        self.leaf_image_2.setEnabled(True)
        self.leaf_image_2.setGeometry(QRect(650, 60, 181, 131))
        self.leaf_image_2.setPixmap(QPixmap(u":/images/images/leaf2.png"))
        self.leaf_image_2.setScaledContents(True)
        self.leaf_image_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.leaf_image_2.setWordWrap(False)
        MainWindow.setCentralWidget(self.centralwidget)
        QWidget.setTabOrder(self.lineEdit, self.add_button)
        QWidget.setTabOrder(self.add_button, self.in_progress_scroll)
        QWidget.setTabOrder(self.in_progress_scroll, self.search_box)
        QWidget.setTabOrder(self.search_box, self.search_button)
        QWidget.setTabOrder(self.search_button, self.remove_button)
        QWidget.setTabOrder(self.remove_button, self.completed_scroll)
        QWidget.setTabOrder(self.completed_scroll, self.complete_button)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.title.setText(QCoreApplication.translate("MainWindow", u"Checklist", None))
        self.in_progress_group.setTitle(QCoreApplication.translate("MainWindow", u"In Progress", None))
#if QT_CONFIG(tooltip)
        self.add_button.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.add_button.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.add_button.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.add_catagory_button.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.remove_catagory_button.setText(QCoreApplication.translate("MainWindow", u"-", None))
#if QT_CONFIG(tooltip)
        self.remove_button_2.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.remove_button_2.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.remove_button_2.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.completed_group.setTitle(QCoreApplication.translate("MainWindow", u"Completed", None))
#if QT_CONFIG(tooltip)
        self.remove_button.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.remove_button.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.remove_button.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
#if QT_CONFIG(statustip)
        self.search_box.setStatusTip("")
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(tooltip)
        self.search_button.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.search_button.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.search_button.setText(QCoreApplication.translate("MainWindow", u"Search", None))
#if QT_CONFIG(tooltip)
        self.complete_button.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.complete_button.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.complete_button.setText(QCoreApplication.translate("MainWindow", u"Complete", None))
        self.leaf_image.setText("")
        self.leaf_image_2.setText("")
    # retranslateUi

