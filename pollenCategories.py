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
        self.items=[]
        self.listed=QListWidget()
        self.removedCategories=[]
        self.bannedWord='total pollen/day'
        self.initUI()
        
        
    def initUI(self):
        
        
           
        j=-1
        okButton = QPushButton("OK")
        

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        
          
        
        vbox=QVBoxLayout()
        
        
        
        for i in range(len(self.newCategories)):
            
                
            
            self.newCategories[i]=self.newCategories[i].lower().split('(p')
            self.items.append(QListWidgetItem(self.newCategories[i][0], self.listed))
            
            self.items[i].setFlags(self.items[i].flags() | Qt.ItemIsUserCheckable)
            
            if len(self.newCategories[i])>1:
                self.items[i].setCheckState(Qt.Checked)
            else: 
                self.items[i].setCheckState(Qt.Unchecked)
            
        
        vbox.addWidget(QLabel('Check boxes next to Pollen categories'))
        vbox.addWidget(self.listed)
        vbox.addWidget(okButton)
        
        self.setLayout(vbox)    
        
        self.setGeometry(300, 300, 400, 450)
        self.setWindowTitle('New Categories!')    
        self.show()
        
        def addP():
            for i in range(self.listed.count()):
                
                if(self.items[i].checkState()==2):
                    minlen=min(len(self.bannedWord),len(self.newCategories[i][0]))
                    if self.bannedWord[0:minlen]!=self.newCategories[i][0][0:minlen].lower():
                        self.newCategories[i]=self.newCategories[i][0]+'(p)'
                    else:
                        self.newCategories[i]=self.newCategories[i][0]
                else:
                    self.newCategories[i]=self.newCategories[i][0]
            self.accept()
        
            
        
        okButton.clicked.connect(addP)
    def closeEvent(self, event):
        for i in range(self.listed.count()):
                
            if(self.items[i].checkState()==2):
                minlen=min(len(self.bannedWord),len(self.newCategories[i][0]))
                if self.bannedWord[0:minlen]!=self.newCategories[i][0][0:minlen].lower():
                    self.newCategories[i]=self.newCategories[i][0]+'(p)'
                else:
                    self.newCategories[i]=self.newCategories[i][0]
            else:
                self.newCategories[i]=self.newCategories[i][0]
        print("dialog closed")
        self.accept()
        

def main(newCategories):
    ex = pollenCategories(newCategories)
    ex.show()
    if(ex.exec_()):
        print(ex.newCategories)
    
    
    
    
if __name__ == '__main__':
    main(['fOod(p)','fuel','total poLLen(p)','hello','test'])