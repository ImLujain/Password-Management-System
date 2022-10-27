from tkinter import *
from tkinter import messagebox
import random
import pyperclip        #used for copy/paste clipboard functions
import hashlib
from db import db, User, hash_main_pw


FONT = ("Courier", 12, "bold")




# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)


#the canvas
canvas = Canvas(width=200, height=200)
mypass_img = PhotoImage(file="assets/logo.PNG")
canvas.create_image(100, 100, image=mypass_img)
canvas.grid(row=0, column=0)

def login_page():
    def add_password_page():

    # ---------------------------- SAVE PASSWORD ------------------------------- #

        def add(): #3ncrypt and insert to db

            website = website_input.get()
            print(website)

            if website_input.get() == "" or website_input.get() == "" or password_input.get() == "":
                messagebox.showinfo(title="Listen Up", message="no empty fields allowed")

            else:
                pass
                #encrypt them and save them to the database
        # ---------------------------- PASSWORD GENERATOR ------------------------------- #
        # Password Generator
        def generate_password():

            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
            numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

            nr_letters = random.randint(8, 10)
            nr_symbols = random.randint(2, 4)
            nr_numbers = random.randint(2, 4)

            password_list = []

            [password_list.append(random.choice(letters)) for _ in range(nr_letters)]
            [password_list.append(random.choice(symbols)) for _ in range(nr_symbols)]
            [password_list.append(random.choice(numbers)) for _ in range(nr_numbers)]

            random.shuffle(password_list)
            password = "".join(password_list)

            pyperclip.copy(password)

            password_input.delete(0,END)
            password_input.insert(0,str(password))
        
        def save_password():
            website = website_input.get()
            username = username_input.get()
            password = password_input.get()

        ##check Creds
        if username1_input.get() == "" or  password1_input.get() == "":
                messagebox.showinfo(title="Listen Up", message="no empty fields allowed")
        else:
            users = db.session.query(User).filter(User.username == username1_input.get()).first()
            if users:
                hashed = hash_main_pw(password1_input.get(), "sha256")
                if users.password == hashed:


                    #destroy_old 
                    username1.destroy()
                    password1.destroy()
                    button.destroy()
                    # website: label
                    website = Label(text="Website: ", font=FONT)
                    website.grid(row=1, column=0)

                    # email/username label
                    username = Label(text="Email/Username: ", font=FONT)
                    username.grid(row=2, column=0)

                    # password: label
                    password = Label(text="Password: ", font=FONT)
                    password.grid(row=3, column=0)

                    # website_input box
                    website_input = Entry(width=35)
                    website_input.focus()
                    website_input.grid(row=1, column=1, columnspan=2)

                    # username_input box
                    username_input = Entry(width=35)
                    username_input.grid(row=2, column=1, columnspan=2)

                    # password_input box
                    #password_input = Entry(width=20,show="*")
                    password_input = Entry(width=20)
                    password_input.grid(row=3, column=1)

                    # generate password button
                    gen_pass = Button(text="Generate password", command=generate_password)
                    gen_pass.grid(row=3, column=2)

                    # Add button
                    add_button = Button(text="Add", width=35, command=add)
                    add_button.grid(row=5, column=1,columnspan=3)
            else:
                answer = messagebox.askquestion("Unregistered User", "Do you want to create a new one?")
                if answer == "yes":
                    user = User(username=username1_input.get(), password=  hash_main_pw(password1_input.get(), "sha256"))
                    db.add(user)
                    db.commit()

    #username: label

    # email/username label
    username1 = Label(text="Email/Username: ", font=FONT)
    username1.grid(row=2, column=0)
    # username_input box
    username1_input = Entry(width=35)
    username1_input.grid(row=2, column=1, columnspan=2)
    # password: label
    password1 = Label(text="Password: ", font=FONT)
    password1.grid(row=3, column=0)
    # password_input box
    #password_input = Entry(width=20,show="*")
    password1_input = Entry(width=20)
    password1_input.grid(row=3, column=1)
    # unlock button
    button = Button(window, text='UNLOCK', command=add_password_page)
    button.grid(row=3, column=4)


 
 
login_page()
window.mainloop()