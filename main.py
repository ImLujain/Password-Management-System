from tkinter import *
from tkinter import messagebox
import random
import pyperclip        #used for copy/paste clipboard functions
from db import MainUser, ServicesPasswords, db, hash_pw #, decrypt_passwords
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

                hash_512 = hash_pw(password1_input.get(), "sha512")
                key_256 = hash_pw(password1_input.get(), "sha256")
            
                if users.main_password == hash_512:
                    ### TEST
                    print("Main user Password (hash512):" , hash_512)
                    print("Encryption KEY (hash256):" , key_256)
                    print("---------------------------------------------------")
                    ### END TEST
                    #destroy_old 
                    username1.destroy()
                    password1.destroy()
                    username1_input.destroy()
                    password1_input.destroy()
                    button.destroy()
                    #Go to PAGE (2) + Send the encryption key to be used for services passwords encryption 
                    PWMPage.build_page(key_256)
                else:
                    messagebox.showinfo(title="Listen Up", message="Wrong Password, try again!")
                    #FUTURE Enhancement1: we can do more here, for example max of 5 attempts to prevent BFA.
            else:
                answer = messagebox.askquestion("Unregistered User", "Do you want to create a new one?")
                if answer == "yes":
                    user = MainUser(main_username=username1_input.get(), main_password=  hash_pw(password1_input.get(), "sha512"))
                    db.add(user)
                    db.commit()


             

