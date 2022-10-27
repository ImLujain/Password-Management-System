from tkinter import *
import sys
from tkinter import messagebox
##### IMPORT OUR CLASSES #####
import db
import login


class PasswordManagement:


    #Save Password
    def add(): #this function we will write to database
        website = website_input.get()
        username = username_input.get()
        password = password_input.get()
        
        #key = 

    ########### CREATE GUI#############
    #window = Tk()
    #window.title("Password Manager")
    #window.config(padx=100, pady=200) #padding
    #window.configure(background="white")
    
    canvas = Canvas(width=200, height=200)
    mypass_img = PhotoImage(file="assets/logo.png")
    canvas.create_image(100, 100, image=mypass_img) #arg[0] x axis, arg[1] y axis
    #canvas.pack()
    canvas.grid(row=0, column=1)
    #canvas.configure(background='white')
    
    #labels
    website_label= Label(text="website")
    website_label.grid(row=1, column=0)
    #website_label.configure(background='white')
    email_label = Label(text="Email/Username")
    email_label.grid(row=2, column=0)
    password_lable = Label(text="password")
    password_lable.grid(row=3, column=0)


    #Entries
    # website_input box
    website_input = Entry(width=35)
    website_input.grid(row=1, column=1, columnspan=2)
    website_input.focus()

    # username_input box
    username_input = Entry(width=35)
    username_input.grid(row=2, column=1, columnspan=2)
    username_input.insert(0, "example@example.com")
    # password_input box
    password_input = Entry(width=35 , show='*')
    password_input.grid(row=3, column=1, columnspan=2)

    #Buttons
    # generate password button
    gen_pass = Button(text="Generate password")
    gen_pass.grid(row=4, column=1, columnspan=2)
    
    # Add button
    add_button = Button(text="Add", width=20, command=add)
    add_button.grid(row=5, column=1, columnspan=2)

    #window.mainloop()