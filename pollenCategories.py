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
        #initialization
        super().__init__()
        self.newCategories=newCategories
        self.items=[]
        self.listed=QListWidget()
        self.removedCategories=[]
        #banned word could be adapted into a list if there were more
        #total categories, but for now a string is ok
        self.bannedWord='total pollen/day'
        self.initUI()
        
        
    def initUI(self):
        
        
           
        j=-1
        okButton = QPushButton("OK")
        

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        
          
        
        vbox=QVBoxLayout()
        mainhBox=QHBoxLayout()
        
        
        for i in range(len(self.newCategories)):
            
                
            #split the item by (p so that a (p) category can be differentiated by length
            #of the returned list as well as be printed without the (p) using its first element
            self.newCategories[i]=self.newCategories[i].split('(p')
            #create items in a list
            self.items.append(QListWidgetItem(self.newCategories[i][0], self.listed))
            #make the items checkable
            self.items[i].setFlags(self.items[i].flags() | Qt.ItemIsUserCheckable)
            #if the category had a (p) in it, make it checked, otherwise unchecked
            if len(self.newCategories[i])>1:
                self.items[i].setCheckState(Qt.Checked)
            else: 
                self.items[i].setCheckState(Qt.Unchecked)
            
        #arranging the buttons
        vbox.addWidget(QLabel('Check boxes next to Pollen categories'))
        vbox.addWidget(self.listed)
        vbox.addWidget(okButton)
        
        self.setLayout(vbox)    
        
        self.setGeometry(300, 300, 400, 450)
        self.setWindowTitle('Pollen Category selector')    
        self.show()
        #ALL CODE ADDED TO addP SHOULD ALSO BE ADDED TO closeEvent
        def addP():
            #when ok is clicked, check if each box is checked
            for i in range(self.listed.count()):
                #if the box is checked and not the banned word, add a (p) to the string
                if(self.items[i].checkState()==2):
                    minlen=min(len(self.bannedWord),len(self.newCategories[i][0]))
                    if self.bannedWord[0:minlen]!=self.newCategories[i][0][0:minlen].lower():
                        self.newCategories[i]=self.newCategories[i][0]+'(p)'
                    else:
                        #if the category's name is the banned word, do not make it a
                        #pollen category.  This is done to prevent recursively
                        #summing total pollen into total pollen
                        self.newCategories[i]=self.newCategories[i][0]
                else:
                    self.newCategories[i]=self.newCategories[i][0]
            #accept closes the dialogue box and returns a true value, allowing
            #the program to proceed
            self.accept()
        
            
        
        okButton.clicked.connect(addP)
    def closeEvent(self, event):
        #this is the same as addP(), but occurs when the x button is clicked
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
        
#tester main
def main(newCategories):
    ex = pollenCategories(newCategories)
    ex.show()
    if(ex.exec_()):
        print(ex.newCategories)
    
    
    
    
if __name__ == '__main__':
    main(['fOod(p)','fuel','total poLLen(p)','hello','test'])