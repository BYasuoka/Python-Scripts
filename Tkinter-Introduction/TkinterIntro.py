#Brenton Yasuoka
#This is my genuine learning of Tkinter on 11-23-24
#Label not showing solution from Reddit: https://www.reddit.com/r/learnpython/comments/13gj1eh/label_not_showing_in_tkinter/ 

#Future of this file: I really want to figure out a way to always have the text centered at the moment this is not necessary
#because I feel I have the basic skills to start coding the GUI for my StressvStrain File.

import tkinter as tk
import time as clock
from tkinter import filedialog
from tkinter.messagebox import showinfo

root = tk.Tk() #create the root window
root.title('Welcome to my first GUI') #Root title
root.geometry('300x300') #size of the GUI window
#root.configure(bg="black")  # Set the root window background to black

#Function to display text when button is clicked
def click(event = None): 
    use_in = txt.get()
    if use_in != '':
        if use_in == 'Password':
            lbl.configure(text = 'Sigining In') #reconfigures the variable lbl with the message to the user
            root.after(2000) #this is me trying to wait for the Signing In to re-populate but it doesn't work
            for widget in root.winfo_children(): #for Loop to destroy all the widgets in the root window
                widget.destroy()
            load_new_widgets() #calling the function to load the new widgets
        else:
            lbl.configure(text = 'Sign In Unsuccessful Try Again')
            lbl.grid(column = 1, row = 0, padx = 50) #Prevents the shifting of everything

#Function to load new widgets once password is entered
def load_new_widgets():
    lbl = tk.Label(root, text = 'Welcome to your bank account')
    lbl.grid(column = 1, row = 0, padx = 50)
    btn = tk.Button(root, text = 'Load Account Balance', command = accBalanceLbl)
    btn.grid(column = 1, row = 2,padx = 50)

#Function to show the balance of the user once the new window is opened
def accBalanceLbl():
    newLbl = tk.Label(root, text = '$100,000')
    newLbl.grid(column = 1, row = 3, padx = 50)

##Iniital Root Window Widgets (needs to be below click[Function] because click is called in btn)

# Create and configure a label
lbl = tk.Label(root, text='Type Password')
lbl.grid(column = 1, row = 0, padx = 100) #default is C = 0 R = 0
#lbl.pack() #I think this just centers the text. Not useful all the time I think

#Button widget with red color text
btn = tk.Button(root, text = 'Sign In', fg = 'red', command = click)
btn.grid(column = 1, row = 2,padx = 100)

#Adding an entry field
txt = tk.Entry(root, width = 10)
txt.grid(column = 1, row = 1,padx = 100)

#Configures the Return key to act as the submit button
root.bind('<Return>', click) 

#Function that asks the user to find a folder and saves the filepath to the folder
def folderPath():
    filepath = filedialog.askdirectory(initialdir = '/', title = "Select a file") #, filetypes = (("Text files",'*.txt'),("All files,",'*.*'))
    showinfo(title = 'Selected Files', message = filepath)
    if filepath: 
        print('Selected File:',filepath)

## How to open and create new window with the menu bar

#Opens a new window (needs to be above the Menu Bar Definitions Below)
    #three options for defining the widgets in this new window
    #1. Define the widgets in the function 
    #2. Create a second function that is called in the first that creates the widgets
    #3. Can use classes that has a function inside this is best if mutliple windows with the same layout is being used
def openNewWindow():
    newWindow = tk.Toplevel(root)
    newWindow.title('New Window my Second GUI')
    newWindow.geometry('300x300')
    btn2 = tk.Button(newWindow,text = 'Open Folder', command = folderPath)
    btn2.grid(column = 1, row = 2,padx = 100)

#Menu Bar in root window
    #this creates the menu bar at the top. File is what we will see in the bar and new is the option we see when we hover over File
menu = tk.Menu(root)
item = tk.Menu(menu)
item.add_command(label = 'Folder Finder', command = openNewWindow)
menu.add_cascade(label = 'Window', menu = item)
root.config(menu=menu)

#execute the window population ALWAYS NEEDED!
root.mainloop()
