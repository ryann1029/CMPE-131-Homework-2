# Group SUS
# Group Members: Ryan Nguyen, Rafael Meza, Jose Hernandez, Kate Dinh
# CMPE 131-04
# Homework 2 - Data Format
# March 13, 2022

import csv
from tkinter import N 
import xml.etree.ElementTree as ET
import os
import re

def changeFormat(fileName, formatType, fortemp = ""):
    
    print("File Reference: \"" + fileName + "\"")
    if (formatType == '-c'):
        txt_to_csv(fileName, fortemp)

    elif (formatType == '-j'): 
        txt_to_json(fileName)
        os.remove("temp.csv")
        print("File \"temp.csv\" is now deleted.")
        
    elif (formatType == '-x'):
        txt_to_xml(fileName)
        os.remove("temp.csv")
        print("File \"temp.csv\" is now deleted.")
        
    else:
        raise Exception("Your selection was not \"-c\", \"-j\", or \"-x\" for .xml.\nProgram Terminated!")

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

    print("Creating \"temp.csv\"")
    txt_to_csv(fileName, "temp")

    split = fileName.split(".")
    fileNameWOfileType = split[0]
    
    print("...Converting \"temp.csv\" to .json...")

    csvFile = "temp.csv"
    csvFileOpen = open(csvFile, 'r')
    jsonFile = fileNameWOfileType + ".json" # Make sure to change back to "fileNameWOfileType"
    csvData = csv.reader(csvFileOpen)
    jsonData = open(jsonFile, 'w')
    
    jsonData.write("{" + "\n")

    rowCount = numRows(csvFile)-1 # minus 1 since we will not be including header as a row

    rowNum = 0
    top = []

    for row in csvData:
        if rowNum == 0:
            for i in range(len(row)):
                row[i] = row[i].replace(" ", "_")
                top.append(row[i])

        else:
            if len(row) > 0:
                jsonData.write("\t\"Player" + str(rowNum) + "\": {\n")
                for i in range(len(row)):
                    if i < len(row)-1:
                        jsonData.write("\t\t\"" + top[i] + "\": " + "\"" + row[i] + "\",\n")
                    else:
                        jsonData.write("\t\t\"" + top[i] + "\": " + "\"" + row[i] + "\"\n")
                
                if rowNum < rowCount:
                    jsonData.write("\t},\n")
                else:
                    jsonData.write("\t}\n")
            else:
                continue
        rowNum += 1

    jsonData.write("}" + "\n")

    print("Converted to .json")

def txt_to_xml(fileName):

    print("Creating \"temp.csv\"")
    txt_to_csv(fileName, "temp")

    split = fileName.split(".")
    fileNameWOfileType = split[0]

    print("...Converting \"temp.csv\" to .xml...")

    csvFile = "temp.csv"
    csvFileOpen = open(csvFile, 'r')
    xmlFile = fileNameWOfileType + ".xml"

    csvData = csv.reader(csvFileOpen)
    xmlData = open(xmlFile, 'w')

    xmlData.write('<?xml version="1.0" encoding="UTF-8"?>' + "\n") # there must be only one top-level tag
    xmlData.write('<NFL_DB>' + "\n")
    
    rowNum = 0
    top = []
    
    for row in csvData:
        if rowNum == 0:
            for i in range(len(row)):
                row[i] = row[i].replace(" ", "_")
                top.append(row[i])
        else:
            if len(row) == 0:
                continue
            else:
                xmlData.write("\t<player>\n")
                for i in range(len(row)):
                    xmlData.write("\t\t<" + top[i] + ">" +  row[i] + "</" + top[i] + ">\n")
                xmlData.write("\t</player>\n")
                
        rowNum += 1

    xmlData.write('</NFL_DB>' + "\n")
    xmlData.close()
    
    csvFileOpen.close()
    
    print("Converted to .xml")

def numRows(fileName):
    rowCount = 0
    validity = re.search(".*\.csv$", fileName)
    print("Validity:", validity)
    if validity == None:
        raise Exception("Invalid file type. Must be .csv type.")
    else:
        csvFileOpen = open(fileName, 'r')
        csvData = csv.reader(csvFileOpen)

        for row in csvData:
            if len(row) <= 0:
                continue
            else:
                rowCount += 1

    return rowCount
    

############################################
# Main Function

fileNameChoice = input("Would you like to input a file? Y/N: ")

while(True):
    if (fileNameChoice == 'Y' or fileNameChoice == 'y'):
        fileName = input("Your .txt file name (do not include file type): ")
        fileName = fileName + ".txt"
        break
    elif (fileNameChoice == 'N' or fileNameChoice == 'n'):
        fileName = "NFL Offensive Player stats, 1999-2013.txt"
        break
    else:
        fileNameChoice = input("Invalid choice. Please pick Y/N: ")

choice = input("File type? \"-c\" for .csv, \"-j\" for .json, \"-x\" for .xml: ")
check = re.search("(^-c$)|(^-x$)|(^-j$)", choice) # using RegEx to validate choice of input

# If user inputs invalid choice, continuously make user choose a correct one.
while check == None:
    choice = input("Invalid choice. Choose \"-c\" for .csv, \"-j\" for .json, or \"-x\" for .xml: ") 
    check = re.search("(^-c$)|(^-x$)|(^-j$)", choice) # using RegEx to validate choice of input

changeFormat(fileName, choice)

print("Program Terminated!")