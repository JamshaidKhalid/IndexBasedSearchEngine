from regex import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from searching import *
import sys

from PyQt5.uic import loadUiType
from PyQt5.uic.Compiler.indenter import createCodeIndenter

from searching import singleWordSearch
ui, _ = loadUiType('search.ui')
browsedata, _ = loadUiType('browse.ui')


class browse(QDialog, browsedata):
    def __init__(self):  # constructor
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowTitle('Browse Files')
        style = open('themes/amoled.css', 'r')
        style = style.read()
        self.setStyleSheet(style)
        self.browse.clicked.connect(self.browsefiles)

    def browsefiles(self):
        fname=QFileDialog.getOpenFileName(self, 'Open file', r'C:\Users\Safi\Desktop\IndexBasedSearchEngine-main\DataSet', 'Images (*.JSON)')
        self.filename.setText(fname[0])
        




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
        self.pushButton_2.clicked.connect(self.show_results2)
        self.pushButton_4.clicked.connect(self.handle_browse)


    def show_results(self):
        self.tabWidget.setCurrentIndex(1)
        self.textBrowser.setStyleSheet("border: 0px")
        self.textBrowser.setText('')


        # this line of code adds hyperlinks in labels
        # linkTemplate = '<a href={0}>{1}>.format({2},{3}</a>'
        # EXAMPLE:  self.label_3.setText(linkTemplate.format('https://Google.com', 'Google.com'))
        searchinput = self.lineEdit.text()
        self.lineEdit_2.setText(searchinput) 

        data = singleWordSearch(searchinput)
        # print (data)x


        for key in data.keys():

            data1 = data[key][0]
            data2 = data[key][1]
            data2 = data2[:-1]
            self.textBrowser.append('<a href=%s>%s</a>'%(data2,data1))
            self.textBrowser.append('')

    def show_results2(self):

        self.textBrowser.setStyleSheet("border: 0px")
        self.textBrowser.setText('')
        searchinput = self.lineEdit_2.text()

        data = singleWordSearch(searchinput)

        for key in data.keys():
            data1 = data[key][0]
            data2 = data[key][1]
            data2 = data2[:-1]
            self.textBrowser.append('<a href=%s>%s</a>'%(data2,data1))
            self.textBrowser.append('')

    def handle_browse(self):
        self.window2 = browse()
        self.window2.show()

    def show_home(self):
        self.tabWidget.setCurrentIndex(0)
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.textBrowser.setText('')

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
