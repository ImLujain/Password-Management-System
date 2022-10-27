from tkinter import *
import sys
##### IMPORT OUR CLASSES #####
import db
from login import *


class MainApplication:

    ########### CREATE GUI #############
    window = Tk()
    window.title("Password Manager")
    window.config(padx=100, pady=200) #padding
    window.configure(background="white")
    #window.configure(background="assets/bg1.jpg")
    
    #Class/Function calls:
    Login.enter_main_pw()


    ########### Finish the program ###########
    window.mainloop()