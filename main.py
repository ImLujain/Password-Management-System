from tkinter import *
from tkinter import messagebox
import random
import pyperclip        #used for copy/paste clipboard functions
from db import MainUser, ServicesPasswords, db, hash_pw 
from AES256GCM import encrypt_AES_GCM , decrypt_AES_GCM

key_256 = ""
FONT = ("Courier", 12, "bold")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title(" Secured Password Manager")
window.config(padx=20, pady=20)

#the canvas
canvas = Canvas(width=200, height=200)
mypass_img = PhotoImage(file="assets/logo.png")
canvas.create_image(100, 100, image=mypass_img)
canvas.grid(row=0, column=0)


# --------------------------------------------- BUILD PAGES ---------------------------------------------#

# --------------------------------------------- PAGE (1) ---------------------------------------------  #
class LoginPage():

    def login_builder():
        # email/username label
        username1 = Label(text="Username: ", font=FONT)
        username1.grid(row=2, column=0)

        # username_input box
        username1_input = Entry(width=35)
        username1_input.grid(row=2, column=1, columnspan=2)

        # password: label
        password1 = Label(text="Password: ", font=FONT)
        password1.grid(row=3, column=0)

        # password_input box
        password1_input = Entry(width=24, show="*")
        password1_input.grid(row=3, column=1)

        # Reset Password Button 
        reset_button = Button(text="Reset Password ?", width=32)
        reset_button.grid(row=4, column=1, columnspan=2) 
        reset_button.configure(command= lambda:LoginPage.build_page_reset_password())

        # unlock button
        button = Button(window, text='UNLOCK')
        button.grid(row=3, column=2) 
        button.configure(command= lambda: LoginPage.unlock(username1_input, password1_input, username1, password1, button, reset_button))
        


    def unlock(username1_input, password1_input, username1, password1, button, reset_button):
        
        # Check Creds:
        if username1_input.get() == "" or  password1_input.get() == "":
                messagebox.showinfo(title="Listen Up", message="No empty fields allowed!")
        else:
            #main_user = db.session.query(MainUser).filter(MainUser.main_username == username1_input.get()).first()
            main_user = MainUser.get(1)
            #print(main_user.main_username)

            # (1) DB is empty: 
            if main_user == None :
                answer = messagebox.askquestion("Unregistered User", "No main user for this app yet, do you want to be the main user?")
                if answer == "yes":
                    user = MainUser(main_username=username1_input.get(), main_password=  hash_pw(password1_input.get(), "sha512"))                                            
                    db.add(user)
                    db.commit()

            # (2) DB contains the main user already: 
            elif main_user.main_username == username1_input.get():
                # Prepare hashs:
                hash_512 = hash_pw(password1_input.get(), "sha512")
                key_256 = hash_pw(password1_input.get(), "sha256")

                if main_user.main_password == hash_512:
                    #destroy_old 
                    username1.destroy()
                    password1.destroy()
                    username1_input.destroy()
                    password1_input.destroy()
                    button.destroy()
                    reset_button.destroy()
                    #Go to PAGE (2) + Send the encryption key to be used for services passwords encryption 
                    PWMPage.build_page(key_256)
                else:
                    messagebox.showinfo(title="Listen Up", message="Wrong Password, try again!")
                    #FUTURE Enhancement1: we can do more here, for example max of 5 attempts to prevent BFA.
            
            # (3) Another user trying to access the app (unauthorized user): 
            else:
                messagebox.showinfo(title="Listen Up", message="INVALID USERNAME: You are not the authorized user to use this app!")
                


   
    def build_page_reset_password():

        reset_pass_window = Toplevel()

        #the canvas
        canvas = Canvas(reset_pass_window ,width=200, height=200)
        mypass_img = PhotoImage(file="assets/logo.png")
        canvas.create_image(100, 100, image=mypass_img)
        canvas.grid(row=0, column=0)
        reset_pass_window.title(" Change Password")
        reset_pass_window.config(padx=20, pady=20)

        # old_pass: label
        old_pass = Label(reset_pass_window, text="Old Password: ", font=FONT)
        old_pass.grid(row=1, column=0)

        # old_pass_input box
        old_pass_input = Entry(reset_pass_window, width=25, show="*")
        old_pass_input.grid(row=1, column=1)

        # new_pass: label
        new_pass = Label(reset_pass_window, text="New Password: ", font=FONT)
        new_pass.grid(row=2, column=0)

        # new_pass_input box
        new_pass_input = Entry(reset_pass_window, width=25, show="*")
        new_pass_input.grid(row=2, column=1)

        # Password reset Button
        reset_button = Button(reset_pass_window, text="Reset", width=22)
        reset_button.grid(row=3, column=1) 

        reset_button.configure(command= lambda:LoginPage.reset_password(old_pass_input.get(), new_pass_input.get()))
        
        reset_pass_window.mainloop()
        


    def reset_password(old_pass_input, new_pass_input):
        # Reset password: 
        # (1) Get old main user info form db:
        main_user = MainUser.query().first()

        # (2) check:
        if old_pass_input == "" or  new_pass_input == "":
                messagebox.showinfo(title="Listen Up", message="No empty fields allowed!")

        else:
            # Prepare (old) hashs:
            old_hash_512 = hash_pw(old_pass_input, "sha512")
            old_key_256 = hash_pw(old_pass_input, "sha256")
            old_secretKey_half = old_key_256[:int(len(old_key_256)/2)].encode("utf-8")

            # Prepare (new) hashs:
            new_hash_512 = hash_pw(new_pass_input, "sha512")
            new_key_256 = hash_pw(new_pass_input, "sha256")
            new_secretKey_half = new_key_256[:int(len(new_key_256)/2)].encode("utf-8")
            
            if main_user.main_password != old_hash_512 :
                messagebox.showinfo(title="Listen Up", message="The old password is incorrect, try again!")

            else: 
                # Now, user is authorized to reset password ...
                main_user.main_password = new_hash_512
                db.session.commit()

                # Now, user is authorized to re-encrypt services passwords with the new key (decrypt with old key first) ...
                for password in ServicesPasswords.query():
                    decryption_info = ( password.service_password , password.nonce , password.authTag)
                    decrypted_pass = decrypt_AES_GCM(decryption_info , old_secretKey_half)
                    encrypted_pass = encrypt_AES_GCM(decrypted_pass , new_secretKey_half)
                    password.service_password= encrypted_pass[0]
                    password.nonce= encrypted_pass[1]
                    password.authTag= encrypted_pass[2]

                    db.session.commit()

                messagebox.showinfo(title="Listen Up", message="Main Password Updated Successfully!")




