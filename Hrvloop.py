# import necessary libraries
import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import numpy as np
import heartpy as hp
import csv 

path = os.getcwd()
# use glob to get all the csv files 
# in the folder
# field names 
fields = ['Patient','Day','BPM', 'ibi', 'sdnn', 'rmssd','hr_mad','sd1','sd2','sd1/sd2',] 
filename = "Measure1.csv"
with open(filename,'a') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)

directory = 'D:/Rohan/RA/new data/'
folder = '_Patient'



#numOfDirs = len(next(os.walk(directory))[1])
sub_folders = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]

num = 10;
ite =1;


#print(sub_folders)
for x in sub_folders:
    ite = ite + 1

    if ite > 10 :
        break

    tempDir = directory + x + '/ECG/'
    #print(tempDir);
    print ("\n")
    dir_list = os.listdir(tempDir)
    #print("Files and directories in '", path, "' :")
    

    for singleFile in dir_list:
       
        if os.path.getsize(tempDir + singleFile)!=0:
            print(tempDir + singleFile + "\n")
            try:
                    data = hp.get_data(tempDir + singleFile)
                    #data = hp.get_data("D:/Rohan/RA/new data/1_Patient/ECG/ECG_Day_1.csv")
                    sample_rate = 240
                    filtered = hp.filter_signal(data, cutoff = 0.05, sample_rate = sample_rate, filtertype='notch')
                    wd, m = hp.process(filtered, sample_rate)

                    #display computed measures
                
                    rows= [tempDir,singleFile,m['bpm'], m['ibi'], m['sdnn'], m['rmssd'],m['hr_mad'],m['sd1'],m['sd2'],m['sd1/sd2']]
                    #print(rows)

                    # writing to csv file 
                    with open(filename,'a') as csvfile: 
                        # creating a csv writer object 
                        csvwriter = csv.writer(csvfile) 
                        # writing the data rows 
                        csvwriter.writerow(rows)
                        print("HRV _Written")


            except:
                print("Failed | An exception occurred")
                try:
                    print("Trying smoothning")
                    #hampel_filter= hp.hampel_filter(data, filtsize = 6)
                    smoothed = hp.smooth_signal(data, sample_rate = 2, window_length=4, polyorder=2)
                    print("Smoothed")
                    wd, m = hp.process(smoothed, sample_rate)
                    rows= [tempDir,singleFile,m['bpm'], m['ibi'], m['sdnn'], m['rmssd'],m['hr_mad'],m['sd1'],m['sd2'],m['sd1/sd2']]
                    # writing to csv file 
                    with open(filename,'a') as csvfile: 
                    # creating a csv writer object 
                        csvwriter = csv.writer(csvfile) 
                        csvwriter.writerow(rows)
                    #print(rows)
                    print("HRV _Written")
                except:
                    print("Failed at  Smoothning")
                    rows= [tempDir,singleFile,'NA','NA','NA','NA','NA','NA','NA','NA']            
                    with open(filename,'a') as csvfile: 
                    # creating a csv writer object 
                        csvwriter = csv.writer(csvfile) 
                        csvwriter.writerow(rows)
        else:
            print("File size 0")
            rows= [tempDir,singleFile,'NA','NA','NA','NA','NA','NA','NA','NA']            
            with open(filename,'a') as csvfile: 
                # creating a csv writer object 
                    csvwriter = csv.writer(csvfile) 
                    csvwriter.writerow(rows)
