# -*- coding: utf-8 -*-
"""
Created on Tue May 29 09:11:29 2018

@author: JessicaKelly
"""

#from IPython import get_ipython
#get_ipython().magic('reset -sf')  # Clear all variables

#imports for the packager
#import pkg_resources.py2_warn
import sklearn.neighbors.typedefs
import sklearn.neighbors.quad_tree
import sklearn.tree
import sklearn.tree._utils
from sklearn.utils import *
import PyQt5.QtWidgets as QtWidgets

#imports for program


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import os
import os.path
import xlwings as xw
import openpyxl
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
import exampleReadFromExcel as RFE
import exampleplots as explots
import spearmanExample as sp
from pollenCategories import pollenCategories
#import gmail


class tabs(QTabWidget):
    
    def __init__(self, parent=None):
        #Creates general GUI layout with tabs
        super(tabs, self).__init__(parent)
        
        self.tab1 = QWidget()
        self.addTab(self.tab1, "Data Entry")
        self.tab1UI()
        
        self.tab2 = QWidget()
        self.addTab(self.tab2, "Calculations")
        self.tab2UI()
        
        self.tab3 = QWidget()
        self.addTab(self.tab3, "Generate Graphs")
        self.tab3UI()
        
        self.tab4 = QWidget()
        self.addTab(self.tab4, "Help")
        self.tab4UI()
        
        #Titles the window
        self.setWindowTitle("The Correlation Machine- Copyright WPI, 2020")
        self.setGeometry(100, 100, 775 ,600)
        
    #creates error box to prevent the user from crashing the program
    #msg is sent to them
    def throwError(self,msg):
        error_dialog = QtWidgets.QErrorMessage()
        error_dialog.showMessage(msg)
        error_dialog.exec_()
        
    def tab1UI(self):                
        #Create buttons and fields
        browse_btn = QPushButton("Browse Files")
        load_btn = QPushButton("Load Master")
        self.masterFileName='master.xlsx'
        #horizontally align buttons
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel("<b>Select data file to import:</b>"))
        hbox1.addWidget(browse_btn)
        hbox1.addWidget(load_btn)
        
        #Show status of data entry
        self.file_name = QLabel('<u>No data has been loaded</u>')
        
        #Create input fields
        self.input_date = QLineEdit('mm/dd/year')
        self.data_pt = QLineEdit('Data value')
        
        #creates dropdown menu for categories
        self.cbox = QComboBox()
        
        #align buttons and input fields for manual data entry
        labelDE = QLabel('<b>Manual Data Point Entry</b>')
        labelDE.setAlignment(Qt.AlignCenter)
        formDE = QFormLayout()
        formDE.addRow('Category (Ex: temperature)', self.cbox)
        formDE.addRow('Date (mm/dd/year)', self.input_date)
        formDE.addRow('Data value (Ex: 10)', self.data_pt)
        formDE.setLabelAlignment(Qt.AlignJustify)
        
        #Create a button to add point to data file
        add_btn = QPushButton("Add Data Point to File")
        
        #Create textboox to present new data
        new_data = QTextEdit('')
        
        #Create buttons to publish data
        sum_btn = QPushButton('Calculate Total Pollen/day')
        polleninfo_btn = QPushButton('View/edit Pollen categories')
        hbox3 = QHBoxLayout()
        hbox3.addWidget(sum_btn)
        hbox3.addWidget(polleninfo_btn)
        
        #sets overall layout for the tab
        vbox = QVBoxLayout(self)
        vbox.addLayout(hbox1)
        vbox.addWidget(self.file_name)
        vbox.addStretch(2)
        vbox.addWidget(labelDE)
        vbox.addLayout(formDE)
        vbox.addWidget(add_btn)
        vbox.addStretch(2)
        vbox.addWidget(QLabel('<b>New Data Added:</b>'))
        vbox.addWidget(new_data)
        vbox.addLayout(hbox3)
        self.tab1.setLayout(vbox)

        #Browse user's computer for excel files
        def openFileNameDialog():
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            new_data.setText("loading data...")
            file, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Excel (*.xlsx)")
            
            #if the user does not select a file, catch error to prevent crashing
            try:
                #update user status of data imported
                self.file_name.setText('File imported: ' + extractName(file))

                #read in the data from the imported file
                ws = RFE.readFile(file)
                raw_data = RFE.toList(ws,RFE.findOrientation(ws),True)
                self.data = RFE.filter(raw_data[0], raw_data[1], raw_data[2])
                filterText="\nFilter Report\n\n"+self.data[3]
                new_data.setText(filterText+"\n Please See other window to continue")
                
                #Update master file and "new data added" box
                if extractName(file) != 'master.xlsx': 
                    mergetext=RFE.toMainSpreadSheet(self.data[0], self.data[1].copy(),self.data[2],self.masterFileName)
                    new_data.setText("Merge Report \n\n"+mergetext+filterText)
              
                self.data=RFE.loadData(self.masterFileName) #read in master
                updateCategories() #add categories to drop-down menus
            except:
                self.throwError("Error: No File Selected")
                print(sys.exc_info()[0])
            
        def extractName(file):
            #separates the name of the file from its directory
            directory=file.split('/')
            name=directory[-1]
            return name
        
        def updateCategories():
            #Adds headers for data categories to all dropdown menus
            categories = self.data[0]
            for x in [self.cbox, self.cat1, self.cat2, self.c1,self.c2,self.c3,self.c4,self.c5,self.c6]:
                x.clear()
                for y in categories:
                    x.addItem(y)
                    
        def setPollenCategories():
            #allows user to access the checkboxes for which categories are pollen type
            #maybe we should run sum_pollen after this one
            categories=RFE.loadDataWithP("master.xlsx")[0]
            try:
                self.data[0]==[]
                1/len(categories)
            except:
                self.throwError('Master file has not been loaded. Click "load master" or "browse files" to load master file')
                
            else:
                ex = pollenCategories(categories)
                ex.show()
                if(ex.exec_()):
                    new_data.setText("Categories updated. summing pollen.")
                    RFE.rewriteCategories(ex.newCategories,'master.xlsx')

                new_data.setText("Categories updated")
                sum_pollen()

        def load():
            #read in master file when "load master" is clicked
            self.data=RFE.loadData(self.masterFileName)
            if self.data[0] != []:
                updateCategories() #update dropdown menus
                self.file_name.setText('File loaded: master.xlsx')
            else:
                self.throwError('Master file has not been created. Click "Browse Files" and select a data file')
            
        def sum_pollen():
            #adds all pollen types together into one category, total pollen
            try:
                report=RFE.calcTotalPollen('master.xlsx')
                new_data.setText(report)
                load()
            except:
                self.throwError('Master file has not been loaded. Click "load master" or "browse files" to load master file')


        def send_email():
            #get today's data, email it.  Not implemented
            #able to send gmails with .xlsx attachments, but not doing anything useful
            #currently
            
            #some function to filter by today's date
            #RFE.toNewSpreadSheet(categories, data, dates, filename)
            #gmail.send_message_from_GUI("trschaeffer@wpi.edu", "Subject", "Hello! here is the pollen data for today",filename)
            pass
        
        def add_datapoint():
            #adds data point to master file using toMainSpreadSheet in readFromExcel
            try:
                data_pt=self.data_pt.text()
                data_pt=int(data_pt)
                if self.cbox.currentText() != '':
                    cat=self.cbox.currentText()
                
                input_date=self.input_date.text().split('/')
                input_date=date(int(input_date[2]), int(input_date[0]), int(input_date[1]))
                new_data.setText(RFE.toMainSpreadSheet([cat], [[data_pt]], [input_date], self.masterFileName))
            except:
                self.throwError('Input is invalid. Category cannot be empty. <br>' 
                        + 'Data value must be a number. Date must be in mm/dd/year format. <br>'
                        + 'If date is only a month, use mm/1/year<br>(Ex: March 2020 should be 3/1/2020)')
                
        # Assigns functions to buttons
        browse_btn.clicked.connect(openFileNameDialog)
        load_btn.clicked.connect(load)
        add_btn.clicked.connect(add_datapoint)
        polleninfo_btn.clicked.connect(setPollenCategories)
        sum_btn.clicked.connect(sum_pollen)


    def tab2UI(self):        
        #Create and format dropdown menu for categories to correlate
        self.cat1 = QComboBox()
        self.cat2 = QComboBox()
        hbox0 = QHBoxLayout()
        hbox0.addWidget(QLabel('<b>Find Correlation Between:</b>'))
        hbox0.addWidget(self.cat1)
        hbox0.addWidget(QLabel('         and'))
        hbox0.addWidget(self.cat2)
        
        seasonbox = QHBoxLayout()
        seasonbox.addWidget(QLabel('Enter the pollen season dates:'))
        seasonS = QLineEdit('mm/dd')
        seasonbox.addWidget(seasonS)
        seasonbox.addWidget(QLabel('to'))
        seasonE = QLineEdit('mm/dd')
        seasonbox.addWidget(seasonE)
        
        #Create options to calculate average of year or month
        averagesbox = QComboBox()
        averagesbox.addItem('None')
        averagesbox.addItem('Years')
        averagesbox.addItem('Months')
        hboxA = QHBoxLayout()
        hboxA.addWidget(QLabel('Calculate averages in the data across'))
        hboxA.addWidget(averagesbox)
        
        #Create options to select time period of data to correlate
        hboxdates = QHBoxLayout()
        datecheck = QCheckBox('Include data between the dates:')
        hboxdates.addWidget(datecheck)
        date1 = QLineEdit('mm/dd/year')
        hboxdates.addWidget(date1)
        hboxdates.addWidget(QLabel('and'))
        date2 = QLineEdit('mm/dd/year')
        hboxdates.addWidget(date2)
        
        #Creates button to calculate correlation
        calc_form = QFormLayout()
        calc_btn = QPushButton('Calculate')
        calc_form.addRow("<b>Calculate Spearman's Correlation Coefficient</b>", calc_btn)
        
        #Creates options to save results
        saveHbox = QHBoxLayout()
        saveHbox.addWidget(QLabel("<b>Save results from the table above as the file name:</b>"))
        self.saveFileName = QLineEdit('')
        saveHbox.addWidget(self.saveFileName)
        saveHbox.addWidget(QLabel('.xlsx'))
        save_btn = QPushButton('Save to Excel')
        
        #Creates table to publish correlation results
        self.cor_results = QTableWidget(1,8)
        self.cor_results.setItem(0,0,QTableWidgetItem('Correlation'))
        self.cor_results.setItem(0,1,QTableWidgetItem('p-value'))
        self.cor_results.setItem(0,2,QTableWidgetItem('Category 1'))
        self.cor_results.setItem(0,3,QTableWidgetItem('Category 2'))
        self.cor_results.setItem(0,4,QTableWidgetItem('Season'))
        self.cor_results.setItem(0,5,QTableWidgetItem('Start date'))
        self.cor_results.setItem(0,6,QTableWidgetItem('End date'))
        self.cor_results.setItem(0,7,QTableWidgetItem('Averages'))
    
        #sets the overall layout for the tab
        vbox1 = QVBoxLayout(self)
        vbox1.addLayout(hbox0)
        vbox1.addStretch(0)
        vbox1.addLayout(seasonbox)
        vbox1.addStretch(3)
        vbox1.addWidget(QLabel('<b>Optional Data Analysis Settings:</b>'))
        vbox1.addStretch(0)
        vbox1.addLayout(hboxA)
        vbox1.addStretch(0)
        vbox1.addWidget(datecheck)
        vbox1.addLayout(hboxdates)
        vbox1.addStretch(3)
        vbox1.addLayout(calc_form)
        vbox1.addWidget(QLabel('<b>Correlation Results</b>'))
        vbox1.addWidget(self.cor_results)
        vbox1.addLayout(saveHbox)
        vbox1.addWidget(save_btn)
        self.tab2.setLayout(vbox1)
        
        def calculate():
            #Calculate correlation based on parameters entered by the user
            try:
                #Find categories
                if self.cat1.currentText() != '' and self.cat2.currentText() != '':
                    cat1_name = self.cat1.currentText()
                    cat2_name = self.cat2.currentText()
                dates = self.data[2]
                #print(self.data[0])
            
                i=0
                #Extract all data from the categories specified by the user
                for a in self.data[0]:
                    if a==cat1_name:
                        raw_xdata = self.data[1][i]
                    if a==cat2_name:
                        raw_ydata = self.data[1][i]
                    i+=1
            except:
                self.throwError('No data selected. Go to the "Data Entry" tab '
                                + 'and either "Browse Files" and select a data file '
                                + 'or "Load Master"')
                return None
                
            #If the user chooses to include only certain range of dates
            # filter the data by these dates using dateFilter
            if datecheck.isChecked() == True:
                try:
                    raw_xdata, raw_ydata, dates = dateFilter(raw_xdata, raw_ydata, dates, 'specific')
                except:
                    self.throwError('Invalid dates entered. Dates must be in mm/dd/year format.'
                                + ' Example: 1/1/2014 - 12/31/2019 will give all data from 2014-2019.')
                    return None
            
            if seasonS.text() != 'mm/dd' and seasonS.text() != '' and seasonE.text() != 'mm/dd' and seasonE.text() != '':
                try:
                    raw_xdata, raw_ydata, dates = dateFilter(raw_xdata, raw_ydata, dates, 'season')
                    #print (seasonS.text(), seasonE.text())
                except:
                    print("Invalid season entered. Dates must be in mm/dd form.")
                
            #If the user selects to calculate yearly or monthly averages
            # return x and y data in the form of averages using calculateAverages
            if averagesbox.currentText() != 'None':
                xdata, ydata = calculateAverages(raw_xdata, raw_ydata, dates, averagesbox.currentText())
            
            #If user does not choose to use optional data filtering, use raw data for calculations
            else:
                xdata=raw_xdata
                ydata=raw_ydata
                    
            #print(xdata, ydata)
            
            #Calculate spearman's correlation
            r,p = sp.calculatecoefficients(np.array(xdata), np.array(ydata))
            
            #Color code correlation and p-value based on strength
            rText = QTableWidgetItem(str(round(r, 3)))
            if r >= 0.4 or r <= -0.4:
                rText.setForeground(QBrush(QColor(0, 255, 0)))
            else:
                rText.setForeground(QBrush(QColor(255, 99, 71)))
                
            pText = QTableWidgetItem(str(round(p, 6)))
            if p <= 0.05:
                pText.setForeground(QBrush(QColor(0, 255, 0)))
            else:
                pText.setForeground(QBrush(QColor(255, 99, 71)))
            
            #print results to the UI table
            self.cor_results.insertRow(1)
            self.cor_results.setItem(1, 0, rText)
            self.cor_results.setItem(1, 1, pText)
            self.cor_results.setItem(1, 2, QTableWidgetItem(cat1_name))
            self.cor_results.setItem(1, 3, QTableWidgetItem(cat2_name))
            if seasonS.text() != 'mm/dd' and seasonE.text() != 'mm/dd':
                season = seasonS.text() + ' - ' + seasonE.text()
                self.cor_results.setItem(1, 4, QTableWidgetItem(season))
            if datecheck.isChecked() == True:
                self.cor_results.setItem(1, 5, QTableWidgetItem(date1.text()))
                self.cor_results.setItem(1, 6, QTableWidgetItem(date2.text()))
            if averagesbox.currentText() != 'None':
                self.cor_results.setItem(1, 7, QTableWidgetItem(averagesbox.currentText()))
            
        def calculateAverages(raw_xdata, raw_ydata, dates, way):
            #calculate monthly or yearly averages based on user input
            i=0
            prevd=0
            listxdates=[]
            listydates=[]
            xdata=[]
            ydata=[]
            
            #Extract year or month from each date, depending on what user selects
            for x in dates:
                if way == 'Years':
                    d=x.year
                elif way == 'Months':
                    d=x.month
                
                #if the year/month matches that of the previous datapoint
                # add to data list, as long as values exist for that day for both categories
                if d == prevd:
                    if raw_xdata[i] != None:
                        listxdates.append(raw_xdata[i])
                    if raw_ydata[i] != None:
                        listydates.append(raw_ydata[i])
                #if the year/month does not match that of previous datapoint
                # marks the start of a new year/month
                if d != prevd:
                    if prevd != 0:
                        # calculate average for the previous year/month and add to list
                        # or add none if there is no data for that time period
                        if len(listxdates) != 0:
                            xdata.append(avg(listxdates))
                        else:
                            xdata.append(None)
                        
                        if len(listydates) != 0:
                            ydata.append(avg(listydates))
                        else:
                            ydata.append(None)
                    
                    #reset indexed date and lists to include most recent datapoint only
                    if raw_xdata[i] != None:
                        listxdates=[raw_xdata[i]]
                    else:
                        listxdates=[]
                        
                    if raw_ydata[i] != None:
                        listydates=[raw_ydata[i]]
                    else:
                        listydates=[]
                    prevd=d
                i+=1
            
            #include average for the last time period once end of loop is reached
            if len(listxdates) != 0:
                xdata.append(avg(listxdates))
            else:
                xdata.append(None)
                        
            if len(listydates) != 0:
                ydata.append(avg(listydates))
            else:
                ydata.append(None)
                
            return xdata, ydata
                
        def avg(datalist):
            #helper function for calculating averages
            sumData=0
            size=len(datalist)
            for x in datalist:
                if x != None:
                    sumData+=x
                else:
                    size = size - 1
            average=sumData/size
            return average
        
        def dateFilter(raw_xdata, raw_ydata, raw_dates, way):
            #Filter data by the date range entered by the user
            if way == 'specific':
                if date1.text() != '' and date2.text() != '':
                    #Extract the dates from user input field and make datetime.date format
                    start_date = date1.text().split('/')
                    start_date = date(int(start_date[2]), int(start_date[0]), int(start_date[1]))
                    end_date = date2.text().split('/')
                    end_date = date(int(end_date[2]), int(end_date[0]), int(end_date[1]))
            
            xdata=[]
            ydata=[]
            dates=[]
            #return data only within the desired range of dates
            for t in range(len(raw_dates)):
                if way == 'season':
                    start_date = seasonS.text().split('/')
                    start_date = date(raw_dates[t].year, int(start_date[0]), int(start_date[1]))
                    end_date = seasonE.text().split('/')
                    end_date = date(raw_dates[t].year, int(end_date[0]), int(end_date[1]))
                    
                if raw_dates[t] >= start_date and raw_dates[t] <= end_date:
                    xdata.append(raw_xdata[t])
                    ydata.append(raw_ydata[t])
                    dates.append(raw_dates[t])
            return xdata, ydata, dates
        
        def saveResults():
            #save all results from the table in the correlation tab to Excel
            headings=[]
            dates=[]
            datas=[]
            for i in range (self.cor_results.columnCount()):
                headings.append(self.cor_results.item(0,i).text())
                data=[]
                for x in range (1, self.cor_results.rowCount()):
                    if self.cor_results.item(x,i) != None:
                        data.append(self.cor_results.item(x,i).text())
                    else:
                        data.append(None)
                datas.append(data)
            for d in range (1, self.cor_results.rowCount()):
                dates.append(d)
            try:
                #use toNewSpreadSheet to write data to Excel and save as name specified
                RFE.toNewSpreadSheet(headings, datas, dates, self.saveFileName.text() + '.xlsx')
                self.throwError('File ' + self.saveFileName.text() + '.xlsx has been successfully saved to the "PollenTool" folder.')
            except:
                self.throwError('File name cannot contain "." or "/"')
        
        #assign function to calculate button
        calc_btn.clicked.connect(calculate)
        save_btn.clicked.connect(saveResults)

        
    def tab3UI(self):
        #Dropdown menu for graph x-variable
        self.c1=QComboBox()
        self.c2=QComboBox()
        self.c3=QComboBox()
        self.c4=QComboBox()
        self.c5=QComboBox()
        self.c6=QComboBox()
        cArr=[self.c1,self.c2,self.c3,self.c4,self.c5,self.c6]
       
         #Create fields for category options
        self.numBox=QComboBox()
        for i in range(1,7):
            self.numBox.addItem(str(i))
        HBoxIterate=[]
        axisNum=[]
        regressionType=[]
        for i in range(0, 6):  #Poplulate dropdown menus
            regressionType.append(QComboBox())
            axisNum.append(QComboBox())
            regressionType[i].addItem('None')
            regressionType[i].addItem('Linear')
            regressionType[i].addItem('Polynomial')
            regressionType[i].addItem('LOESS')
            axisNum[i].addItem('Left')
            axisNum[i].addItem('Right')
        vboxIterate=QVBoxLayout()
        hboxT=QHBoxLayout()
        hboxT.addWidget(QLabel('<b># of Categories to Graph:</b>'))
        create_spaces = QPushButton('Generate Category Options')
        update_spaces = QPushButton('Update Category #')
        hboxT.addWidget(self.numBox)
        hboxT.addWidget(create_spaces)
        
        seasonbox = QHBoxLayout()
        seasonbox.addWidget(QLabel('Enter the pollen season dates:'))
        seasonS = QLineEdit('mm/dd')
        seasonbox.addWidget(seasonS)
        seasonbox.addWidget(QLabel('to'))
        seasonE = QLineEdit('mm/dd')
        seasonbox.addWidget(seasonE)
        
        #Create options to calculate average of year or month
        averagesbox = QComboBox()
        averagesbox.addItem('None')
        averagesbox.addItem('Years')
        averagesbox.addItem('Months')
        hboxA = QHBoxLayout()
        hboxA.addWidget(QLabel('Calculate averages in the data across'))
        hboxA.addWidget(averagesbox)
        
        #Creates fields to enter dates
        #datecheck = QCheckBox('Filter data by the dates entered below')
        hboxDates = QHBoxLayout()
        datecheck = QCheckBox('Include data between the dates:')
        hboxDates.addWidget(datecheck)
        date1 = QLineEdit('mm/dd/year')
        hboxDates.addWidget(date1)
        hboxDates.addWidget(QLabel('and'))
        date2 = QLineEdit('mm/dd/year')
        hboxDates.addWidget(date2)
        
        #future prediction panel
        hboxFuture = QHBoxLayout()
        futurecheck = QCheckBox('Show Regression to year:')
        hboxFuture.addWidget(futurecheck)
        futureYear = QLineEdit('yyyy')
        hboxFuture.addWidget(futureYear)
        
        #Dropdown menu for selecting type of graph
        graph_form = QFormLayout()
        graphtype = QComboBox()
        graphtype.addItem('Scatterplot')
        graphtype.addItem('Boxplot')
        graph_form.addRow('<b>Graph Style:</b>', graphtype)
        hboxGraphType = QHBoxLayout()
        hboxGraphType.addLayout(graph_form)
        
        #Create graphing buttons
        generate_btn = QPushButton('Generate Graph')
        hboxGenerate = QHBoxLayout()
        hboxGenerate.addWidget(generate_btn)
        
        #sets the overall layout for the tab
        vbox1 = QVBoxLayout(self)
        vbox1.addLayout(hboxT)
        vbox1.addLayout(vboxIterate)
        vbox1.addStretch(2)
        vbox1.addLayout(hboxGraphType)
        vbox1.addStretch(3)
        vbox1.addWidget(QLabel('<b>Optional Data Analysis Settings:</b>'))
        vbox1.addStretch(0)
        vbox1.addLayout(seasonbox)
        vbox1.addStretch(0)
        vbox1.addLayout(hboxA)
        vbox1.addStretch(0)
        vbox1.addWidget(datecheck)
        vbox1.addLayout(hboxDates)
        vbox1.addLayout(hboxFuture)
        vbox1.addStretch(3)
        vbox1.addLayout(hboxGenerate)
        self.tab3.setLayout(vbox1)
        
        #the user inputs the number of slots they want to create, this will
        #graph them
        def createSlots():
            for i in range(0,7):
                    HBoxIterate.append(QHBoxLayout())
                    if i<int(self.numBox.currentText()):
                        HBoxIterate[i].addWidget(QLabel('Category:'))
                        HBoxIterate[i].addWidget(cArr[i])
                        HBoxIterate[i].addWidget(QLabel('       Read Scale from Axis:'))
                        HBoxIterate[i].addWidget(axisNum[i])
                        HBoxIterate[i].addWidget(QLabel('           Regression:'))
                        HBoxIterate[i].addWidget(regressionType[i])
                        vboxIterate.addLayout(HBoxIterate[i])
                
            create_spaces.setParent(None)
            hboxT.addWidget(update_spaces)
            
        #called after create slots, deletes old slots and makes new ones 
        def updateSlots():
            for layout in HBoxIterate:
                for i in reversed(range(layout.count())): 
                    layout.itemAt(i).widget().setParent(None)
                    
            for i in range(0,int(self.numBox.currentText())):
                HBoxIterate[i].addWidget(QLabel('Category:'))
                HBoxIterate[i].addWidget(cArr[i])
                HBoxIterate[i].addWidget(QLabel('       Read Scale from Axis:'))
                HBoxIterate[i].addWidget(axisNum[i])
                HBoxIterate[i].addWidget(QLabel('           Regression:'))
                HBoxIterate[i].addWidget(regressionType[i])
                vboxIterate.addLayout(HBoxIterate[i])     
                    
        def graph():            
            #Find the categories specified by the user and extract the data
            cats=[]
            for i in range(0,int(self.numBox.currentText())):
                cats.append(cArr[i].currentText())
            
            try:
                dates=self.data[2]
            except:
                self.throwError('No data entered into the tool. Return to the Data Entry tab '
                                + 'and either "Browse Files" or "Load Master".')
                return None
            
            i=0
            raw_arr=[]
            for j in range(len(cats)):
                for i in range(len(self.data[0])):
                
                    if self.data[0][i]==cats[j]:
                        
                        raw_arr.append(self.data[1][i])
                        break
                    
            regressions=[]
            axies=[]
            #fill regressions array with what the user put in the boxes
            for i in range(len(cats)):
                regressions.append(regressionType[i].currentText())
                axies.append(axisNum[i].currentText())
            datesArr=[dates]*len(raw_arr)
            arr=[None]*len(raw_arr)
            
            #the user may want to make future predictions to a certain year
            if(futurecheck.isChecked()==True):
                try:
                    future=int(futureYear.text())
                except:
                    self.throwError('Year must be a number, such as 2030')
                    return None
            else:
                future=-1
            
            #If the user chooses to include only certain range of dates
            # filter the data by these dates using dateFilter
            if datecheck.isChecked() == True:
                try:
                    for i in range(len(raw_arr)):
                        raw_arr[i], datesArr[i] = dateFilter(raw_arr[i], datesArr[i], 'specific')
                except:
                    self.throwError('Invalid dates entered. Dates must be in mm/dd/year format.'
                                + ' Example: 1/1/2014 - 12/31/2019 will give all data from 2014-2019.')
                    return None
                
            if seasonS.text() != 'mm/dd' and seasonS.text() != '' and seasonE.text() != 'mm/dd' and seasonE.text() != '':
                try:
                    for i in range(len(raw_arr)):
                        raw_arr[i], datesArr[i] = dateFilter(raw_arr[i], datesArr[i], 'season')
                        #print (seasonS.text(), seasonE.text())
                except:
                    print("Invalid season entered. Dates must be in mm/dd form.")
                    
            #If the user selects to calculate yearly or monthly averages
            # return x and y data in the form of averages using calculateAverages
            if averagesbox.currentText() != 'None':
                for i in range(len(raw_arr)):
                    arr[i], datesArr[i] = calculateAverages(raw_arr[i], datesArr[i], averagesbox.currentText())
                    cats[i]=cats[i]+(' ')+averagesbox.currentText()[:-1]+' Avg'  
            
            #If user does not choose to use optional data filtering, use raw data for calculations
            else:
                arr=raw_arr
            
            #graph type indicated by the user
            if graphtype.currentText() == 'Scatterplot':
                explots.arrayvstime2(arr,datesArr,cats,regressions,axies,future)
            if graphtype.currentText() == 'Boxplot':
                explots.boxplot(arr,datesArr,cats,regressions,axies,future)
                
                
        def calculateAverages(raw_data, raw_dates, way):
            i=0
            prevd=0
            listdates=[]
            data=[]
            dates=[]
            
            #Extract year or month from each date, depending on what user selects
            for x in raw_dates:
                if way == 'Years':
                    d=[x.year]
                elif way == 'Months':
                    d=[x.year,x.month]
                
                #if the year/month matches that of the previous datapoint
                # add to data list
                if d == prevd:
                    if raw_data[i] != None:
                        listdates.append(raw_data[i])
                        #print("listDates:")
                        #print (listdates)
                        
                #if the year/month does not match that of previous datapoint
                # marks the start of a new year/month
                if d != prevd:
                    if way=='Years':
                        dates.append(date(d[0],1,1))
                    if way=='Months':
                        dates.append(date(d[0],d[1],1))
                   
                    if prevd != 0:
                        # calculate average for the previous year/month and add to list
                        # or add none if there is no data for that time period
                        if len(listdates) != 0:
                            data.append(avg(listdates))
                        else:
                            data.append(None)
                    
                    #reset indexed date and lists to include most recent datapoint only
                    if raw_data[i] != None:
                        listdates=[raw_data[i]]
                    else:
                        listdates=[]
                        
                    prevd=d
                i+=1 
            
            #include average for the last time period once end of loop is reached
            if len(listdates) != 0:
                data.append(avg(listdates))
            else:
                data.append(None)
                        
            #print(data, dates)
            return data, dates
        
        def avg(datalist):
            #helper function to calculate averages
            sumData=0
            size=len(datalist)
            for x in datalist:
                if x != None:
                    sumData+=x
                else:
                    size = size - 1
            average=sumData/size
            return average
        
        
        def dateFilter(raw_data, raw_dates, way):
            #Extract the dates from user input field and make datetime.date format
            if way == 'specific':
                start_date = date1.text().split('/')
                start_date = date(int(start_date[2]), int(start_date[0]), int(start_date[1]))
                end_date = date2.text().split('/')
                end_date = date(int(end_date[2]), int(end_date[0]), int(end_date[1]))
           
            data=[]
            dates=[]
            
            #filter datapoints based on date range input by user
            for t in range(len(raw_dates)):
                if way == 'season':
                    start_date = seasonS.text().split('/')
                    start_date = date(raw_dates[t].year, int(start_date[0]), int(start_date[1]))
                    end_date = seasonE.text().split('/')
                    end_date = date(raw_dates[t].year, int(end_date[0]), int(end_date[1]))
                    
                if raw_dates[t] >= start_date and raw_dates[t] <= end_date:
                    data.append(raw_data[t])
                    dates.append(raw_dates[t])
            return data, dates
        
        #Give function to the graphing button
        generate_btn.clicked.connect(graph)
        create_spaces.clicked.connect(createSlots)
        update_spaces.clicked.connect(updateSlots)
        
        
    def tab4UI(self):
        #creates text that is able to link to youtube tutorial videos
        example = QLabel()
        example.setText('''<a href='https://youtu.be/csKUE2iLCII'>How to import example data when you first download the tool</a>''')
        example.setOpenExternalLinks(True)
        own = QLabel()
        own.setText('''<a href='https://youtu.be/kfCO77dJt8c'>How to import your own data into the tool</a>''')
        own.setOpenExternalLinks(True)
        addpt = QLabel()
        addpt.setText('''<a href='https://youtu.be/llJd3eYIPOA'>How to manually add a data point</a>''')
        addpt.setOpenExternalLinks(True)
        totpollen = QLabel()
        totpollen.setText('''<a href='https://youtu.be/SGz4TARd0Wo'>How to edit pollen categories and calculate total pollen per day</a>''')
        totpollen.setOpenExternalLinks(True)
        
        corrsimple = QLabel()
        corrsimple.setText('''<a href='https://youtu.be/oHi1GAu6cP0'>How to calculate a simple correlation</a>''')
        corrsimple.setOpenExternalLinks(True)
        corrdates = QLabel()
        corrdates.setText('''<a href='https://youtu.be/t07QWXaJ1W0'>How to calculate a correlation from a specific range of dates</a>''')
        corrdates.setOpenExternalLinks(True)
        corravg = QLabel()
        corravg.setText('''<a href='https://youtu.be/j8sozS84SnA'>How to calculate a correlation using yearly or monthly averages</a>''')
        corravg.setOpenExternalLinks(True)
        corrsave = QLabel()
        corrsave.setText('''<a href='https://youtu.be/iPAekEz70VI'>How to save your correlation results</a>''')
        corrsave.setOpenExternalLinks(True)
        
        graphsimple = QLabel()
        graphsimple.setText('''<a href='https://youtu.be/rPRv1LG3Nng'>How to create a simple graph</a>''')
        graphsimple.setOpenExternalLinks(True)
        graphavg = QLabel()
        graphavg.setText('''<a href='https://youtu.be/usi_bolu5mw'>How to create a graph of averages in the data</a>''')
        graphavg.setOpenExternalLinks(True)
        graphregress = QLabel()
        graphregress.setText('''<a href='https://youtu.be/ag5SpNZiunY'>How to graph regressions to represent trends over time</a>''')
        graphregress.setOpenExternalLinks(True)
        graphregressext = QLabel()
        graphregressext.setText('''<a href='https://youtu.be/PwZcpWxa-Lg'>How to extend regressions to see future predictions</a>''')
        graphregressext.setOpenExternalLinks(True)
        graphsave = QLabel()
        graphsave.setText('''<a href='https://youtu.be/PwZcpWxa-Lg'>How to save a graph</a>''')
        graphsave.setOpenExternalLinks(True)
        
        guide = QLabel()
        guide.setText('''<a href='https://docs.google.com/document/d/1FTMhJfqGYcq7x647V00lqRdfvlEVrG9LKunpnRkDKdU/edit?usp=sharing'>Click Here to View the Full User's Guide</a>''')
        guide.setOpenExternalLinks(True)
        
        vbox=QVBoxLayout(self)
        vbox.addWidget(QLabel('<b>The following link to tutorial videos if you need help with the tool:</b>'))
        vbox.addWidget(QLabel('Actions in the "Data Entry" Tab:'))
        vbox.addWidget(example)
        vbox.addWidget(own)
        vbox.addWidget(addpt)
        vbox.addWidget(totpollen)
        vbox.addWidget(QLabel('Actions in the "Calculations" Tab:'))
        vbox.addWidget(corrsimple)
        vbox.addWidget(corrdates)
        vbox.addWidget(corravg)
        vbox.addWidget(corrsave)
        vbox.addWidget(QLabel('Actions in the "Generate Graphs" Tab:'))
        vbox.addWidget(graphsimple)
        vbox.addWidget(graphavg)
        vbox.addWidget(graphregress)
        vbox.addWidget(graphregressext)
        vbox.addWidget(graphsave)
        vbox.addStretch(0)
        vbox.addWidget(guide)
        
        self.tab4.setLayout(vbox)


#Automatically launches the app when the program is run
def main():
    app = QCoreApplication.instance()
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    ex = tabs()
    
    ex.show()
    
    app.setQuitOnLastWindowClosed(True)
    app.exec_()
    print("exiting")
    sys.exit()


main()
    
