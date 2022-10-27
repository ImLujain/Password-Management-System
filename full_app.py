from cgi import print_directory
import tkinter as tk
from tkinter import ttk
from tkinter import *
import sys
from tkinter import messagebox
import hashlib
import db


LARGEFONT =("Verdana", 40)

class tkinterApp(tk.Tk):
	
	# __init__ function for class tkinterApp
	def __init__(self, *args, **kwargs):
		
		# __init__ function for class Tk
		tk.Tk.__init__(self, *args, **kwargs)
		
		# creating a container
		container = tk.Frame(self)
		container.pack(side = "top", fill = "both", expand = True)

		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		

		# initializing frames to an empty array
		self.frames = {}

		# iterating through a tuple consisting
		# of the different page layouts
		for F in (StartPage, Page1PWM, Page2ResetPW, Page3NewPW):

			frame = F(container, self)

			# initializing frame of that object from
			# startpage, page1, page2 respectively with
			# for loop
			self.frames[F] = frame

			frame.grid(row = 0, column = 0, sticky ="nsew")

		self.show_frame(StartPage)

	# to display the current frame passed as
	# parameter
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

# first window frame startpage

class StartPage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		# Lable 1
		label_1 = ttk.Label(self, text ="Enter Your Main Password", font = LARGEFONT)
		label_1.grid(row = 0, column = 0, padx = 10, pady = 10)

		# Entry 1
		main_pw = ttk.Entry(self, width=25 , show='*')
		main_pw.grid(row=1, column=0, padx = 10, pady = 10)
		hashed_pw = main_pw.get()
		#hashed_pw = self.hash_main_pw(main_pw.get())
		print(hashed_pw)

		# Button 1 : Enter
		bttn1_enter = ttk.Button(self, text ="UNLOCK",
		command = lambda : controller.show_frame(Page1PWM))
		#cmd2_hash256_512 = lambda : controller.(self.hash_main_pw(main_pw.get())))

		bttn1_enter.grid(row = 2, column = 0, padx = 10, pady = 10)

		# Button 2 : Forget your main password?
		bttn2_forget_pw = ttk.Button(self, text ="Forget your main password?",
		command = lambda : controller.show_frame(Page2ResetPW))
		bttn2_forget_pw.grid(row = 3, column = 0, padx = 10, pady = 10)

		# Button 3 : New to Password Manager?
		bttn3_new_pw = ttk.Button(self, text ="New to Password Manager?",
		command = lambda : controller.show_frame(Page3NewPW))
		bttn3_new_pw.grid(row = 4, column = 0, padx = 10, pady = 10)
	
	
	def hash_main_pw(main_pw):
		# SHA-256 hash of the password
		hash256 = hashlib.sha256(main_pw.encode('utf-8')).hexdigest()
		# SHA-512 hash of the password
		hash512 = hashlib.sha512(main_pw.encode('utf-8')).hexdigest()

		
		

# second window frame page1
class Page1PWM(tk.Frame):
	
	def __init__(self, parent, controller):
		
		tk.Frame.__init__(self, parent)
		label = ttk.Label(self, text ="Page 1", font = LARGEFONT)
		label.grid(row = 0, column = 4, padx = 10, pady = 10)

		# button to show frame 2 with text
		# layout2
		button1 = ttk.Button(self, text ="StartPage",
							command = lambda : controller.show_frame(StartPage))
	
		# putting the button in its place
		# by using grid
		button1.grid(row = 1, column = 1, padx = 10, pady = 10)

		# button to show frame 2 with text
		# layout2
		button2 = ttk.Button(self, text ="Page 2",
							command = lambda : controller.show_frame(Page2ResetPW))
	
		# putting the button in its place by
		# using grid
		button2.grid(row = 2, column = 1, padx = 10, pady = 10)





# third window frame page2
class Page2ResetPW(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = ttk.Label(self, text ="Page 2", font = LARGEFONT)
		label.grid(row = 0, column = 4, padx = 10, pady = 10)

		# button to show frame 2 with text
		# layout2
		button1 = ttk.Button(self, text ="Page 1",
							command = lambda : controller.show_frame(Page1PWM))
	
		# putting the button in its place by
		# using grid
		button1.grid(row = 1, column = 1, padx = 10, pady = 10)

		# button to show frame 3 with text
		# layout3
		button2 = ttk.Button(self, text ="Startpage",
							command = lambda : controller.show_frame(StartPage))
		# putting the button in its place by
		# using grid
		button2.grid(row = 2, column = 1, padx = 10, pady = 10)




# Fourth window frame page3
class Page3NewPW(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = ttk.Label(self, text ="Page 2", font = LARGEFONT)
		label.grid(row = 0, column = 4, padx = 10, pady = 10)

		# button to show frame 2 with text
		# layout2
		button1 = ttk.Button(self, text ="Page 1",
							command = lambda : controller.show_frame(Page1PWM))
	
		# putting the button in its place by
		# using grid
		button1.grid(row = 1, column = 1, padx = 10, pady = 10)

		# button to show frame 3 with text
		# layout3
		button2 = ttk.Button(self, text ="Startpage",
							command = lambda : controller.show_frame(StartPage))
		# putting the button in its place by
		# using grid
		button2.grid(row = 2, column = 1, padx = 10, pady = 10)


# Driver Code
app = tkinterApp()
app.title("PWM")
#app.geometry("300x300")
app.mainloop()
