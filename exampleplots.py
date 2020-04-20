# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 12:16:41 2020

@author: Tobias
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import date
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.preprocessing import PolynomialFeatures
import statsmodels.api as sm

#create the boxplots
def boxplot(raw_arr,raw_days,name,regressions,axies,future):
    #array of colors, rotated through in order
    colors=['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']
    #initialize the plots, other variables
    fig, ax = plt.subplots(figsize=(10,8))
    ax2=ax.twinx()
    legend=[]
    #categories on left axis
    left=''
    #legend information for regressions is put in this array
    newName=[]
    right=''
    minYear=30000
    maxYear=0
    
    for j in range(len(raw_arr)):
        array1 = np.array([])
        days1 = np.array([])
        #fill array1, days1 with only data that isnt none
        for i in range (np.size(raw_days[j])):
            if raw_arr[j][i]!=None: 
                array1 = np.append(array1, raw_arr[j][i])
                days1 = np.append(days1, raw_days[j][i])
        #get regression type as number
        if(regressions[j]=='Polynomial'):
            order=2
        if(regressions[j]=='Linear'):
            order=1
        if(regressions[j]=='LOESS'):
            order=0
        if(regressions[j]=='None'):
            order=-1
        
        dates1=np.array([])
        #wills dates1 with the int representing date
        for i in range(0, len(days1)):
            dates1=np.append(dates1,mdates.date2num(days1[i]))
            
       
        #seperates the data given into years and yearly averages
        arr,labels=seperateByYear(array1,dates1) #split array
        #keeps track of the max and min year for x axis labels
        minYear=min(minYear,min(labels))
        maxYear=max(maxYear,max(labels))
        #scaledlabels will allow regressions to be based off of the starting year
        #instead of 1970 or 01/01/0000 
        scaledLabels=np.array([])
        for label in labels:
            scaledLabels=np.append(scaledLabels,label-labels[0])
        #boxplots on the left axis    
        if(axies[j]=='Left'):
            bp=draw_plot(arr, j,len(raw_arr), colors[j], "white",labels,ax)
            left=left+', '+name[j]
            newName.append(name[j])
            reg=ax
        #boxplots on the right axis
        elif(axies[j]=='Right'): 
            bp=draw_plot(arr, j,len(raw_arr), colors[j], "white",labels,ax2)
            right=right+', '+name[j]
            newName.append(name[j])
            reg=ax2
        
        handles = bp["boxes"][0]
        #adds the handle to the legend
        legend.append(handles)
        means=[]
        #retrieves means of the boxplots, used for the regression
        for line in bp["means"]:
            _,mean=line.get_xydata()[1]
            means.append(mean)
        #print(medians)
        #print(labels)
     
        
      
        if(order==1 or order==2):
            if(future==-1 or labels[-1]>future):
                future=labels[-1]
            a=np.polyfit(labels,means,order)       #calculates nth order regression 
            b=np.polyfit(scaledLabels,means,order) #calculates scaled boxplots so constants can be printed cleanly
            if order==1:
                equation='m='+str(round(b[0],2))+'/year, b='+str(round(b[1],2))
            else:
                equation='a='+str(round(b[0],2))+'/year^2, b='+str(round(b[1],2))+'/year, c='+str(round(b[2],2))
            #plots and adds the line of regression to the legend
            l3,=reg.plot(np.linspace(labels[0],future,50),np.polyval(a,np.linspace(labels[0],future,50)),color=colors[j],label=(regressions[j]+" reg. of "+name[j]+": "+equation),linestyle="--") #plots polynomial regression
            legend.append(l3)
            
            
            newName.append(regressions[j]+" reg. of "+name[j]+": "+equation)
        elif(order==0):
            loess=loessregression(labels,means)   #performs loess regression
            l4, =reg.plot(labels,loess,color=colors[j],label="LOESS of"+name[j],linestyle='--') #plots loess
            legend.append(l4)
            newName.append("LOESS of "+name[j])
        
        #print(handles)
        ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
        
        
        # rotates and right aligns the x labels, and moves the bottom of the
        # axes up to make room for them
    
    fig.autofmt_xdate() 
    #print(legend)
    #print(name)
    loc='best'
    
    if(left!=''):
        ax.set_ylabel(left)   #set the axis label
   
        #fig.autofmt_xdate()  
        ax.grid(True)
    if(right!=''):
        ax2.grid(True)
        ax2.set_ylabel(right)  #set the axis label
    plt.xticks(range(minYear,maxYear+1))#x axis labeled with range of years
    ax.set_ylabel(left)   #set the axis label
    ax2.set_ylabel(right)  #set the axis label
    
    ax.set_xlabel("Years")
    plt.show()
    plt.legend(legend,newName,bbox_to_anchor=(-0.05, .95, 1.1, .2), loc=1,
               ncol=2, mode="expand", borderaxespad=0.)
               
