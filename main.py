####Ariana Escobar Chalen
####10131324

import sys
import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget
from PyQt5.QtWidgets import QPushButton
import numpy as np
import numpy

#####GUI#####
class App(QWidget):
    def __init__(self):
        super().__init__()

        self.title='FIR Filter'
        self.left=700
        self.top=400
        self.width=400
        self.height=200
        self.initUI()
        self.Header=np.array([])
        self.fileName = 0
        self.coeffName = 0
        self.yout = 0

####buttons
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top,self.width,self.height)
        open_wav=QPushButton('Open WAV File', self)
        open_wav.move(10,10)
        open_wav.clicked.connect(self.on_click_file)

        import_fir = QPushButton('Import FIR Coefficients', self)
        import_fir.move(10, 100)
        import_fir.clicked.connect(self.on_click_coeff)

        filter_wav = QPushButton('Filter WAV File', self)
        filter_wav.move(200, 10)
        filter_wav.clicked.connect(self.filter)

        save_wav = QPushButton('Save Filtered WAV File', self)
        save_wav.move(200, 100)
        save_wav.clicked.connect(self.save_filter)
        self.show()

    @pyqtSlot()
    def on_click_file(self):
        self.openFileNameDialog()

    def on_click_coeff(self):
        self.openCoeff()

####Open dialog to get files
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if self.fileName:
            print(self.fileName)

####Open dialog to get files
    def openCoeff(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.coeffName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if self.coeffName:
            print(self.coeffName)

    def readWav(self):
        self.fileName

    def readCoeff(self):
        self.coeffName
####Filter FIR
    def filter(self):
        binarySound = {}
        binaryHeader = {}
        print ("filtering")
        with open(self.fileName, 'rb') as f:
            buffer = f.read(44)
            self.Header = numpy.frombuffer(buffer, dtype=numpy.int16)
            buffer = f.read()
            binarySound = numpy.frombuffer(buffer, dtype=numpy.int16)

        f = open(self.coeffName, "r")
        coeff = []
        for line in f:
            line = float(line.split('\\')[0])
            coeff.append(line)

        coeff = np.array(coeff)

        binarySound = np.concatenate([binarySound, np.zeros(len(coeff) - 1)])
        y = np.zeros(len(binarySound))

        for n in range(0, len(binarySound)):
            y[n] = 0
            for k in range(0, (len(coeff))):
                y[n] = y[n] + coeff[k] * binarySound[n - k]

        out = y[0:(len(binarySound) - len(coeff) + 1)]

        self.yout = np.array(list(map(np.int16, out)))

####Save WAV
    def save_filter(self):
        song={}
        with open("new.wav", "wb") as f:
            song = np.concatenate([self.Header, self.yout])
            f.write(song)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())








