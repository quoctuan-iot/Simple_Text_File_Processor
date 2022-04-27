# Author: TuanTran 
# Github: https://github.com/quoctuan-iot
# Email: quoctuan.iot@gmail.com

from __future__ import barry_as_FLUFL
from tkinter import *
import os
from tkinter.font import BOLD
import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showwarning,showinfo, showerror


# Hide console when using with tkinter
#import win32gui, win32con
#hide = win32gui.GetForegroundWindow()
#win32gui.ShowWindow(hide , win32con.SW_HIDE)

class FileProcessor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.windowWidth = 700
        self.windowHeight = 400
        self.radioVar = IntVar()

        self.selectedFolder = True
        self.selectedFileOrFolder = False
        self.flagTxt = False
        self.flagWxt = False
        self.listFileTxt = []
        self.listFileWxt = []
        self.folderSelection = ''
        self.fileSelection = ''
        
        self.title('File Processor - Generator')
        self.resizable(False,False)
        self.showScreenCenter()
        #self.attributes('-toolwindow', True)

        # Creating a frames
        self.frameTitle = Frame(self)
        self.frameTitle.pack(padx=30,pady=30)

        self.frameChose = Frame(self,highlightbackground='black', highlightthickness=2)
        self.frameChose.pack(padx=30,pady=10)

        self.frameStatus = Frame(self)
        self.frameStatus.pack(padx=30,pady=10)

        self.frameButton = Frame(self)
        self.frameButton.pack(padx=30,pady=30)

        # Creating a title
        self.labelTitle = Label(self.frameTitle,text='File Processor/Generator',font=('Arial',30,BOLD))
        self.labelTitle.grid(row=0,column=0)

        # Crateing a label chose radioButton
        self.labelChose = Label(self.frameChose,text='Chose:',font=('Arial',15))
        self.labelChose.grid(column=0,row=1)

        self.radioFolder = Radiobutton(self.frameChose,text='Folder (Default)',variable=self.radioVar,value=1,command = self.callRadioChose, font=('Arial',15))
        self.radioFolder.select()
        self.radioFolder.grid(column=1,row=1,sticky='w')

        self.radioFile = Radiobutton(self.frameChose,text='File',variable=self.radioVar,value=0,command = self.callRadioChose, font=('Arial',15))
        self.radioFile.grid(column=1,row=2,sticky='w')
        
        # Creating a label status
        self.labelStatus = Label(self.frameStatus,font=('Arial',9),width=100,height=2,bg='white',anchor=W)
        self.labelStatus.grid(column=0,row=0)

        # Creating a button
        self.buttonSelection = Button(self.frameButton,text='Browse Folder or File',font=('Arial',15),command=self.callButtonBrowse)
        self.buttonSelection.grid(column=0,row = 0,padx=20)

        self.buttonStart = Button(self.frameButton,text='Start',font=('Arial',15),command=self.callButtonStart)
        self.buttonStart.grid(column=1,row = 0,padx=20)

    def showScreenCenter(self):
        # Getting screen width and height
        self.screenWidth = self.winfo_screenwidth()
        self.screenHeight = self.winfo_screenheight()

        x = int((self.screenWidth / 2) - (self.windowWidth / 2))
        y = int((self.screenHeight / 2) - self.windowHeight / 2)

        self.geometry('{}x{}+{}+{}'.format(self.windowWidth, self.windowHeight, x, y))

    def callRadioChose(self):
        radioSelection = self.radioVar.get()

        # Checking selection folder
        if radioSelection:
            self.selectedFolder = True
        else:
            self.selectedFolder = False

    def callButtonStart(self):
        # checking the folder or the file is selected
        if (self.selectedFileOrFolder):

            # Call generate file
            self.generateFileRxt()
            self.generateFileSxt()

            # Clean label status
            self.labelStatus.config(text='')

            showinfo(title = 'Infor',message='The file is generated completely')

        else:
            showwarning(title = 'Warning',message='Please select folder of file')
            
        # Reset flag selection file or folder
        self.selectedFileOrFolder = False

    def callButtonBrowse(self):
        # Handle button browse click event
        if (self.selectedFolder):
            self.folderSelection = fd.askdirectory()

            if (self.folderSelection == ''):
                showwarning(title='Warning',message='Please chose folder')
            else:
                # Update flag selection file or folder
                self.selectedFileOrFolder = True

                if (self.checkFileInputExist()):
                    self.labelStatus.config(text = self.folderSelection)
            
        else:
            self.folderSelection = ''
            self.filetypes = (('All files','*.*'),('Text files','*.txt'),
                                ('Write files','*.wxt'))

            self.fileSelection = fd.askopenfilenames(
                                    title='Open files',initialdir='/',
                                    filetypes=self.filetypes)

            if (self.fileSelection == ''):
                showwarning(title='Warning',message='Please chose files')

            else:
                # Update flag selection file or folder
                self.selectedFileOrFolder = True

                if (self.checkFileInputExist()):
                    self.labelStatus.config(text = '{},{}'.format(self.listFileTxt,self.listFileWxt))
                    for item in self.fileSelection[0].split('/')[:-1]:
                      self.folderSelection = self.folderSelection + item + '/'
                self.folderSelection = self.folderSelection[:-1]
                

    def checkFileInputExist(self):
        if (self.selectedFolder):
            for file in os.listdir(self.folderSelection):
                if (file.endswith(('.txt'))):
                    self.listFileTxt.append(file)
                    self.flagTxt = True

                if (file.endswith(('.wxt'))):
                    self.listFileWxt.append(file)
                    self.flagWxt = True
        else:
            for file in self.fileSelection:
                fileName = file.split('/')[-1]

                if (fileName.endswith(('.txt'))):
                    self.listFileTxt.append(fileName)
                    self.flagTxt = True

                if (file.endswith(('.wxt'))):
                    self.listFileWxt.append(fileName)
                    self.flagWxt = True

        if (self.flagTxt == False and self.flagWxt == True):
            showwarning(
                    title='Warning',
                    message="Files *.txt don't exist")
            return False

        elif (self.flagWxt == False and self.flagTxt == True):
            showwarning(
                    title='Warning',
                    message="Files * .wxt don't exist")
            return False

        elif (self.flagWxt == False and self.flagTxt == False):
            showwarning(
                    title='Warning',
                    message="Files *.txt and *.wxt don't exist")
            return False

        else:
            return True

    def generateFileRxt(self):
        try:
            # Loop all files in the list file Txt
            for fileName in self.listFileTxt:
                # Creating file paths
                pathFileTxt = self.folderSelection + '/' + fileName
                pathFileRxt = self.folderSelection + '/' + fileName.split('.')[0] + '.rxt'

                # Creating object read and write
                readLinesTxt = open(pathFileTxt).readlines()
                fileRxt = open(pathFileRxt,'w')
                
                # Declare local variable
                characterAddition = ''
                characterIndex = -1
                characterNumber = 1

                # Loop file to get data line by line
                for cnt, line in enumerate(readLinesTxt):
                    # Tool only add two characters: Example 'zz'
                    # If cnt > 701 lines, break writing file
                    if cnt > 701:
                        showwarning(
                                title='Warning',
                                message="File *.txt contains multiple lines (more than 701 lines), So wrong format file *.rxt ")
                        break

                    # Checking lines need to add character
                    if (cnt % 26 == 0 and cnt != 0):
                        characterNumber = cnt // 26 + 1
                        characterIndex = 0
                    else:
                        characterIndex = characterIndex + 1
                        characterNumber = cnt // 26 + 1

                    # Checking character number need to add
                    if characterNumber == 1:
                        characterAddition = chr(97 + characterIndex)
                    elif characterNumber >= 2:
                        characterAddition = chr(97 + characterNumber - 2) + chr(97 + characterIndex)

                    # Formating output data 
                    out_line = line.replace('\n','') + characterAddition + '\n'

                    # Writing a file Rxt
                    fileRxt.write(out_line)
                
                # Close a file
                fileRxt.close()

        except Exception as bug:
            showerror(title='Error',message='Please check the input file structure')

    def generateFileSxt(self):
        try:
            # Loop all files in the list file Txt
            for fileName in self.listFileTxt:
                # Creating file paths
                pathFileTxt = self.folderSelection + '/' + fileName
                pathFileWxt = self.folderSelection+ '/' + fileName.split('.')[0] + '.wxt'
                pathFileSxt = self.folderSelection + '/' + fileName.split('.')[0] + '.sxt'

                # Creating object read and write
                readLinesTxt = open(pathFileTxt).readlines()
                readLineWxt = open(pathFileWxt).readlines()
                fileSxt = open(pathFileSxt,'w')

                # Loop file to get data line by line
                for cnt, line in enumerate(readLinesTxt):
                    tmp = line.replace('\n','').split('\t')[0]

                    # Getting integral part and fractional part
                    integralPart = tmp.split('.')[0]
                    fractionalPart = tmp.split('.')[1]

                    # Converting seconds to hours:minutes:seconds
                    conversionResult = ('{},{}'.format(self.convertSecond2FormatTime(int(integralPart)),fractionalPart[0:3]))

                    # Only getting data of the first line, don't write
                    if cnt == 0:
                        previousConversionResult = conversionResult
                        continue
                    
                    # Formating output data 
                    lineOutput = '{} --> {}\n'.format(previousConversionResult,conversionResult)
                    
                    # Writing a file Sxt
                    fileSxt.write('{}\n'.format(cnt))
                    fileSxt.write(lineOutput)
                    fileSxt.write('{}\n'.format(readLineWxt[cnt-1]))

                    # Updating a conversion result
                    previousConversionResult = conversionResult

                # Close file
                fileSxt.close()

        except Exception as bug:
            showerror(title='Error',message='Please check the input file structure')

    def convertSecond2FormatTime(self,seconds):
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        result = '{}:{}:{}'.format(str(hour).zfill(2),str(minutes).zfill(2),str(seconds).zfill(2))
        return result
 
def main():
    fileProcessor = FileProcessor()
    fileProcessor.mainloop()
    
if __name__ == '__main__':
    main()