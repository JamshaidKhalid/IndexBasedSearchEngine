from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys 

from PyQt5.uic import loadUiType
from PyQt5.uic.Compiler.indenter import createCodeIndenter
ui,_ = loadUiType('search.ui')


class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.tabWidget.tabBar().setVisible(False) 
        self.setWindowTitle('Search Engine')
        style = open('themes/amoled.css', 'r')
        style = style.read()
        self.setStyleSheet(style)
        self.showMaximized()
        self.pushButton.clicked.connect(self.show_results)
        self.pushButton_3.clicked.connect(self.show_home)




    def show_results(self):
        self.tabWidget.setCurrentIndex(1)
        self.textBrowser.setStyleSheet("border: 0px")

        #this line of code adds hyperlinks in labels
        # linkTemplate = '<a href={0}>{1}>.format({2},{3}</a>'
        # EXAMPLE:  self.label_3.setText(linkTemplate.format('https://Google.com', 'Google.com'))


        self.textBrowser.append('Below are your search results!')
        data = 'http://google.com'
        data2 = 'Google'
        self.textBrowser.append('<a href=%s>%s</a>'%(data,data2))



    def show_home(self):
        self.tabWidget.setCurrentIndex(0)



def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()