from regex import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from searching import *
import itertools
import os
import sys
from uploadFile import upload 
from PyQt5.uic import loadUiType
from PyQt5.uic.Compiler.indenter import createCodeIndenter
import time

#Loading UI files
ui, _ = loadUiType('search.ui')
browsedata, _ = loadUiType('browse.ui')

# initializing browse pop-up methods
class browse(QDialog, browsedata):
    def __init__(self):  # constructor
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowTitle('Browse Files')
        self.setWindowIcon(QIcon('icons/logo2.png'))
        style = open('themes/amoled.css', 'r')
        style = style.read()
        self.setStyleSheet(style)
        self.browse.clicked.connect(self.browsefiles)
        self.pushButton.clicked.connect(self.addfile)
        self.pushButton_2.clicked.connect(self.close_browse)

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Open file', r'A:\DSA', 'Files (*.JSON)')
        file = self.filename.setText(fname[0])

    def addfile(self):
        originalPath = self.filename.text()  # address of file
        upload(originalPath)
        self.label.setText('New File Added Successfully!')

    def close_browse(self):
        self.close()



#MainWindow begins here
class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.tabWidget.tabBar().setVisible(False)
        self.setWindowTitle('Search Engine')
        self.setWindowIcon(QIcon('icons/flash.png'))
        style = open('themes/amoled.css', 'r')
        style = style.read()
        self.setStyleSheet(style)
        self.showMaximized()

        #connecting buttons with corresponding methods
        self.pushButton.clicked.connect(self.show_results)
        self.pushButton_3.clicked.connect(self.show_home)
        self.pushButton_2.clicked.connect(self.show_results2)
        self.pushButton_4.clicked.connect(self.handle_browse)

    #method to print results in the TextBrowser
    def show_results(self):
        if self.lineEdit.text() == '':
            self.label_4.setText('Please Enter a Query First!')
            return

        else:
            self.tabWidget.setCurrentIndex(1)
            self.textBrowser.setText('')
            self.tabWidget.setStyleSheet("border: 0px;background-color: rgb(5, 5, 5);")
            self.textBrowser.setStyleSheet("border: 0px;background-color: rgb(5, 5, 5);")


            searchinput = self.lineEdit.text()
            self.lineEdit_2.setText(searchinput)
            start_time = time.time()
            data = search(searchinput)

            timetaken = str(time.time() - start_time)
            timetaken = timetaken[0:6]

            if not (data == None):
                numofresults = len(data)
                self.textBrowser.append("About %d results returned in %s seconds" %(numofresults, timetaken))
                self.textBrowser.append('')
                self.textBrowser.append('')
                data = dict(itertools.islice(data.items(), 10))
                for key in data:
                    data1 = key
                    data2 = data[key]
                    if data2[-1] == '/':        #removes '/' at end of the link for optimal hyperlink performance
                        data2 = data2[:-1]
                    self.textBrowser.append('<a href=%s>%s</a>' % (data2, data1))
                    self.textBrowser.append(str(data2))
                    self.textBrowser.append('')
            else:
                self.textBrowser.setStyleSheet("color: rgb(255, 250, 252);")
                self.textBrowser.append('OOPS! This query yielded no results...')

    #method to print results in the second tab
    def show_results2(self):
        if self.lineEdit_2.text() == '':
            self.label_7.setText('Please Enter a Query First!')
            return
        else:

            self.tabWidget.setStyleSheet("border: 0px;background-color: rgb(5, 5, 5);")
            self.textBrowser.setStyleSheet("border: 0px;background-color: rgb(5, 5, 5);")
            self.textBrowser.setText('')
            searchinput = self.lineEdit_2.text()
            start_time = time.time()
            data = search(searchinput)
            timetaken = str(time.time() - start_time)
            timetaken = timetaken[0:6]

            if not (data == None):
                numofresults = len(data)
                self.textBrowser.append("About %d results returned in %s seconds" %(numofresults, timetaken))
                self.textBrowser.append('')
                self.textBrowser.append('')
                data = dict(itertools.islice(data.items(), 10))
                for key in data:

                    data1 = key
                    data2 = data[key]
                    if data2[-1] == '/':
                        data2 = data2[:-1]
                    self.textBrowser.append(
                        '<a href=%s>%s</a>' % (data2, data1))
                    self.textBrowser.append(str(data2))
                    self.textBrowser.append('')
            else:
                self.textBrowser.setStyleSheet("color: rgb(255, 250, 252);")
                self.textBrowser.append('OOPS! This query yielded no results...')
    def handle_browse(self):
        self.window2 = browse()
        self.window2.show()

    #this is the return to home method
    def show_home(self):
        self.tabWidget.setCurrentIndex(0)
        style = open('themes/amoled.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.textBrowser.setText('')
        self.label_4.setText('')
        self.label_7.setText('')

#main method that executes and displays the main window
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
