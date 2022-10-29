from tkinter import *
from tkinter import messagebox
import random
import pyperclip        #used for copy/paste clipboard functions
import hashlib
from db import MainUser, ServicesPasswords, db, hash_pw
from AES256GCM import encrypt_AES_GCM , decrypt_AES_GCM


FONT = ("Courier", 12, "bold")




# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

#the canvas
canvas = Canvas(width=200, height=200)
mypass_img = PhotoImage(file="assets/logo.png")
canvas.create_image(100, 100, image=mypass_img)
canvas.grid(row=0, column=0)


# --------------------------------------------- BUILD PAGES ---------------------------------------------#

# --------------------------------------------- PAGE (1) ---------------------------------------------  #
class LoginPage():

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
    password1_input = Entry(width=25, show="*")
    password1_input.grid(row=3, column=1)

    # unlock button
    button = Button(window, text='UNLOCK')
    button.grid(row=3, column=2) 
    button.configure(command= lambda: LoginPage.unlock(
        LoginPage.username1_input, LoginPage.password1_input, LoginPage.username1, LoginPage.password1, LoginPage.button))

    def unlock(username1_input, password1_input, username1, password1, button):
        ##check Creds
        if username1_input.get() == "" or  password1_input.get() == "":
                messagebox.showinfo(title="Listen Up", message="No empty fields allowed!")
        else:
            users = db.session.query(MainUser).filter(MainUser.main_username == username1_input.get()).first()
            if users:
                hash_256 = hash_pw(password1_input.get(), "sha256")
                #key_512 = hash_pw(password1_input.get(), "sha512")
                if users.main_password == hash_256:
                    #destroy_old 
                    username1.destroy()
                    password1.destroy()
                    username1_input.destroy()
                    password1_input.destroy()
                    button.destroy()
                    #Go to PAGE (2)
                    PWMPage.build_page()
                else:
                    messagebox.showinfo(title="Listen Up", message="Wrong Password, try again!")
                    #FUTURE Enhancement1: we can do more here, for example max of 5 attempts to prevent BFA.
            else:
                answer = messagebox.askquestion("Unregistered User", "Do you want to create a new one?")
                if answer == "yes":
                    user = MainUser(main_username=username1_input.get(), main_password=  hash_pw(password1_input.get(), "sha256"))
                    db.add(user)
                    db.commit()


             

# --------------------------------------------- PAGE (2) --------------------------------------------- #
class PWMPage():

    # ---------------------------- ENTER SERVICE INFO ------------------------------- #
    def build_page():
        # website: label
        service = Label(text="Service: ", font=FONT)
        service.grid(row=1, column=0)

        # email/username label
        svc_username = Label(text="Username: ", font=FONT)
        svc_username.grid(row=2, column=0)

        # password: label
        svc_password = Label(text="Password: ", font=FONT)
        svc_password.grid(row=3, column=0)

        # website_input box
        service_input = Entry(width=35)
        service_input.focus()
        service_input.grid(row=1, column=1, columnspan=2)

        # username_input box
        svc_username_input = Entry(width=35)
        svc_username_input.grid(row=2, column=1, columnspan=2)

        # password_input box
        #password_input = Entry(width=20,show="*")
        svc_password_input = Entry(width=15)
        svc_password_input.grid(row=3, column=1)

        # generate password button
        gen_pass = Button(text="Generate password")
        gen_pass.grid(row=3, column=2)
        gen_pass.configure(command= lambda: PWMPage.generate_password(svc_password_input))

        # Add button
        add_svc_button = Button(text="Add", width=33)
        add_svc_button.grid(row=5, column=1,columnspan=2)
        add_svc_button.configure(command= lambda: PWMPage.add_toDB(service_input, svc_username_input, svc_password_input,))


    #encrypt and insert to db
    def add_toDB(service_input, svc_username_input, svc_password_input): 
        
        if service_input.get() == "" or svc_username_input.get() == "" or svc_password_input.get() == "":
            messagebox.showinfo(title="Listen Up", message="No empty fields allowed!")

        else:
            #encrypt password + save all service info to the database
            PWMPage.save_svc_password(service_input, svc_username_input, svc_password_input)


    # ---------------------------- PASSWORD GENERATOR ------------------------------- #
    def generate_password(svc_password_input):

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

        svc_password_input.delete(0,END)
        svc_password_input.insert(0,str(password))
    

    # ---------------------------- SAVE SERVICE INFO TO DB ------------------------------- #
    def save_svc_password(service_input, svc_username_input, svc_password_input):

        # (1) Encrypt Password with a random 256bit-key using ASE256 + GCM:
        msg = svc_password_input.get()
        encrypted_pw = encrypt_AES_GCM(msg.encode("utf-8"))
        print("encrypted_pw:" , encrypted_pw[0])

        # (2) Save Service info to DB with Encrypted Password:
        svc = ServicesPasswords(website= service_input.get(), service_username= svc_username_input.get(), service_password= encrypted_pw[0]) 
        db.add(svc)
        db.commit()

        # (3) Show all Services Info in the GUI with Decrypted Passwords:
        decrypted_pw = decrypt_AES_GCM(encrypted_pw)
        print("decrypted_pw:" , decrypted_pw)






# --------------------------------------------- APP LAUNCHER --------------------------------------------- #
LoginPage()
window.mainloop()