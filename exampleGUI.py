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
        
        #Titles the window
        self.setWindowTitle("Data Analysis Tool")
        self.setGeometry(100, 100, 775 ,550)
        
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
        
        self.file_name = QLabel('<u>No data has been loaded</u>')
        
        #Create input fields
        self.input_date = QLineEdit('mm/dd/year')
        self.data_pt = QLineEdit('Data value')
        
        #creates dropdown menu for categories
        self.cbox = QComboBox()
        
        #horizontally align buttons and input fields
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

        #Browse user's computer for excel files, create new if none selected
        def openFileNameDialog():
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            new_data.setText("loading data...")
            file, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Excel (*.xlsx)")
            #xw.Book(file)
            try:
                self.file_name.setText('File imported: ' + extractName(file))
                ws = RFE.readFile(file)
                raw_data = RFE.toList(ws,RFE.findOrientation(ws),False)
                self.data = RFE.filter(raw_data[0], raw_data[1], raw_data[2])
            
                filterText="\nFilter Report\n\n"+self.data[3]
                new_data.setText(filterText+"\n Please See other window to continue")
                #Update master file
                if extractName(file) != 'master.xlsx': 
                    mergetext=RFE.toMainSpreadSheet(self.data[0], self.data[1].copy(),self.data[2],self.masterFileName)
                    new_data.setText("Merge Report \n\n"+mergetext+filterText)
              
                self.data=RFE.loadData(self.masterFileName)
                updateCategories() #add categories to drop-down menus
            except:
                self.throwError("Error: No File Selected")
            
        def extractName(file):
            #separates the name of the file from its directory
            directory=file.split('/')
            name=directory[-1]
            return name
        
        def updateCategories():
            #Adds headers for data categories to dropdown menus
            #self.data=RFE.loadData(self.masterFileName)
            categories = self.data[0]
            for x in [self.cbox, self.cat1, self.cat2, self.c1,self.c2,self.c3,self.c4,self.c5,self.c6]:
                x.clear()
                for y in categories:
                    x.addItem(y)
        def setPollenCategories():
            categories=RFE.loadDataWithP("master.xlsx")[0]
            ex = pollenCategories(categories)
            ex.show()
            if(ex.exec_()):
                RFE.rewriteCategories(ex.newCategories,'master.xlsx')
            new_data.setText("Categories updated")
            
        def load():
            self.data=RFE.loadData(self.masterFileName)
            if self.data[0] != []:
                updateCategories()
                self.file_name.setText('File loaded: master.xlsx')
            else:
                self.throwError('Master file has not been created. Click "Browse Files" and select a data file')
            
            
        def sum_pollen():
            report=RFE.calcTotalPollen('master.xlsx')
            new_data.setText(report)
            updateCategories()


        def send_email():
            #get today's data, email it
            #some function to filter by today's date
            #RFE.toNewSpreadSheet(categories, data, dates, filename)
            #gmail.send_message_from_GUI("trschaeffer@wpi.edu", "Subject", "Hello! here is the pollen data for today",filename)
            pass
        
        def add_datapoint():
            try:
                #adds data point to master file using toMainSpreadSheet in readFromExcel
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
        
        self.setTabText(0, "Data Entry") #Title the tab


    def tab2UI(self):        
        #Dropdown menu for category for correlation
        self.cat1 = QComboBox()
        self.cat2 = QComboBox()
        
        #formats the two categories next to eachother
        hbox0 = QHBoxLayout()
        hbox0.addWidget(QLabel('<b>Find Correlation Between:</b>'))
        hbox0.addWidget(self.cat1)
        hbox0.addWidget(QLabel('         and'))
        hbox0.addWidget(self.cat2)
       
        #Create options to calculate average of year or month
        averagesbox = QComboBox()
        averagesbox.addItem('None')
        averagesbox.addItem('Years')
        averagesbox.addItem('Months')
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel('Calculate averages in the data across'))
        hbox1.addWidget(averagesbox)
        
        #Create options to select time period of data to correlate
        #datecheck = QCheckBox('Filter data by specific dates (if checked, enter a range of dates below)')
        hbox2 = QHBoxLayout()
        datecheck = QCheckBox('Include data between the dates:')
        #hbox2.addWidget(QLabel('Include data between the dates'))
        hbox2.addWidget(datecheck)
        date1 = QLineEdit('mm/dd/year')
        hbox2.addWidget(date1)
        hbox2.addWidget(QLabel('and'))
        date2 = QLineEdit('mm/dd/year')
        hbox2.addWidget(date2)
        
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
        self.cor_results = QTableWidget(1,7)
        self.cor_results.setItem(0,0,QTableWidgetItem('Correlation'))
        self.cor_results.setItem(0,1,QTableWidgetItem('p-value'))
        self.cor_results.setItem(0,2,QTableWidgetItem('Category 1'))
        self.cor_results.setItem(0,3,QTableWidgetItem('Category 2'))
        self.cor_results.setItem(0,4,QTableWidgetItem('Start date'))
        self.cor_results.setItem(0,5,QTableWidgetItem('End date'))
        self.cor_results.setItem(0,6,QTableWidgetItem('Averages'))
    
        #sets the overall layout for the tab
        vbox1 = QVBoxLayout(self)
        vbox1.addLayout(hbox0)
        vbox1.addStretch(3)
        vbox1.addWidget(QLabel('<b>Optional Data Analysis Settings:</b>'))
        vbox1.addStretch(0)
        vbox1.addLayout(hbox1)
        vbox1.addStretch(0)
        vbox1.addWidget(datecheck)
        vbox1.addLayout(hbox2)
        vbox1.addStretch(3)
        vbox1.addLayout(calc_form)
        vbox1.addWidget(QLabel('<b>Correlation Results</b>'))
        vbox1.addWidget(self.cor_results)
        vbox1.addLayout(saveHbox)
        vbox1.addWidget(save_btn)
        self.tab2.setLayout(vbox1)
        
        
        def calculate():
            try:
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
                    raw_xdata, raw_ydata, dates = dateFilter(raw_xdata, raw_ydata)
                except:
                    self.throwError('Invalid dates entered. Dates must be in mm/dd/year format.'
                                + ' Example: 1/1/2014 - 12/31/2019 will give all data from 2014-2019.')
                    return None
                
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
                
            self.cor_results.insertRow(1)
            self.cor_results.setItem(1, 0, rText)
            self.cor_results.setItem(1, 1, pText)
            self.cor_results.setItem(1, 2, QTableWidgetItem(cat1_name))
            self.cor_results.setItem(1, 3, QTableWidgetItem(cat2_name))
            
            if datecheck.isChecked() == True:
                self.cor_results.setItem(1, 4, QTableWidgetItem(date1.text()))
                self.cor_results.setItem(1, 5, QTableWidgetItem(date2.text()))
            if averagesbox.currentText() != 'None':
                self.cor_results.setItem(1, 6, QTableWidgetItem(averagesbox.currentText()))
            
        def calculateAverages(raw_xdata, raw_ydata, dates, way):
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
            sumData=0
            size=len(datalist)
            for x in datalist:
                if x != None:
                    sumData+=x
                else:
                    size = size - 1
                    
            average=sumData/size
            return average
        
        def dateFilter(raw_xdata, raw_ydata):
            if date1.text() != '' and date2.text() != '':
                #Extract the dates from user input field and make datetime.date format
                start_date = date1.text().split('/')
                start_date = date(int(start_date[2]), int(start_date[0]), int(start_date[1]))
                end_date = date2.text().split('/')
                end_date = date(int(end_date[2]), int(end_date[0]), int(end_date[1]))
            
            xdata=[]
            ydata=[]
            dates=[]
            #filter datapoints based on date range input by user
            for t in range(len(self.data[2])):
                if self.data[2][t] >= start_date and self.data[2][t] <= end_date:
                    xdata.append(raw_xdata[t])
                    ydata.append(raw_ydata[t])
                    dates.append(self.data[2][t])
            return xdata, ydata, dates
        
        def saveResults():
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
            RFE.toNewSpreadSheet(headings, datas, dates, self.saveFileName.text() + '.xlsx')
            self.throwError('File ' + self.saveFileName.text() + '.xlsx has been successfully saved to the "PollenTool" folder.')
            
        
        #assign function to calculate button
        calc_btn.clicked.connect(calculate)
        save_btn.clicked.connect(saveResults)
        
        #Titles the tab
        self.setTabText(1, "Calculations")
        
    def tab3UI(self):
        #Dropdown menu for graph x-variable
        self.c1=QComboBox()
        self.c2=QComboBox()
        self.c3=QComboBox()
        self.c4=QComboBox()
        self.c5=QComboBox()
        self.c6=QComboBox()
        cArr=[self.c1,self.c2,self.c3,self.c4,self.c5,self.c6]
       
        self.numBox=QComboBox()
        for i in range(1,7):
            self.numBox.addItem(str(i))
        
        HBoxIterate=[]
        axisNum=[]
        regressionType=[]
       
        for i in range(0, 6):
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
        #Arranges drop-downs for variables next to each other
        hbox1 = QHBoxLayout()
        """hbox1.addWidget(QLabel('category:'))
        hbox1.addWidget(self.xvar)
        hbox1.addWidget(QLabel('Axis #'))
        hbox1.addWidget(self.yvar)"""
        
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
        #hbox0.addWidget(QLabel('Include data between the dates'))
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
        #Check box to add linear regression model
        #regcheck = QCheckBox('Plot Regression?')
        #Horizontally align
        hboxGraphType = QHBoxLayout()
        hboxGraphType.addLayout(graph_form)
        #hbox2.addWidget(regcheck)
        
        #Create graphing buttons
        generate_btn = QPushButton('Generate Graph')
        #export_btn = QPushButton('Export Graph')
        #Horizontally align graphing buttons
        hboxGenerate = QHBoxLayout()
        hboxGenerate.addWidget(generate_btn)
        #hbox3.addWidget(export_btn)
        
        #sets the overall layout for the tab
        vbox1 = QVBoxLayout(self)
        vbox1.addLayout(hboxT)
        vbox1.addLayout(vboxIterate)
        vbox1.addStretch(2)
        vbox1.addLayout(hboxGraphType)
        vbox1.addStretch(3)
        vbox1.addWidget(QLabel('<b>Optional Data Analysis Settings:</b>'))
        vbox1.addStretch(0)
        vbox1.addLayout(hbox1)
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
            
            #if the user wants to make future predictions to a certain year,
            #this is the place to do it
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
                        raw_arr[i], datesArr[i] = dateFilter(raw_arr[i])
                except:
                    self.throwError('Invalid dates entered. Dates must be in mm/dd/year format.'
                                + ' Example: 1/1/2014 - 12/31/2019 will give all data from 2014-2019.')
                    return None
                    
            #If the user selects to calculate yearly or monthly averages
            # return x and y data in the form of averages using calculateAverages
            
            if averagesbox.currentText() != 'None':
                for i in range(len(raw_arr)):
                    arr[i], datesArr[i] = calculateAverages(raw_arr[i], datesArr[i], averagesbox.currentText())
            
            #If user does not choose to use optional data filtering, use raw data for calculations
            else:
                arr=raw_arr
            
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
            sumData=0
            size=len(datalist)
            for x in datalist:
                if x != None:
                    sumData+=x
                else:
                    size = size - 1
            average=sumData/size
            return average
        
        
        def dateFilter(raw_data):
            #Extract the dates from user input field and make datetime.date format
            start_date = date1.text().split('/')
            start_date = date(int(start_date[2]), int(start_date[0]), int(start_date[1]))
            end_date = date2.text().split('/')
            end_date = date(int(end_date[2]), int(end_date[0]), int(end_date[1]))
           
            data=[]
            dates=[]
            
            #filter datapoints based on date range input by user
            for t in range(len(self.data[2])):
                if self.data[2][t] >= start_date and self.data[2][t] <= end_date:
                    data.append(raw_data[t])
                    
                    dates.append(self.data[2][t])

            return data, dates
            
        
        #Give function to the graphing button
        generate_btn.clicked.connect(graph)
        create_spaces.clicked.connect(createSlots)
        update_spaces.clicked.connect(updateSlots)
        #Titles the tab
        self.setTabText(2, "Generate Graphs")


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
    
