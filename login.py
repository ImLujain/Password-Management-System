from tkinter import *
import sys
#from tkinter import messagebox
import db

class Login:
    
    #Enter the main pw
    def enter_main_pw(): 
        #label
        enter_pw_label= Label(text="Enter Your Main Password")
        enter_pw_label.grid(row=1, column=0)
        enter_pw_label.configure(background='white')
        #entry
        pw_entry = Entry(width=35 , show='*')
        pw_entry.grid(row=2, column=0, columnspan=2)
        pw_entry.focus()
        #Buttons
        #(1) Login bttn
        login_bttn = Button(text="LOG IN")
        login_bttn.grid(row=3, column=0)
        #(2) Sign Up bttn
        signup_bttn = Button(text="SIGN UP")
        signup_bttn.grid(row=3, column=2)
        #(3) Reset bttn
        login_bttn = Button(text="Reset Password ?")
        login_bttn.grid(row=4, column=1)


    #Create hash(1) from the main pw
    #def create_hash1():
        
    #Store hash(1) in db 
    #def store_hash1(): 
        
        

    


     