### Hello =D ###
### How do you do ###

### Test ###

import numpy.random.common
import numpy.random.bounded_integers
import numpy.random.entropy

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import VCF_search_MainWindow
from VCF_search_MainWindow import Ui_MainWindow
import numpy as np
import pandas as pd
import vcf
import os
import allel
import sys

class mywindow(Ui_MainWindow, QWidget):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('VCF search')

        # Buttom setting
        self.pushButton_A.clicked.connect(self.search_POS)
        self.pushButton_D.clicked.connect(self.clear_POS)
        self.pushButton_RA.clicked.connect(self.search_RS)
        self.pushButton_RD.clicked.connect(self.clear_RS)
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit', "Do you want to Exit?", QMessageBox.Yes|QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore() 

    def search_POS(self):
        # read vcf file
        file_path = self.line_path.text()
        df = allel.read_vcf(file_path)
        Q = np.array(df['variants/QUAL'])
        ID = np.array(df['variants/ID'])
        REF = np.array(df['variants/REF'])
        ALT = np.array(df['variants/ALT'])
        F = np.array(df['variants/FILTER_PASS'])
        GT = np.array(df['calldata/GT'])
        Sample = ''.join((df['samples']))    # read sample name
        POS = np.array(df['variants/POS'])

        # search from chr & pos
        pos = int(self.line_pos.text())
        chrom = 'chr' + (self.line_chr.text())     
        result_pos = np.where(POS == pos)
        row = self.table.rowCount()
        self.table.setRowCount(row + 1)        
        self.table.setItem(row, 0, QTableWidgetItem(Sample))
        self.table.setItem(row, 1, QTableWidgetItem(chrom))
        self.table.setItem(row, 2, QTableWidgetItem(str(pos)))
        self.table.setItem(row, 3, QTableWidgetItem(str(ID[result_pos])))
        self.table.setItem(row, 4, QTableWidgetItem(str(REF[result_pos])))
        self.table.setItem(row, 5, QTableWidgetItem(str(ALT[result_pos])))
        self.table.setItem(row, 6, QTableWidgetItem(str(Q[result_pos])))
        self.table.setItem(row, 7, QTableWidgetItem(str(GT[result_pos])))
        self.table.setItem(row, 8, QTableWidgetItem(str(F[result_pos])))
        #self.table.item(row,1).setBackground(QtGui.QColor(125, 150, 150))

        #self.bt2.setEnabled(False)
        #if self.line_pos.text() > 0:      

    def search_RS(self):
        # read vcf file
        file_path = self.line_path.text()
        df = allel.read_vcf(file_path)
        Q = np.array(df['variants/QUAL'])
        CHROM = np.array(df['variants/CHROM'])
        POS = np.array(df['variants/POS'])
        REF = np.array(df['variants/REF'])
        ALT = np.array(df['variants/ALT'])
        F = np.array(df['variants/FILTER_PASS'])
        GT = np.array(df['calldata/GT'])
        Sample = ''.join((df['samples']))    # read sample name
        ID = np.array(df['variants/ID'])

        # search from rs_number
        rs = self.line_rs.text()
        result_rs = np.where(ID == rs)
        row = self.table.rowCount()
        self.table.setRowCount(row + 1)        
        self.table.setItem(row, 0, QTableWidgetItem(Sample))
        self.table.setItem(row, 1, QTableWidgetItem(str(CHROM[result_rs])))
        self.table.setItem(row, 3, QTableWidgetItem(rs))
        self.table.setItem(row, 2, QTableWidgetItem(str(POS[result_rs])))
        self.table.setItem(row, 4, QTableWidgetItem(str(REF[result_rs])))
        self.table.setItem(row, 5, QTableWidgetItem(str(ALT[result_rs])))
        self.table.setItem(row, 6, QTableWidgetItem(str(Q[result_rs])))
        self.table.setItem(row, 7, QTableWidgetItem(str(GT[result_rs])))
        self.table.setItem(row, 8, QTableWidgetItem(str(F[result_rs])))

    def clear_POS(self):
        self.line_pos.clear()
        self.line_chr.clear()

    def clear_RS(self):
        self.line_rs.clear()
        
    def msg(self):
        file_name, filetype = QFileDialog.getOpenFileName(self, "File import", "./", "vCard Files (*.vcf)")
        self.line_path.setText(file_name)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = mywindow()
    w.show()
    sys.exit(app.exec_())
