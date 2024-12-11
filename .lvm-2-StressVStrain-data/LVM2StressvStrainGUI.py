#Brenton Yasuoka 11-9-2024 
#This is my Python Script that converts a folder full of .lvm files and creates a excel sheet that averages and rounds your stress and
#strain values from multiple trials/samples.
## FEEL FREE TO SHARE THIS IS OPEN SOURCE AND IS PUBLISHED ON MY GITHUB

import pandas as pd
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os




plt.close()

# Function to convert a .lvm file to .csv format
def convert_lvm_to_csv(lvm_file, csv_file):
    # Open the .lvm file and read all lines
    with open(lvm_file, 'r') as lvm:
        lines = lvm.readlines()

    # Locate the start of the data by skipping the header
    data_start = 0
    for i, line in enumerate(lines):
        if line.strip() == "":  # This can be adjusted based on actual header structure
            data_start = i + 1
            break
    
    data_lines = lines[data_start:]

    # Write the data to a .csv file
    with open(csv_file, 'w', newline='') as csv_out:
        writer = csv.writer(csv_out)
        for line in data_lines:
            # Split each line by tab delimiter and write to csv
            row = line.strip().split('\t')
            writer.writerow(row)

# Function to get a list of all .lvm file paths in a folder
def get_file_paths(folder_path,mode):
    file_paths = []
    
    # Traverse directory and add .lvm files to the list
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(mode):  # Filter only .lvm files
                file_paths.append(os.path.join(root, file))
            elif file.endswith(mode):
                file_paths.append(os.path.join(root, file))
    
    return file_paths

# Function to calculate strain
def find_strain(length_i, length_D):
    if length_i == 0:
        return float(0)  # Prevent division by zero
    return (length_D) / length_i

# Function to calculate stress
def find_stress(Area, Force):
    if Area == 0:
        return float(0)
    return (Force/Area)