# --------------------------------------------- PAGE (2) --------------------------------------------- #
class PWMPage():
    @staticmethod
    def enc_pass(msg, key_256 ):
        secretKey_half = key_256[:int(len(key_256)/2)].encode("utf-8") # ASE-256 only accepts key size (32 byte) which is half of the sha256 value (64 byte)
        encrypted_pw = encrypt_AES_GCM(msg, secretKey_half)
        return encrypted_pw
    @staticmethod
    def enc_dec(key_256, new_pass):
        print(new_pass)
        hash_512 = hash_pw(new_pass, "sha512")
        print(hash_512)
        new_key_256 = hash_pw(new_pass, "sha256")
        secretKey_half = key_256[:int(len(key_256)/2)].encode("utf-8") # ASE-256 only accepts key size (32 byte) which is half of the sha256 value (64 byte)
        user = MainUser.query().first()
        user.main_password = hash_512
        db.session.commit()
        print("TEST: DECRYPT ALL PASSWORDS AND SHOW THEM ..... ")
        id = 0
        for password in ServicesPasswords.query():
            decryption_info = ( password.service_password , password.nonce , password.authTag)
            decrypted_pass = decrypt_AES_GCM(decryption_info , secretKey_half)
            encrypted_pass = PWMPage.enc_pass(decrypted_pass, new_key_256)
            password.service_password= encrypted_pass[0]
            password.nonce= encrypted_pass[1]
            password.authTag= encrypted_pass[2]

            db.session.commit()

            id = id + 1
        

        
            #print("Decrypted Password " , id , ":" , decrypt_AES_GCM(decryption_info , secretKey_half))
        print("---------------------- #### END #### ----------------------")

        


    # ---------------------------- ENTER SERVICE INFO ------------------------------- #
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
        #password_input = Entry(width=20,show="*")
        svc_password_input = Entry(width=15)
        svc_password_input.grid(row=3, column=1)

        # generate password button
        gen_pass = Button(text="Generate password")
        gen_pass.grid(row=3, column=2)
        gen_pass.configure(command= lambda: PWMPage.generate_password(svc_password_input))

        # Add button
        add_svc_button = Button(text="Add", width=14)
        add_svc_button.grid(row=5, column=1)
        add_svc_button.configure(command= lambda: PWMPage.add_toDB(service_input, svc_username_input, svc_password_input, key_256))

        # Show Passwords Button 

        show_pass_button = Button(text="show Passwords", width=14)
        show_pass_button.grid(row=5, column=2)
        show_pass_button.configure(command= lambda:pages.show_passwords_page(key_256))


        # Reset Password Button 

        reset_button = Button(text="change password")
        reset_button.grid(row=0, column=2) 
        reset_button.configure(command= lambda:pages.change_password_page(key_256))



    #encrypt and insert to db
    def add_toDB(service_input, svc_username_input, svc_password_input, key_256): 
        
        if service_input.get() == "" or svc_username_input.get() == "" or svc_password_input.get() == "":
            messagebox.showinfo(title="Listen Up", message="No empty fields allowed!")

        else:
            # encrypt password + save all service info to the database
            PWMPage.save_svc_password(service_input, svc_username_input, svc_password_input, key_256)


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
    def save_svc_password(service_input, svc_username_input, svc_password_input, key_256):
        global secretKey_half
        # (1) Encrypt Password with a random 256bit-key using ASE256 + GCM:
        msg = svc_password_input.get()
        secretKey_half = key_256[:int(len(key_256)/2)].encode("utf-8") # ASE-256 only accepts key size (32 byte) which is half of the sha256 value (64 byte)
        encrypted_pw = encrypt_AES_GCM(msg.encode("utf-8") , secretKey_half)
        print("encrypted_pw:" , encrypted_pw[0])

        # (2) Save Service info to DB with Encrypted Password:
        svc = ServicesPasswords(service= service_input.get(), service_username= svc_username_input.get(), 
                                service_password= encrypted_pw[0], nonce= encrypted_pw[1], authTag= encrypted_pw[2]) 
        db.add(svc)
        db.commit()

        # (3) Show all Services Info in the GUI with Decrypted Passwords:
        decrypted_pw = decrypt_AES_GCM(encrypted_pw , secretKey_half)
        print("decrypted_pw:" , decrypted_pw)

        # Decrypt and show all passwords:
        # (1) We have to retrive not only the ciphertext (encrypted_pw[0]) , but also the nonce (encrypted_pw[1]) and authTag (encrypted_pw[2]) for each password
        # (2) These three parametrs have to be sent to decrypt_AES_GCM() fonction in a tuple along with the secretKey_half
        # NOTE : we need to save into db the encrypted password and also the nonce (encrypted_pw[1]) and authTag (encrypted_pw[2])
        #        Since they are being changed with each password, no worries if they were public/known or stored in the db
        #        ONLY the KEY has to remain secret !!
        print("---------------------- #### ADD PASSWORD #### ----------------------")
        print("TEST: DECRYPT ALL PASSWORDS AND SHOW THEM ..... ")
        id = 0
        for all_svc_info in ServicesPasswords.query():
            decryption_info = ( all_svc_info.service_password , all_svc_info.nonce , all_svc_info.authTag)
            id = id + 1
            print("Decrypted Password " , id , ":" , decrypt_AES_GCM(decryption_info , secretKey_half))
        print("---------------------- #### END #### ----------------------")



# --------------------------------------------- APP LAUNCHER --------------------------------------------- #
class pages():

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


    def change_password_page(key_256):
        secretKey_half = key_256[:int(len(key_256)/2)].encode("utf-8")
        svc_list = db.session.query(ServicesPasswords).all()

        change_pass_window = Toplevel()
        #the canvas
        canvas = Canvas(change_pass_window ,width=200, height=200)
        mypass_img = PhotoImage(file="assets/logo.png")
        canvas.create_image(100, 100, image=mypass_img)
        canvas.grid(row=0, column=0)
        change_pass_window.title(" Change Password")
        change_pass_window.config(padx=20, pady=20)
        # Change_pass: label
        change_pass = Label(change_pass_window, text="New Password: ", font=FONT)
        change_pass.grid(row=1, column=0)
        # Password_input box
        update_input = Entry(change_pass_window, width=15)
        update_input.grid(row=1, column=1)
        
        # Password change Button

        update_button = Button(change_pass_window, text="update")
        update_button.grid(row=2, column=1) 
        # if update_input.get() == "" :
        #     messagebox.showinfo(title="Listen Up", message="No empty fields allowed here!")
        # else:
        update_button.configure(command= lambda:PWMPage.enc_dec(key_256, update_input.get()))
        change_pass_window.mainloop()


LoginPage()
window.mainloop()