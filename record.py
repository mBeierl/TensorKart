#!/usr/bin/env python

# screenshot ref: http://doc.qt.io/qt-4.8/qt-desktop-screenshot-example.html

import sys
import os
import shutil

from datetime import datetime

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, \
    QApplication, QMessageBox, QLineEdit, QTextEdit
from PyQt5.QtGui import QIcon, QPixmap, QScreen, QGuiApplication
from PyQt5.QtCore import QBasicTimer

from utils import XboxController, take_screenshot

IDLE_SAMPLE_RATE = 1500
SAMPLE_RATE = 200

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.recording = False
        self.t = 0

        # Init controller
        self.controller = XboxController()

        # Create GUI
        self.initUI()

        # Timer
        self.timer = QBasicTimer()
        self.rate = SAMPLE_RATE
        self.idle_rate = IDLE_SAMPLE_RATE
        self.timer.start(self.idle_rate, self)


    def initUI(self):
        # Create Boxes
        hboxTop = QHBoxLayout()
        hboxBottom = QHBoxLayout()
        vbox = QVBoxLayout()

        # Create Elements
        self.recordButton = QPushButton("Record")
        self.recordButton.clicked.connect(self.on_btn_record)

        self.pathTxt = QLineEdit(self)
        uid = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.pathTxt.setText("samples/" + uid)

        image = QPixmap(320, 240)
        self.lbl_image = QLabel(self)
        self.lbl_image.setPixmap(image)

        self.controllerText = QTextEdit(self)
        self.controllerText.append("Controller input:")

        # Add Elements to Boxes
        hboxTop.addStretch(1)
        hboxTop.addWidget(self.lbl_image)
        hboxTop.addWidget(self.controllerText)

        hboxBottom.addWidget(self.recordButton)
        hboxBottom.addWidget(self.pathTxt)

        vbox.addStretch(1)
        vbox.addLayout(hboxTop)
        vbox.addLayout(hboxBottom)

        # Assign Layout
        self.setLayout(vbox)

        # Position Window, set Title & show
        self.setGeometry(0, 0, 660, 330)
        self.setWindowTitle('TensorKart - Record')
        # self.setWindowIcon(QIcon('icon.png'))
        self.show()


    def on_btn_record(self, event):

        # pause timer
        self.timer.Stop()

        # switch state
        self.recording = not self.recording

        if self.recording:
            self.start_recording()
            self.recordButton.setText("Stop Recording")
            self.timer.Start(self.rate)
        else:
            self.recordButton.setText("Record")
            self.timer.Start(self.idle_rate)
            

    def start_recording(self):

        # check that a dir has been specified
        if not self.pathTxt.text():

            msg = QMessageBox.warning(self, 'Error', 'Specify the Output Directory', QMessageBox.Ok)

            self.recording = False

        else:  # a directory was specified
            self.outputDir = self.pathTxt.text()
            self.t = 0

            # check if path exists - ie may be saving over data
            if os.path.exists(self.outputDir):

                result = QMessageBox.question(self, 'Attention', "Output Directory Exists - Overwrite Data?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                # overwrite the data
                if result == True:

                    # delete the dir
                    shutil.rmtree(self.outputDir)

                    # re-make dir
                    os.mkdir(self.outputDir)

                # do not overwrite the data
                else:  # result == False
                    self.recording = False
                    self.txt_outputDir.SetFocus()

            # no directory so make one
            else:
                os.mkdir(self.outputDir)


    def timerEvent(self, event):

        if event.timerId() == self.timer.timerId():

            self.poll()

        else:
            super(MainWindow, self).timerEvent(event)


    def poll(self):
        self.img = take_screenshot()
        self.controller_data = self.controller.read()
        #self.update_plot()

        if self.recording == True:
            self.save_data()
        else:
            self.lbl_image.setPixmap(self.img)
            str_controller_data = ' '.join(str(e) for e in self.controller_data)
            self.controllerText.append(str_controller_data)


    def save_data(self):
        print("Save Data!")
        image_file = self.outputDir + '/' + 'img_' + str(self.t) + '.png'

        self.img.save(image_file)

        # make / open outfile
        outfile = open(self.outputDir + '/' + 'data.csv', 'a')

        # write line
        outfile.write(image_file + ',' + ','.join(map(str, self.controller_data)) + '\n')
        outfile.close()

        self.t += 1


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