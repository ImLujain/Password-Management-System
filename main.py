from tkinter import *
import sys
from tkinter import messagebox


class MainApplication:

    def __init__(self, master):
        self.master = master
        self.master.title("Password Storage")


    def reset(self):
        self.master.withdraw()
        self.passwordsScreen = Toplevel(self.master)
        self.addPasswordLabel = Label(self.frame1, text="Add New Password", font=self.large_font)
        pass

    #Save Password
    def add(self): #this function we will write to database
        website = website_input.get()
        username = username_input.get()
        password = password_input.get()
        print(website, username, password)

        #key = 


    ########### CREATE GUI#############
    window = Tk()
    window.title("Password Manager")
    window.config(padx=22, pady=22) #padding
    #Window.configure(background='white')

    canvas = Canvas(width=200, height=200)
    mypass_img = PhotoImage(file="assets/logo.png")
    canvas.create_image(100, 100, image=mypass_img) #arg[0] x axis, arg[1] y axis
    #Canvas.pack()
    canvas.grid(row=0, column=1)

    #Labels
    website_label= Label(text="website")
    website_label.grid(row=1, column=0)
    #Website_label.configure(background='white')
    email_label = Label(text="Email/Username")
    email_label.grid(row=2, column=0)
    password_lable = Label(text="password")
    password_lable.grid(row=3, column=0)


    #Entries
    # Website_input box
    website_input = Entry(width=35)
    website_input.grid(row=1, column=1, columnspan=2)
    website_input.focus()

    # Username_input box
    username_input = Entry(width=35)
    username_input.grid(row=2, column=1, columnspan=2)
    username_input.insert(0, "example@example.com")
    # Password_input box
    password_input = Entry(width=20)
    password_input.grid(row=3, column=1)

    #Buttons
    # Generate password button
    gen_pass = Button(text="Generate password")
    gen_pass.grid(row=3, column=2)

    # Add button
    add_button = Button(text="Add", width=36, command=lambda:self.add())
    add_button.grid(row=4, column=1, columnspan=2)


    window.mainloop()