# --------------------------------------------- PAGE (2) --------------------------------------------- #
class PWMPage():

    def build_page(key_256):
        # service: label
        service = Label(text="Service: ", font=FONT)
        service.grid(row=1, column=0)

        # email/username label
        svc_username = Label(text="Username: ", font=FONT)
        svc_username.grid(row=2, column=0)

        # password: label
        svc_password = Label(text="Password: ", font=FONT)
        svc_password.grid(row=3, column=0)

        # service_input box
        service_input = Entry(width=35)
        service_input.focus()
        service_input.grid(row=1, column=1, columnspan=2)

        # username_input box
        svc_username_input = Entry(width=35)
        svc_username_input.grid(row=2, column=1, columnspan=2)

        # password_input box
        svc_password_input = Entry(width=15)
        svc_password_input.grid(row=3, column=1)

        # generate password button
        gen_pass = Button(text="Generate Password")
        gen_pass.grid(row=3, column=2)
        gen_pass.configure(command= lambda: PWMPage.generate_password(svc_password_input))

        # Add button
        add_svc_button = Button(text="Add", width=12)
        add_svc_button.grid(row=5, column=1)
        add_svc_button.configure(command= lambda: PWMPage.add_toDB(service_input, svc_username_input, svc_password_input, key_256))

        # Show Passwords Button 
        show_pass_button = Button(text="Show Passwords", width=16)
        show_pass_button.grid(row=5, column=2)
        show_pass_button.configure(command= lambda:ShowPWPage.show_passwords_page(key_256))

        # SIGN OUT Button 
        signout_button = Button(text="SIGN OUT", width=32)
        signout_button.grid(row=6, column=1, columnspan=2)
        signout_button.configure(command= lambda: back_to_loginpage())
        def back_to_loginpage():
            #destroy_old 
            service.destroy()
            svc_username.destroy()
            svc_password.destroy()
            service_input.destroy()
            svc_username_input.destroy()
            svc_password_input.destroy()
            gen_pass.destroy()
            add_svc_button.destroy()
            show_pass_button.destroy()
            signout_button.destroy()
            LoginPage.login_builder()
            
        


    # Encrypt and insert to db
    def add_toDB(service_input, svc_username_input, svc_password_input, key_256): 
        
        if service_input.get() == "" or svc_username_input.get() == "" or svc_password_input.get() == "":
            messagebox.showinfo(title="Listen Up", message="No empty fields allowed!")

        else:
            # (1) Encrypt Password with a random 256bit-key using ASE256 + GCM:
            msg = svc_password_input.get()
            secretKey_half = key_256[:int(len(key_256)/2)].encode("utf-8") # ASE-256 only accepts key size (32 byte) ...
                                                                           # which is half of the sha256 value after encoding (64 byte)
            encrypted_pw = encrypt_AES_GCM(msg.encode("utf-8") , secretKey_half)

            # (2) Save Service info to DB with Encrypted Password:
            svc = ServicesPasswords(service= service_input.get(), service_username= svc_username_input.get(), 
                                    service_password= encrypted_pw[0], nonce= encrypted_pw[1], authTag= encrypted_pw[2]) 
            db.add(svc)
            db.commit()

            messagebox.showinfo(title="Listen Up", message="New entry has been added successfully!")

        



    def generate_password(svc_password_input):

        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 
                    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 
                    'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 
                    'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 
                    'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

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




