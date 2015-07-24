from PyQt4 import QtGui, QtCore

class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        layout = QtGui.QHBoxLayout(self)
        self.button = QtGui.QToolButton(self)
        self.button.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.button.setMenu(QtGui.QMenu(self.button))
        self.textBox = QtGui.QTextBrowser(self)
        action = QtGui.QWidgetAction(self.button)
        action.setDefaultWidget(self.textBox)
        self.button.menu().addAction(action)
        layout.addWidget(self.button)

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.resize(100, 60)
    window.show()
    sys.exit(app.exec_())

