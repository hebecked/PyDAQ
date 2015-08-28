# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UIs/Monochromator.ui'
#
# Created: Tue Aug 11 15:46:39 2015
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import sys
sys.path.append("..")
from monochromator import CornerStone260
from Data_IO import serialports

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Monochromatorcontrol(object):
    def setupUi(self, Monochromatorcontrol):
        self.comport=None
        '''
        #Main window
        '''
        Monochromatorcontrol.setObjectName(_fromUtf8("Monochromatorcontrol"))
        Monochromatorcontrol.resize(279, 784)
        Monochromatorcontrol.setWindowTitle(QtGui.QApplication.translate("Monochromatorcontrol", "Monochromator control", None, QtGui.QApplication.UnicodeUTF8))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("UIs/colour.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        Monochromatorcontrol.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(Monochromatorcontrol)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        '''
        #Com Port selection
        '''
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setText(QtGui.QApplication.translate("Monochromatorcontrol", "Serial Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.comboBox_2 = QtGui.QComboBox(self.centralwidget)
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.verticalLayout.addWidget(self.comboBox_2)
        self.horizontalLayout_5.addLayout(self.verticalLayout)
        self.init_comportmenu()
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setText(QtGui.QApplication.translate("Monochromatorcontrol", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_5.addWidget(self.pushButton)
        self.gridLayout.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 29, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        '''
        #Wavelength selection
        '''
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setText(QtGui.QApplication.translate("Monochromatorcontrol", "Wavlength [nm]", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        self.lineEdit_2 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_2.setText(QtGui.QApplication.translate("Monochromatorcontrol", "Wavelength [nm]", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.verticalLayout_2.addWidget(self.lineEdit_2)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setText(QtGui.QApplication.translate("Monochromatorcontrol", "Set", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout_4.addWidget(self.pushButton_2)
        self.gridLayout.addLayout(self.horizontalLayout_4, 2, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 30, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        '''
        #Grating selection
        '''
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setText(QtGui.QApplication.translate("Monochromatorcontrol", "Grating", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_3.addWidget(self.label_3)
        self.comboBox_3 = QtGui.QComboBox(self.centralwidget)
        self.comboBox_3.setObjectName(_fromUtf8("comboBox_3"))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.setItemText(0, QtGui.QApplication.translate("Monochromatorcontrol", "Grating 0", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.setItemText(1, QtGui.QApplication.translate("Monochromatorcontrol", "Grating 1", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.setItemText(2, QtGui.QApplication.translate("Monochromatorcontrol", "Grating 2", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout_3.addWidget(self.comboBox_3)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.pushButton_3 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_3.setText(QtGui.QApplication.translate("Monochromatorcontrol", "Set", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.horizontalLayout_3.addWidget(self.pushButton_3)
        self.gridLayout.addLayout(self.horizontalLayout_3, 4, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 29, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 5, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        '''
        #Filter selection
        '''
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setText(QtGui.QApplication.translate("Monochromatorcontrol", "Filter", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_4.addWidget(self.label_4)
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(0, QtGui.QApplication.translate("Monochromatorcontrol", "Filter 1", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(1, QtGui.QApplication.translate("Monochromatorcontrol", "Filter 2", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(2, QtGui.QApplication.translate("Monochromatorcontrol", "Filter 3", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(3, QtGui.QApplication.translate("Monochromatorcontrol", "Filter 4", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(4, QtGui.QApplication.translate("Monochromatorcontrol", "Filter 5", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(5, QtGui.QApplication.translate("Monochromatorcontrol", "Filter 6", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout_4.addWidget(self.comboBox)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.pushButton_4 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_4.setText(QtGui.QApplication.translate("Monochromatorcontrol", "Set", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        self.gridLayout.addLayout(self.horizontalLayout_2, 6, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 29, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 7, 0, 1, 1)
        '''
        #Shutter control
        '''
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setText(QtGui.QApplication.translate("Monochromatorcontrol", "Shutter", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayout_5.addWidget(self.label_6)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton_6 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_6.setText(QtGui.QApplication.translate("Monochromatorcontrol", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.horizontalLayout.addWidget(self.pushButton_6)
        self.pushButton_7 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_7.setText(QtGui.QApplication.translate("Monochromatorcontrol", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))
        self.horizontalLayout.addWidget(self.pushButton_7)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout_5, 8, 0, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(20, 29, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 9, 0, 1, 1)
        '''
        #Port control
        '''
        self.verticalLayout_p = QtGui.QVBoxLayout()
        self.verticalLayout_p.setObjectName(_fromUtf8("verticalLayout_p"))
        self.label_p = QtGui.QLabel(self.centralwidget)
        self.label_p.setText(QtGui.QApplication.translate("Monochromatorcontrol", "Out Port", None, QtGui.QApplication.UnicodeUTF8))
        self.label_p.setObjectName(_fromUtf8("label_p"))
        self.verticalLayout_p.addWidget(self.label_p)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton_p1 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_p1.setText(QtGui.QApplication.translate("Monochromatorcontrol", "Port 1", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_p1.setObjectName(_fromUtf8("pushButton_p1"))
        self.horizontalLayout.addWidget(self.pushButton_p1)
        self.pushButton_p2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_p2.setText(QtGui.QApplication.translate("Monochromatorcontrol", "Port 2", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_p2.setObjectName(_fromUtf8("pushButton_p2"))
        self.horizontalLayout.addWidget(self.pushButton_p2)
        self.verticalLayout_p.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout_p, 10, 0, 1, 1)
        spacerItemp = QtGui.QSpacerItem(20, 29, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItemp, 9, 0, 1, 1)
        '''
        #Monochromator info
        '''
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setText(QtGui.QApplication.translate("Monochromatorcontrol", "Current settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_6.addWidget(self.label_5)
        self.pushButton_5 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_5.setText(QtGui.QApplication.translate("Monochromatorcontrol", "Obtain", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.horizontalLayout_6.addWidget(self.pushButton_5)
        self.verticalLayout_6.addLayout(self.horizontalLayout_6)
        self.textEdit = QtGui.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.verticalLayout_6.addWidget(self.textEdit)
        self.gridLayout.addLayout(self.verticalLayout_6, 12, 0, 1, 1)
        Monochromatorcontrol.setCentralWidget(self.centralwidget)
        '''
        #Menu Bar
        '''
        self.menubar = QtGui.QMenuBar(Monochromatorcontrol)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 279, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setTitle(QtGui.QApplication.translate("Monochromatorcontrol", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        Monochromatorcontrol.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(Monochromatorcontrol)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        Monochromatorcontrol.setStatusBar(self.statusbar)
        self.actionOpen_Config = QtGui.QAction(Monochromatorcontrol)
        self.actionOpen_Config.setText(QtGui.QApplication.translate("Monochromatorcontrol", "&Open Config", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_Config.setShortcut(QtGui.QApplication.translate("Monochromatorcontrol", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_Config.setObjectName(_fromUtf8("actionOpen_Config"))
        self.actionClose = QtGui.QAction(Monochromatorcontrol)
        self.actionClose.setText(QtGui.QApplication.translate("Monochromatorcontrol", "&Close", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setShortcut(QtGui.QApplication.translate("Monochromatorcontrol", "Ctrl+W", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setIconVisibleInMenu(True)
        self.actionClose.setObjectName(_fromUtf8("actionClose"))
        self.actionStore_Config = QtGui.QAction(Monochromatorcontrol)
        self.actionStore_Config.setText(QtGui.QApplication.translate("Monochromatorcontrol", "&Store Config", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStore_Config.setShortcut(QtGui.QApplication.translate("Monochromatorcontrol", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStore_Config.setObjectName(_fromUtf8("actionStore_Config"))
        self.menuFile.addAction(self.actionOpen_Config)
        self.menuFile.addAction(self.actionStore_Config)
        self.menuFile.addAction(self.actionClose)
        self.menubar.addAction(self.menuFile.menuAction())


        '''
        #Connect actions
        '''
        self.retranslateUi(Monochromatorcontrol)
        QtCore.QObject.connect(self.actionClose, QtCore.SIGNAL(_fromUtf8("activated()")), Monochromatorcontrol.close)
        QtCore.QObject.connect(self.actionOpen_Config, QtCore.SIGNAL(_fromUtf8("activated()")), self.error)
        QtCore.QObject.connect(self.actionStore_Config, QtCore.SIGNAL(_fromUtf8("activated()")), self.error)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.connect)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.set_wavelength)
        QtCore.QObject.connect(self.pushButton_3, QtCore.SIGNAL(_fromUtf8("clicked()")), self.set_grating)
        QtCore.QObject.connect(self.pushButton_4, QtCore.SIGNAL(_fromUtf8("clicked()")), self.set_filter)
        QtCore.QObject.connect(self.pushButton_5, QtCore.SIGNAL(_fromUtf8("clicked()")), self.getInfo)
        QtCore.QObject.connect(self.pushButton_6, QtCore.SIGNAL(_fromUtf8("clicked()")), self.open_shutter)
        QtCore.QObject.connect(self.pushButton_7, QtCore.SIGNAL(_fromUtf8("clicked()")), self.close_shutter)
        QtCore.QObject.connect(self.pushButton_p1, QtCore.SIGNAL(_fromUtf8("clicked()")), self.Port1)
        QtCore.QObject.connect(self.pushButton_p2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.Port2)
        
        

        QtCore.QMetaObject.connectSlotsByName(Monochromatorcontrol)


    def retranslateUi(self, Monochromatorcontrol):
        pass

    def init_comportmenu(self):
        p=serialports()
        items=p.ports
        for i in range(len(items)):
            self.comboBox_2.setItemText(i, QtGui.QApplication.translate("Monochromatorcontrol", items[i], None, QtGui.QApplication.UnicodeUTF8))

    def get_comport(self):
        return self.comboBox_2.currentText()

    def connect(self):
        new_comport=self.get_comport()
        if self.comport==new_comport:
            self.error(msg="Com Port identical to current Port")
            return
        if self.comport!=None:
            self.mc.SetSerialPort(new_comport)
        else:
            self.mc = CornerStone260( port = new_comport)
        self.comport=new_comport
        self.init_gratingmenu()
        self.init_filtermenu()

    def set_wavelength(self):
        if 'mc' not in locals():
            self.error(msg="Not connected!")
            return
        wvl=self.lineEdit_2.text()
        try:
            wvl=float(wvl)
            if wvl<0 or wvl>2000:
                raise ValueError()
        except ValueError:
            self.error(msg="This is not a valid Wavelength!")
            return
        self.mc.Units_NM()
        self.mc.GoWave(wvl)
        self.textEdit.clear()
        self.textEdit.append("Wavelength set to " + str(mc.GetWave) + " nm")


    def init_gratingmenu(self):
        if 'mc' not in locals():
            self.error(msg="Not connected!")
            return
        for i in range(3):
            gratings=str(i) + " " + mc.GetLabel(i)
            self.comboBox_3.setItemText(i, QtGui.QApplication.translate("Monochromatorcontrol", gratings, None, QtGui.QApplication.UnicodeUTF8))

    def init_filtermenu(self):
        if 'mc' not in locals():
            self.error(msg="Not connected!")
            return
        for i in range(6):
            filters=str(i) + " " + mc.GetFilterLabel(i)
            self.comboBox.setItemText(i, QtGui.QApplication.translate("Monochromatorcontrol", filters, None, QtGui.QApplication.UnicodeUTF8))

    def set_grating(self):
        new_grating=self.comboBox_3.currentIndex()
        self.mc.Grat(new_grating)

    def set_filter(self):
        new_filter=self.comboBox.currentIndex()
        self.mc.Filter(new_filter)

    def open_shutter(self):
        if 'mc' not in locals():
            self.error(msg="Not connected!")
            return
        self.mc.ShutterOpen()

    def close_shutter(self):
        if 'mc' not in locals():
            self.error(msg="Not connected!")
            return
        self.mc.ShutterClose()

    def Port1(self):
        if 'mc' not in locals():
            self.error(msg="Not connected!")
            return
        self.mc.OutPort(1)

    def Port2(self):
        if 'mc' not in locals():
            self.error(msg="Not connected!")
            return
        self.mc.OutPort(2)


    def getInfo(self):
        if 'mc' not in locals():
            self.error(msg="Not connected!")
            return
        mcinfo=self.mc.GetInfo() #if not complete information compile one
        self.textEdit.clear()
        self.textEdit.append(mcinfo)

    def error(self,msg=""):
        self.textEdit.clear()
        self.textEdit.append("Error: " + msg)


if __name__ == "__main__":
    '''
    #Add menu for output selection
    #indicate for all things the current state?
    #load values from config file
    #write values from config file
    '''
    import sys
    app = QtGui.QApplication(sys.argv)
    Monochromatorcontrol = QtGui.QMainWindow()
    ui = Ui_Monochromatorcontrol()
    ui.setupUi(Monochromatorcontrol)
    Monochromatorcontrol.show()
    sys.exit(app.exec_())

