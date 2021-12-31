from regex import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from searching import *
import itertools
import os
import sys

from PyQt5.uic import loadUiType
from PyQt5.uic.Compiler.indenter import createCodeIndenter

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
        self.pushButton.clicked.connect(self.addfile)
        self.pushButton_2.clicked.connect(self.close_browse)


    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(
        self, 'Open file', r'C:\Users\Safi\Desktop\IndexBasedSearchEngine-main\DataSet', 'Files (*.JSON)')
        file = self.filename.setText(fname[0])

    def addfile(self):
        filepath = self.filename.text() # address of file
        filename = os.path.basename(filepath)   #extracting name of file

        dir = "C:\\Users\Safi\Desktop\\IndexBasedSearchEngine-main\\DataSet"
        newfile = os.path.join(dir, filename)
        with open(filepath,'r') as firstfile, open(newfile,'a') as secondfile:
      
            for line in firstfile:
               
             # append content to second file
                secondfile.write(line)

        self.label.setText('New File Added Successfully!')

    def close_browse(self):
        self.close()


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
        if self.lineEdit.text() == '':
            self.label_4.setText('Please Enter a Query First!')
            return

        else:
            self.tabWidget.setCurrentIndex(1)
            self.textBrowser.setText('')
        # self.tabWidget.setStyleSheet("background-image: url(:/icons/logo3.png)")
            self.textBrowser.setStyleSheet("border: 0px")
        # self.textBrowser.setStyleSheet("background-color: rgb(230, 230, 230)")
        # self.textBrowser.setStyleSheet("background-color: rgb(10, 10, 10)")


            searchinput = self.lineEdit.text()
            self.lineEdit_2.setText(searchinput)

            data = search(searchinput)
            data = dict(itertools.islice(data.items(), 10))

            if not (data == None):
                for key in data:
                    data1 = key
                    data2 = data[key]
                    data2 = data2[:-1]
                    self.textBrowser.append('<a href=%s>%s</a>' % (data2, data1))
                    self.textBrowser.append(data2)
                    self.textBrowser.append('')

    def show_results2(self):
        if self.lineEdit_2.text() == '':
            self.label_7.setText('Please Enter a Query First!')
            return
        else:

            self.textBrowser.setStyleSheet("border: 0px")
        # self.tabBrowser.setStyleSheet("background-color: rgb(240, 212, 215)")
            self.textBrowser.setText('')
            searchinput = self.lineEdit_2.text()

            data = search(searchinput)
            data = dict(itertools.islice(data.items(), 10))

            if not (data == None):
                for key in data:

                    data1 = key
                    data2 = data[key]
                    data2 = data2[:-1]
                    self.textBrowser.append('<a href=%s>%s</a>' % (data2, data1))
                    self.textBrowser.append(data2)
                    self.textBrowser.append('')

    def handle_browse(self):
        self.window2 = browse()
        self.window2.show()



    def show_home(self):
        self.tabWidget.setCurrentIndex(0)
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.textBrowser.setText('')
        self.label_4.setText('')
        self.label_7.setText('')


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