#made to plot two lines on the same graph
    
def arrayvstime2(raw_arr,raw_days,names,regressions,axies,future):
    #formats for x labeling
    years = mdates.YearLocator()   # every year
    months = mdates.MonthLocator()  # every month
    everyOtherMonth=mdates.MonthLocator(interval=2)#every other month
    years_fmt = mdates.DateFormatter('%Y')
    months_fmt=mdates.DateFormatter('%m')

    #format future to date2num number so it can be used
    if(future!=-1):
        future=int(mdates.date2num(date(future,1,1)))
    #Filter data so a date is only included if there is a value for both
    #categories for that day
    
        
    fig, ax = plt.subplots(figsize=(10,8))
    ax2=ax.twinx()
    
    legend=[]
    left=''
    right=''
    dateMin=10000
    dateMax=0
    colors=['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']
    for j in range(len(raw_arr)):
        
        array1 = np.array([])
        days1 = np.array([])
        for i in range (np.size(raw_days[j])):
            if raw_arr[j][i]!=None: 
                array1 = np.append(array1, raw_arr[j][i])
                days1 = np.append(days1, raw_days[j][i])
        
        
        if(regressions[j]=='Polynomial'):
            order=2
        if(regressions[j]=='Linear'):
            order=1
        if(regressions[j]=='LOESS'):
            order=0
        if(regressions[j]=='None'):
            order=-1
        #dates1 is the raw date2numarray for plotting
        #scaledDates is the offset version of this
        #datesRegress is divided by 365 for regression units to be in years
        dates1=np.array([])
        scaledDates=np.array([])
        datesRegress=np.array([])
        
        for i in range(0, len(days1)):
            dates1=np.append(dates1,mdates.date2num(days1[i]))
            scaledDates=np.append(scaledDates,dates1[i]-dates1[0])
            datesRegress=np.append(datesRegress,scaledDates[i]/365)
        dateMin=min(dateMin,datesRegress[0])
        dateMax=max(dateMax,datesRegress[-1])
        #print(array1,dates1)
        if(axies[j]=='Left'):
            
            l1, =ax.plot(dates1, array1,color=colors[j],label=names[j], marker='.')#plots the line
            legend.append(l1)  
            if(order==1 or order==2):
                if(future==-1 or future<dates1[-1]):
                    future=int(dates1[-1]+1)
                a=np.polyfit(datesRegress,array1,order)       #calculates nth order regression 
                b=np.polyfit(dates1,array1,order)       #calculates nth order regression
                if order==1:
                    equation='m='+str(round(a[0],2))+'/year, b='+str(round(a[1],2))
                else:
                   
                    equation='a='+str(round(a[0],2))+'/year^2'+', b='+str(round(a[1],2))+'/year, c='+str(round(a[2],2))
                l3,=ax.plot(np.append(dates1,range(int(dates1[-1])+1,future)),np.polyval(b,np.append(dates1,range(int(dates1[-1])+1,future))),color=colors[j],label=(regressions[j]+" reg. of "+names[j]+": "+equation),linestyle='--') #plots polynomial regression
                legend.append(l3)
            elif(order==0):
                loess=loessregression(dates1,array1)   #performs loess regression
                l4, =ax.plot(dates1,loess,color=colors[j], label="LOESS of "+names[j],linestyle='--') #plots loess
                legend.append(l4)
            
            left=left+', '+names[j]
                          
            
            ax.tick_params(axis='y', labelcolor=colors[j])  #color of the axis labels
           
            
             
            
        if(axies[j]=='Right'):   #creates axis on right
            color="tab:green"    #color of second y axis
            
            l2,=ax2.plot(dates1,array1,color=colors[j],label=names[j], marker='.')  #plots as scatter plot
            legend.append(l2)
            if(order==1 or order==2):
                a=np.polyfit(datesRegress,array1,order)       #calculates nth order regression 
                b=np.polyfit(dates1,array1,order)
                if order==1:
                    equation='m='+str(round(a[0],2))+'/year, b='+str(round(a[1],2))
                else:
                   
                    equation='a='+str(round(a[0],2))+'/year^2'+', b='+str(round(a[1],2))+'/year, c='+str(round(a[2],2))
                l3,=ax.plot(np.append(dates1,range(int(dates1[-1])+1,future)),np.polyval(b,np.append(dates1,range(int(dates1[-1])+1,future))),color=colors[j],label=(regressions[j]+" reg. of "+names[j]+": "+equation),linestyle='--') #plots polynomial regression
                legend.append(l3)
            elif(order==0):
                loess=loessregression(dates1,array1)   #performs loess regression
                l4, =ax2.plot(dates1,loess,color=colors[j], label="LOESS of "+names[j],linestyle='--') #plots loess
                legend.append(l4)
            right=right+', '+names[j]
            
            ax2.tick_params(axis='y', labelcolor=colors[j])
            # rotates and right aligns the x labels, and moves the bottom of the
            # axes up to make room for them
     # format the ticks
    dateRange=dateMax-dateMin
    #auto locators/formatters very useful for making the graphs look good and scaled properly
    locator=mdates.AutoDateLocator(minticks=5) 
    minorLocator=mdates.AutoDateLocator(minticks=30, maxticks=80)
    formatter = mdates.AutoDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_minor_locator(minorLocator)
    ax.xaxis.set_major_formatter(formatter)
    
    # format the coords message box
    ax.format_xdata = mdates.DateFormatter('-%m-%d-%Y') 
    ax2.format_xdata = mdates.DateFormatter('-%m-%d-%Y')  
    if(left!=''):
        ax.set_ylabel(left)   #set the axis label
   
        #fig.autofmt_xdate()  
        ax.grid(True)
    if(right!=''):
        ax2.grid(True)
        ax2.set_ylabel(right)  #set the axis label
    plt.legend(handles=legend,bbox_to_anchor=(-0.05, .95, 1.1, .2), loc=1,
       ncol=2, mode="expand", borderaxespad=0.)    #creates legend\
    
    ax.set_xlabel("Time")
    
    plt.show()
