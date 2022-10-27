from tkinter import *
import sys
from tkinter import messagebox

class MainApplication:

#Save Password
    def add(): #this function we will write to database
        website = website_input.get()
        username = username_input.get()
        password = password_input.get()
        print(website)

        #key = 


    ########### CREATE GUI#############
    window = Tk()
    window.title("Password Manager")
    window.config(padx=22, pady=22) #padding
    #window.configure(background='white')

    # the canvas
    canvas = Canvas(width=200, height=200)
    mypass_img = PhotoImage(file="assets/logo.PNG")
    canvas.create_image(100, 100, image=mypass_img)
    canvas.grid(row=0, column=1)

    # website: label
    website = Label(text="Website: ",)
    website.grid(row=1, column=0)

    # email/username label
    username = Label(text="Email/Username: ")
    username.grid(row=2, column=0)

    # password: label
    password = Label(text="Password: ")
    password.grid(row=3, column=0)

    # website_input box
    website_input = Entry(width=35)
    website_input.grid(row=1, column=1, columnspan=2)

    # username_input box
    username_input = Entry(width=35)
    username_input.grid(row=2, column=1, columnspan=2)

    # password_input box
    password_input = Entry(width=20)
    password_input.grid(row=3, column=1)

    # generate password button
    gen_pass = Button(text="Generate password")
    gen_pass.grid(row=3, column=2)

    # Add button
    add_button = Button(text="Add", command=add)
    add_button.grid(row=4, column=2)

    window.mainloop()