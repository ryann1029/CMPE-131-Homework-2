import json 
import csv
from tkinter import N 
import xml.etree.ElementTree as ET
import os
import re

def changeFormat(fileName, formatType, fortemp = ""):
    
    print("File Reference: \"" + fileName + "\"")
    if (formatType == '-c'):
        txt_to_csv(fileName, fortemp)
    if (formatType == '-j'): 
        txt_to_json(fileName)
        
    if (formatType == '-x'):
        txt_to_xml(fileName)
        
        os.remove("temp.csv")
        print("File \"temp.csv\" is now deleted.")

def txt_to_csv(fileName, fortemp):
    print("...Converting .txt to .csv...")
    with open(fileName, newline='') as file:
        fileReader = csv.reader(file, delimiter='\t')
        
        if fortemp != "":
            fileNameWOfileType = fortemp
        else:
            split = fileName.split(".")
            fileNameWOfileType = split[0]
        newFile = open(fileNameWOfileType + ".csv", 'w')
        csvWriter = csv.writer(newFile)
        
        for x in fileReader: 
            csvWriter.writerow(x)
        newFile.close()
        
    print("Converted to .csv")

def txt_to_json(fileName):
    print("...Converting .txt to .json...")
    
    array = {}
    
    with open(fileName) as file:
        for line in file: 
            description1 = list(line.strip().split(None, 39))
            break
        l = 1
        for line in file: 
            description = list(line.strip().split(None, 38))
            block ='Player'+str(l)

            i = 0
            information = {}
            while i<len(description):
                information[description1[i]]= description[i]
                i = i + 1

            array[block] = information
            l = l + 1
    
    split = fileName.split(".")
    fileNameWOfileType = split[0]
    newFile = open(fileNameWOfileType + ".json", "w")
    json.dump(array, newFile, indent=4)
    newFile.close()
    print("Converted to .json")

def txt_to_xml(fileName):
    txt_to_csv(fileName, "temp")
    
    print("...Converting .csv to .xml...")

    csvFile = "temp.csv"
    csvFileOpen = open(csvFile, 'r')
    xmlFile = fileName + ".xml"

    csvData = csv.reader(csvFileOpen)
    xmlData = open(xmlFile, 'w')
    xmlData.write('<?xml version="1.0" encoding="UTF-8"?>' + "\n")
    # there must be only one top-level tag
    xmlData.write('<NFL_DB>' + "\n")
    
    rowNum = 0
    top = []
    temp = []
    
    for row in csvData:
        if rowNum == 0:
            for i in range(len(row)):
                row[i] = row[i].replace(" ", "_")
                top.append(row[i])
        else:
            if len(row) == 0:
                continue
            else:
                xmlData.write("<player>\n")
                for i in range(len(row)):
                    xmlData.write("\t<" + top[i] + ">" +  row[i] + "</" + top[i] + ">\n")
                xmlData.write("</player>\n")
                
        rowNum += 1

    xmlData.write('</NFL_DB>' + "\n")
    xmlData.close()
    
    csvFileOpen.close()
    
    print("Converted to .xml")


############################################
# Main Function

fileNameChoice = input("Would you like to input a file? Y/N\n")

while(True):
    if (fileNameChoice == 'Y' or fileNameChoice == 'y'):
        fileName = input("Your .txt file name (do not include file type): ")
        fileName = fileName + ".txt"
        break
    elif (fileNameChoice == 'N' or fileNameChoice == 'n'):
        fileName = "NFL Offensive Player stats, 1999-2013.txt"
        break
    else:
        fileNameChoice = input("Invalid choice. Please pick Y/N.\n")

choice = input("File type? \"-c\" for .csv, \"-j\" for .json, \"-x\" for .xml: ")
check = re.search("(^-c$)|(^-x$)|(^-j$)", choice) # using RegEx to validate choice of input

if check == None:
    print("Invalid choice.")
else:
    changeFormat(fileName, choice)

print("Program Terminated!")