def draw_plot(data, j,lenj,edge_color, fill_color,labels,ax):
    positions=labels.copy()
    k=.5
    for i in range(len(positions)):
        #formula to set positions of boxplots to be offset so that they can be centered
        #around a year tick but not on top of eachother
        positions[i]=positions[i]+(((j+1)/lenj)-.5-(.5/lenj))*k
    print(labels)
    bp = ax.boxplot(data, widths=0.4/lenj, patch_artist=True,positions=positions,manage_ticks=False, showmeans=True,meanline=True,whis=[2,98])
    
        
    for element in ['boxes', 'whiskers', 'fliers','means' ,'medians', 'caps']:
        plt.setp(bp[element], color=edge_color)
    for patch in bp['boxes']:
        patch.set(facecolor=fill_color)
    return bp
def seperateByYear(data, dates):
    #seperates data into years for the boxplotting to handle
    deltay=mdates.num2date(dates[-1]).year-mdates.num2date(dates[0]).year
    i=0
    j=-1
    k=0
    array = [[] for g in range(deltay+1)]
    
    while(i<data.size):
        if(mdates.num2date(dates[i]).year==mdates.num2date(dates[i-1]).year and deltay>0 and i>0):
            k+=1
        elif(deltay==0):
            j=0
        else:
            j+=1
            k=0
       
        array[j].append(data[i])
        
        i+=1
    labels=[]
    for i in range(mdates.num2date(dates[0]).year,mdates.num2date(dates[0]).year+deltay+1):
        labels.append(i)
    return array,labels
        
def loessregression(x,y):
    #basic loess regression code
    lowess_sm = sm.nonparametric.lowess
    yest_sm = lowess_sm(y,x,frac=1./3.,it=3, return_sorted = False)
    return yest_sm
   #the dates should be in number format before being passed in as shown below

#days = np.array([mdates.date2num(date(2013,1,30)), mdates.date2num(date(2013,5,30)),mdates.date2num(date(2014,4,5)), mdates.date2num(date(2015,8,6)), mdates.date2num(date(2016,8,6))])
#arr=np.array([100,100000,100000,40000,8000])
#arr2=np.array([100000,100,50000,30000,8000])
#boxplot(arr,days,"pollen count")
#arrayvstime2(arr,arr2,days,"pollen","ragweed",2)