# Function to delete the first 9 rows from a file
def delete_first_9_rows(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Skip the first 9 rows of the file
        for _ in range(9):
            next(reader, None)
        
        # Write the remaining rows to the output file
        for row in reader:
            writer.writerow(row)

# Function to round values to the nearest 0.005
def round_to_nearest(value):
    return round(value / 0.005) * 0.005

# Function to calculate average stress for unique strain values
def StressvStrainCare(df, Strain, Stress):
    # Assuming the columns in df are named 'Strain' and 'Stress' (adjust as needed)
    strain_column = Strain
    stress_column = Stress

    # Group by strain and calculate mean stress for each unique strain value
    grouped_df = df.groupby(strain_column, as_index=False)[stress_column].mean()

    # Add unique strain and average stress columns to the dataframe
    if 'ext' in Strain:
        uniqueStrainStr = f'Unique {Strain}'
        avgExtStressStr = f'Average ext {Stress}'
        df[uniqueStrainStr] = grouped_df[strain_column]
        df[avgExtStressStr] = grouped_df[stress_column]
        #plotIT(df,uniqueStrainStr,avgExtStressStr, f'{avgExtStressStr} vs {uniqueStrainStr} curve' )
    else:
        uniqueStrainStr = f'Unique {Strain}'
        avgExtStressStr = f'Average {Stress}'
        df[f'Unique {Strain}'] = grouped_df[strain_column]
        df[f'Average {Stress}'] = grouped_df[stress_column]
        #plotIT(df,uniqueStrainStr,avgExtStressStr, f'{avgExtStressStr} vs {uniqueStrainStr} curve' )
    return df

def lenAreaDF(path,columnTitle):
    df = pd.read_excel(path)
    return df[columnTitle]
    
def convLVM2CSV(path):
    files_list = get_file_paths(path,'.lvm')
    for i in files_list:
        csv_file_path = f'{i[0:-4]}.csv'
        convert_lvm_to_csv(i, csv_file_path)  # Convert lvm to csv
        csv_file_path2 = f'{csv_file_path[0:-4]}update.csv'
        delete_first_9_rows(csv_file_path, csv_file_path2)  # Remove first 9 rows of data this is useless in the grand scheme of things 
        #it can still be found in the original csv that doesn't have a updated.csv at the end

def plotIT(df,headers,pos,title):
    #pos length needs to be even
    color_list = ['blue', 'green', 'red', 'yellow']
    ii = 0
    plt.figure()
    for i in range(0,len(pos)//2,2):
        x = df[headers[pos[i]]]
        y = df[headers[pos[i+1]]]
        plt.scatter(x,y,label = headers[i+1],color = color_list[ii])
        ii += 1
    plt.title(title)
    plt.xlabel('Strain')
    plt.ylabel('Stress MPa')
    plt.legend
    plt.show()#(block = False)
    #input('Type something in terminal to go to next plot.')

def getCSVfileList(folderPath):
    csvFileList = get_file_paths(folderPath,'.csv')
    for i in csvFileList[:]:
        if "update.csv" in i:
            continue
        else:
            csvFileList.remove(i)
    return csvFileList

def workFunc(folderPath,length,area,excelName):
    csvFileList = getCSVfileList(folderPath)
    #csvFileList should only have the files that are called sometthingupdate.csv now
    with pd.ExcelWriter(f'{folderPath}/{excelName}', engine='openpyxl', mode='a') as writer:
        for iter1 in range(len(length)):
            for iter2 in csvFileList:
                temp_df = pd.read_csv(iter2)
                #Will pull the global displacement, extensometer displacement, and force data into its own dataframes
                glob_disp = temp_df['Global Displacement-mm (Mean)']
                ext_disp = temp_df['Extensometer Displacement-mm (Mean)']
                force_df = temp_df['Force-N (Mean)']
                #Creating some strain 
                temp_df['Strain Unrounded'] = np.nan
                temp_df['Strain Rounded'] = np.nan
                temp_df['Strain ext Unrounded'] = np.nan
                temp_df['Strain ext Rounded'] = np.nan
                temp_df['Stress (MPa)'] = np.nan
                for iter3 in range(len(temp_df)):
                    a = find_strain(length[iter1],glob_disp[iter3])
                    rndA = round_to_nearest(a)
                    b = find_strain(length[iter1], ext_disp[iter3])
                    rndB = round_to_nearest(b)
                    c = find_stress(area[iter1],force_df[iter3])
                    temp_df.at[iter3, 'Strain Unrounded'] = a
                    temp_df.at[iter3, 'Strain Rounded'] = rndA
                    temp_df.at[iter3, 'Strain ext Unrounded'] = b
                    temp_df.at[iter3, 'Strain ext Rounded'] = rndB
                    temp_df.at[iter3, 'Stress (MPa)'] = c
                temp_df = StressvStrainCare(temp_df, 'Strain ext Rounded', 'Stress (MPa)')
                temp_df = StressvStrainCare(temp_df, 'Strain Rounded', 'Stress (MPa)')
                #print(temp_df.head)
                sheetName = iter2.split('/')[-1]
                sheetName = sheetName[0:-10]
                temp_df.to_excel(writer,sheet_name = sheetName, index=False)

def cumulativeRes(folderpath,headers,nameConv,excelName1,excelName2):
    data = [[0]*len(headers)] #placeholder data
    blank_df = pd.DataFrame(columns = headers) #creates dataframe with the headers as the column names
    blank_df = pd.DataFrame(data, columns = headers)
    excelFile = pd.ExcelFile(f'{folderpath}/{excelName1}')
    #This creates a list of all the unique names like 4130_NHT and 4130_HT# 
    sheetNamesList = excelFile.sheet_names
    #print(sheetNamesList)
    nameConvL = len(nameConv)
    newSheetList = []
    seen = set()
    for i in sheetNamesList:
        shortname = i[:nameConvL]
        if i[0:nameConvL] not in seen:
            seen.add(shortname)
            newSheetList.append(shortname)
    newSheetList.pop(0)
    print(newSheetList)
    with pd.ExcelWriter(f'{folderpath}/{excelName2}', engine='openpyxl', mode='a') as writer:
        for iter1 in newSheetList:
            combined_df = pd.DataFrame()
            cumulative_df = pd.DataFrame()
            for iter2 in sheetNamesList:
                temp_df = excelFile.parse(iter2)
                #print(temp_df.head)
                if iter2[:nameConvL] == iter1 and headers[0] in temp_df.columns:
                    temp_df_filtered = (temp_df[headers])
                    combined_df = pd.concat([combined_df,temp_df_filtered],ignore_index = True)
                    cumulative_df1 = combined_df.groupby(headers[0], as_index=False)[headers[1]].mean()
                    cumulative_df2 = combined_df.groupby(headers[2], as_index=False)[headers[3]].mean()
                    cumulative_df = pd.concat([cumulative_df1, cumulative_df2],axis = 1)
                else: 
                    continue
            cumulative_df.to_excel(writer, sheet_name=iter1, index=False)

def plotMyCumulativeResults(folderpath,headers,excelName,positions):
    excelFile = pd.ExcelFile(f'{folderpath}/{excelName}')
    sheetNamesList = excelFile.sheet_names
    for iter1 in range(1,len(sheetNamesList)):
        df = excelFile.parse(sheetNamesList[iter1])
        title = sheetNamesList[iter1]
        plotIT(df,headers,positions,title)


######################################################################################
#Initialize room
root= tk.Tk()
root.title('LabView Tensile Data to Stress v Strain Curve')
root.geometry('1000x500')

#Create Widgets and functions for each widget
def lbl1_Initial_window():
    txt1 = 'Select the folder that holds all of your .lvm files. '
    txt2  = 'It is imperative that the files in the folder have a .lvm at the end. '
    txt3 = 'Lastly it is important that there are two excel files with different names in this folder. '
    txt4 = 'The excel files will be used to store all of the processed data for your viewing after you close the program'
    folder_instructionsTXT = txt1 + txt2 + txt3 + txt4
    lbl1 = tk.Label(root, text = folder_instructionsTXT, wraplength = 400)
    lbl1.grid(column = 0, row = 0, padx = 50, pady = 50)

def getpath():
    global folderPath
    folderPath = filedialog.askdirectory(initialdir = '/', title = "Select a file") #, filetypes = (("Text files",'*.txt'),("All files,",'*.*'))
    if folderPath:
        global lbl2
        if 'lbl2' in globals() and lbl2.winfo_exists():
            lbl2.destroy()
        lbl2 = tk.Label(root, text = folderPath)
        lbl2.grid(column = 0, row = 3, sticky = 'n')
        canvas.delete("text")
        disp_file_names(folderPath)
    

def btn1_Initial_window():
    btn1 = tk.Button(root, text = 'Select Folder', command = getpath)
    btn1.grid(column = 0, row = 1, padx = 175, sticky = 'n')
    

def square_initial_window():
    global canvas
    canvas = tk.Canvas(root, width = 500, height = 500)
    canvas.grid(column = 1,row = 0, rowspan = 20)
    rect = canvas.create_rectangle(50,50, 450,450, outline = 'black')

def get_file_paths(folder_path,mode):
    file_paths = []
    # Traverse directory and add .lvm files to the list
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(mode):  # Filter only .lvm files
                file_paths.append(os.path.join(root, file))
            elif file.endswith(mode):
                file_paths.append(os.path.join(root, file))
    
    return file_paths

def disp_file_names(folderPath):
    file_list = get_file_paths(folderPath, '.lvm')
    file_list.extend(get_file_paths(folderPath, '.xlsx'))
    x_off = 10
    y_off = 10
    line_spacing = 400//len(file_list)
    for i, string in enumerate(file_list):
        string = string.replace(f'{folderPath}/',"")
        y_position = y_off + i * line_spacing
        canvas.create_text(50 + x_off,50 + y_position,text=string,anchor="nw",tag="text")
    counter = 0
    for string in file_list:
        if string[-4::] == 'xlsx':
            counter += 1
    if counter < 2:
        global lbl3
        lbl3 = tk.Label(root, text = 'There is not enough Excel sheets we expect 2. Add the excel sheets and re-select folder.', wraplength = 400)
        lbl3.grid(column = 0, row = 4, sticky = 'n')
    elif counter == 2:
        if 'lbl3' in globals() and lbl3.winfo_exists():
            lbl3.destroy()
        disp_entryExcel_box()

def disp_entryExcel_box():
    txt1 = 'Input the naming convetion that is consistent across the samples/datasets. '
    txt2 = 'It is imperative there is a consistent naming convetion of consistent length. '
    txt3 = 'E.g. If your file names looked like: 4130_NHT_Test1.lvm , 4130_NHT_Test2.lvm , 4130_HT1_Test1.lvm and etc. '
    txt4 = 'The value you should enter should be 4130_NHT'
    NamingConventionInstructions = txt1 + txt2 + txt3 + txt4
    global lbl4
    lbl4 = tk.Label(root, text = NamingConventionInstructions, wraplength = 400)
    lbl4.grid(column = 0, row = 4, sticky = 'n')
    global nameConvention
    nameConvention = tk.Entry(root,width = 10)
    nameConvention.grid(column = 0, row = 5, sticky = 'n')
    root.bind('<Return>', excelFileNameInput)
    global btn2
    btn2 = tk.Button(root, text = 'Submit', fg = 'red', command = excelFileNameInput)
    btn2.grid(column = 0, row = 6,sticky = 'n')

def excelFileNameInput(event = None):
    use_in = nameConvention.get()
    Excel_Sheet_Instructions = 'Type in the First excel sheet that will store all the cumulative data for all the trials. Then in the second box type in the excel sheet name for the compiled data that will have averaged values ready to plot.'
    if use_in != '':
        if 'nameConvention' in globals() and nameConvention.winfo_exists():
            nameConvention.destroy()
            lbl4.destroy()
            btn2.destroy()
            lbl5 = tk.Label(root, text = Excel_Sheet_Instructions, wraplength = 400)
            lbl5.grid(column = 0, row = 4, sticky = 'n')
            root.bind('<Return>', NewWindow)
            btn3 = tk.Button(root, text = 'Submit', fg = 'red', command = NewWindow)
            btn3.grid(column = 0, row = 7,sticky = 'n')
            global excelName1
            global excelName2
            excelName1 = tk.Entry(root, width = 40)
            excelName1.grid(column = 0, row = 5, sticky = 'n')
            excelName2 = tk.Entry(root, width = 40)
            excelName2.grid(column = 0, row = 6, sticky = 'n')

def NewWindow():
    for widget in root.winfo_children():
        widget.destroy()
    root.after(5000, create_label)  # 5000ms = 5 seconds

def create_label():
    lbl1 = tk.Label(root, text='Loading.')
    lbl1.pack(pady=10)
    
    dots = ['Loading.', 'Loading..', 'Loading...']
    
    # Create a function for updating the label
    def update_text(index):
        lbl1.config(text=dots[index % len(dots)])
        # Schedule the next update
        root.after(2000, lambda: update_text(index + 1))

    waiting = 1
    while waiting != 0:
                #Knowns this is specific to .LVM's that will be used for Stress v Strain Curves
        headers = ['Unique Strain ext Rounded', 'Average ext Stress (MPa)', 'Unique Strain Rounded', 'Average Stress (MPa)']

        #Things to Change with each new use!
        folder_path = folderPath
        length = [33.21] #Some value length if you are using a nominal length
        area = [3.23] #Some value area if you are usinga  nominal area
            #if you are using a list of Lengths and Areas from an excel file make sure you know the column titles
        #excel_file_Path = '/Users/hoodieb/Desktop/MECH331B_Corrosion_Lab_Group_4_Data.xlsx'
        #length = lenAreaDF(excel_file_Path,'length (mm)') #update 2nd input argument with the title column for length
        #area = lenAreaDF(excel_file_Path,'area (mm^2)') #update 2nd input argument with the title column for area
        nameConvention = '4130_NHT' #This naming convention variable helps us compile all the data from each sample/trial. 
            #for example 4130_NHT_Test1 could be the name of your first lvm and then the second is 4130_NHT_Test2
            #the naming convention would be just 4130_NHT. 
        #Something super important to note here is that along all the tests we need to keep the length consistent because that is how it is used
            #for example: 4130_NHT_TEST# then 4130_HT1_TEST# and so on.
        #NOTE both excel sheets need to be created and blank within the folder that you specified above
        excelName1 = 'MECH331_Hardness.xlsx' #This is the intermediate Excel sheet that will let you see all the rounded and averaged values for each trial
        excelName2 = 'MECH331_Hardness_Cumulative.xlsx' #This is the MASTER excel sheet 

        #Starting the Work! Make sure you updated everyting above. 
        convLVM2CSV(folder_path) #this converts and updates all the csv files so that we have all the data that we care about and nothing else
        workFunc(folder_path,length,area,excelName1) #This function does all the heavy lifting of taking the CSV files and compiling them into one excel sheet
        cumulativeRes(folder_path,headers,nameConvention,excelName1, excelName2) #This function does a cool down where it takes the new excel sheet with all 
        #the data and compiles it into one excel sheet with just the data we actually care about which is the columns found in the headers variables
        plotMyCumulativeResults(folder_path,headers,excelName2,[0,1,2,3]) #This will plot each trial.
        #The last input is necessary to specify if you want to plot the extensometer data (0,1) and then just global displacement data (2,3)
        print('DONE')
    
    #Start to calculate using the other file.
    # Start updating the label
    update_text(0)


#Initialize first window widgets
lbl1_Initial_window()
btn1_Initial_window()
square_initial_window()


#execute the window population ALWAYS NEEDED!
root.mainloop()

#PsuedoCode
#1. Initial Window should ask the user for the filepath to the folder
    #It should be a button and then once the button is pressed the system dialog should appear to look for the folder
    #Once the folder is selected, It should populate a window that has a list of all the file names in the folder on the right
        #Create a check to make sure there are 2 xlsx files in there with different names
    #The left will have a label that shows the folder path
    #the left below the folder path label will have an entry box for the naming convention with instructions
    #Below the entry box is a submission box 
        #in the Background we should run a check of the files in the folder and then compare it to the naming convetion
            #make sure the file names are longer than the naming convetion
            #other edge cases
    #Once the user submits the naming convetion 
    #Ask the user for the name of the xlsx files in order of 1 and 2 Include instructions to the user why this is important
        #Check in the background that the files exist and throw an error to the user if that is not the case
    #Once this is done move on to window 2
#2. Second window has a list of the sheets in the cumulative file next to each name is a check box that allows for the user to select what they want graphed
    # The check boxes will have a ext, global, or both option
    # Once the selection is made there should be a Plot it Button on the bottom
    # Use Matplot to plot the data (Double check that it is possible to grab singular data points on the graph to calculate the E value manually)
        #With the option to export the plot as well!
    # Once a plot is populated a new box should populate that asks the user to input the X1, Y1 and X2 and Y2 values to calculate the E value

