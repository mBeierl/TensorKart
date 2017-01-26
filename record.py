#!/usr/bin/env python

import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLabel, QApplication, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QScreen, QGuiApplication
from PyQt5.QtCore import QBasicTimer

#from utils import XboxController

SAMPLE_RATE = 200

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        # Init controller
        #self.controller = XboxController()

        # Create GUI
        self.initUI()

        # Timer
        self.timer = QBasicTimer()
        self.rate = SAMPLE_RATE
        self.timer.start(self.rate, self)

        self.recording = False
        self.t = 0


    def initUI(self):
        # Create Boxes
        hbox = QHBoxLayout()

        # Create Elements
        recordButton = QPushButton("Record")
        recordButton.clicked.connect(self.recordClicked)

        image = QPixmap(320, 240)
        self.lbl_image = QLabel(self)
        self.lbl_image.setPixmap(image)


        # Add Elements to Boxes
        hbox.addStretch(1)
        hbox.addWidget(self.lbl_image)
        hbox.addWidget(recordButton)

        # Assign Layout
        self.setLayout(hbox)

        # Position Window, set Title & show
        self.setGeometry(0, 0, 660, 330)
        self.setWindowTitle('TensorKart - Record')
        # self.setWindowIcon(QIcon('icon.png'))
        self.show()



    def recordClicked(self):
        print("Record Clicked!")


    def takeScreenshot(self):
        # take screenshot
        img = QScreen.grabWindow(QApplication.primaryScreen(), QApplication.desktop().winId(), 0, 0, 320, 240)
        self.lbl_image.setPixmap(img)


    def timerEvent(self, event):

        if event.timerId() == self.timer.timerId():

            self.takeScreenshot()

        else:
            super(MainWindow, self).timerEvent(event)


    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Attention', "Are you sure to quit?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())