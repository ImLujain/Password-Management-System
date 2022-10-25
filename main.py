from tkinter import *
import sys
from tkinter import messagebox

window = Tk()
window.title("Password Manager")
window.config(padx=22, pady=22) #padding
#window.configure(background='white')

canvas = Canvas(width=250, height=250)
mypass_img = PhotoImage(file="assets/logo.png")
canvas.create_image(125, 125, image=mypass_img) #arg[0] x axis, arg[1] y axis
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


#entries
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
add_button = Button(text="Add") #command=add)
add_button.grid(row=4, column=2)

window.mainloop()