# --------------------------------------------- PAGE (3) --------------------------------------------- #
class ShowPWPage():

    def show_passwords_page(key_256):
        secretKey_half = key_256[:int(len(key_256)/2)].encode("utf-8")
        svc_list = db.session.query(ServicesPasswords).all()

        pass_window = Toplevel(window)
        #the canvas
        canvas = Canvas(pass_window ,width=200, height=200)
        mypass_img = PhotoImage(file="assets/logo.png")
        canvas.create_image(100, 100, image=mypass_img)
        canvas.grid(row=0, column=0)
        pass_window.title("passwords list")
        pass_window.config(padx=20, pady=20)

        # service: label
        service = Label(pass_window, text="Service: ", font=FONT)
        service.grid(row=1, column=0)

        # email/username label
        svc_username = Label(pass_window, text="Username: ", font=FONT)
        svc_username.grid(row=1, column=2)

        # password: label
        svc_password = Label(pass_window, text="Password: ", font=FONT)
        svc_password.grid(row=1, column=4 )
        row = 2
        for svc in svc_list:
            decryption_info = ( svc.service_password , svc.nonce , svc.authTag)
            e = Label(pass_window, text=svc.service, font=FONT)
            e.grid(row=row, column=0)
            e = Label(pass_window, text=svc.service_username, font=FONT)
            e.grid(row=row, column=2)
            e = Label(pass_window, text=decrypt_AES_GCM(decryption_info , secretKey_half), font=FONT)
            e.grid(row=row, column=4)

            row=row+1

        pass_window.mainloop()




# >>>>>>>>>>>>>>>>>>>>>>>>>>> APP LUNCHER <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< #
LoginPage.login_builder()
window.mainloop()