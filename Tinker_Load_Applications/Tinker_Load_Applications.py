#--------------------- a program to save apps and run them in row -----------------------------------
import tkinter as tk
from tkinter import filedialog, Text
import os

root = tk.Tk()
apps = []
PATH="/Users/Rani0/python_coding/Tinker_Load_Applications/"

#---- read the saved configuration file remove spaces
if os.path.isfile(PATH + 'Saved_Apps.txt'):
    print("Saved configuration found!")
    with open(PATH + 'Saved_Apps.txt','r') as f:
        tempApps = f.read()
        tempApps = tempApps.split(',')
        #loop on tempApps if there is spaces remove them
        apps= [x for x in tempApps if x.strip()]
        print("Saved Apps = " + str(apps))    
else:
    print("Creating new configuration file!") 
 
#------------------------------------------------ functions ------------------------------------------
#---- open and choose file app 
def addApp():
    #this for gives access to what inside the frame
    for widget in frame.winfo_children():
        widget.destroy()

    #open and choose file, only .exe or all files
    filename=filedialog.askopenfile(initialdir="/",title="Select File",
    filetypes=(("executables","*.exe"),("all files","*.*")))
    apps.append(filename.name)
    print(filename)
    for app in apps:
        lable = tk.Label(frame, text=app, bg ="gray")
        lable.pack()

#---- run the apps
def runApps():
    for app in apps:
        os.startfile(app)

#---- The big green screen as root
canvas = tk.Canvas(root , height=600,width=600,bg="#263D42" )
canvas.pack()

#---- the white attached to the root screen 
frame =tk.Frame(root,bg="white")
frame.place(relwidth=0.8, relheight=0.7, relx=0.1, rely=0.1)

#---- buttons attached to the root with padding, the pack is to attach
openFile = tk.Button(root , text="Open File" , padx=10 , pady=10 , fg="white" , bg ="#263D42",command=addApp)
openFile.pack()
runApps = tk.Button(root , text="Run Apps" , padx=10 , pady=10 , fg="white" , bg ="#263D42" , command=runApps)
runApps.pack()

for app in apps:
    Label = tk.Label(frame, text=app)
    Label.pack()

root.mainloop()

#---- write and save all the apps to txt file
with open('Saved_Apps.txt' ,'w') as f:
    for app in apps:
        f.write(app + ',')
		
print("New changes in code git test")