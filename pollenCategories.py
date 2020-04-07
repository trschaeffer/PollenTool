# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 10:33:15 2020

@author: Tobias
"""
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import PyQt5.QtWidgets as QtWidgets


class pollenCategories(QDialog):
    
    def __init__(self,newCategories):
        super().__init__()
        self.newCategories=newCategories
        self.initUI()
        
        
    def initUI(self):
        
        
           
        j=-1
        okButton = QPushButton("OK")
        

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        
        
        
        vbox=QVBoxLayout()
        
        listed = QListWidget()
        items=[]
        for i in range(len(self.newCategories)):
            
            
            items.append(QListWidgetItem(self.newCategories[i], listed))
            items[i].setFlags(items[i].flags() | Qt.ItemIsUserCheckable)
            items[i].setCheckState(Qt.Unchecked)
            
            
        
        vbox.addWidget(QLabel('Check boxes next to Pollen categories'))
        vbox.addWidget(listed)
        vbox.addWidget(okButton)
        
        self.setLayout(vbox)    
        
        self.setGeometry(300, 300, 400, 450)
        self.setWindowTitle('New Categories!')    
        self.show()
        
        def addP():
            for i in range(listed.count()):
                
                if(items[i].checkState()==2):
                    self.newCategories[i]=self.newCategories[i]+'(p)'
            self.accept()
        
            
        
        okButton.clicked.connect(addP)
    def closeEvent(self, event):
        print("dialog closed")
        self.accept()
        

def main(newCategories):
    ex = pollenCategories(newCategories)
    ex.show()
    if(ex.exec_()):
        print(ex.newCategories)
    
    
    
    
if __name__ == '__main__':
    main(['food','fuel'])