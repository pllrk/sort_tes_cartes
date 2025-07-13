#import the tkinter module
from tkinter import *
import requests
import json
from tkinter import filedialog
import os
from PIL import Image, ImageTk

#create window
window = Tk()
#size of window
window.geometry()
window.config(bg= '#2f2f2f')

##### json managment #####
with open('./tri_raw_data_base/path.json', 'r') as openfile:
	json_object = json.load(openfile)
card_list = json_object['test_data'] #for test
#card_list = json_object['big_data'] #for real

####


frame = Frame(window)
frame.pack()

label = Label(window, 
			  		text="Sort tes cartes", 
			  		font=('Arial', 40, 'bold'), 
			  		fg="#F5F23C",
			  		bg= '#7954AB',
			  		relief=RAISED,
			  		bd = 10,
			  		padx = 200,
			  		pady = 10)
label.pack()
#label.place(x = 0, y = 0)


##### entry box text #####


#auto_complete

card_name = ""
check_for_button = 0
frame_auto_button = Frame(window)
frame_auto_button.pack()
list_of_button = []
list_of_sets_name_global = []

def clear_buttons():
    global list_of_button
    for button in list_of_button:
        button.destroy()
    list_of_button.clear()

def creation_auto_button(list_of_results):
	global list_of_button
	clear_buttons()
	index_list_of_button = IntVar()
	for j in range(len(list_of_results)):
		radiobutton = Radiobutton(frame_auto_button, 
								font=('Arial', 20), 
								text=list_of_results[j],
								value=j, 
								variable= index_list_of_button,
								relief=RAISED,
								bd = 5,
								padx = 5,
								pady = 5,
								fg='#49119B',
								bg= '#7954AB',
								activeforeground='#5E3B91',
								activebackground='#9B7DA6',
								indicatoron= 0)
		radiobutton.pack(anchor="w")
		list_of_button.append(radiobutton)

def clear_buttons_set_name():
    global list_of_sets_name_global
    for button in list_of_sets_name_global:
        button.destroy()
    list_of_sets_name_global.clear()

def creation_auto_set_name(list_of_set_names):
	global list_of_sets_name_global
	clear_buttons_set_name()
	index_list_of_button_set_name = IntVar()
	for j in range(len(list_of_set_names)):
		png_path = os.path.join("edhrec_set_png", f"{list_of_set_names[j]}.png")
		try:
			image = Image.open(png_path)
			image_set = ImageTk.PhotoImage(image)
		except Exception as e:
			raise Exception(f"Failed to load image: {e}")
		print(png_path)
		image_set_button = Radiobutton(frame_auto_button, 
								font=('Arial', 20), 
								text=list_of_set_names[j],
								value=j, 
								variable= index_list_of_button_set_name,
								relief=RAISED,
								bd = 5,
								padx = 5,
								pady = 5,
								fg='#49119B',
								bg= '#7954AB',
								activeforeground='#5E3B91',
								activebackground='#9B7DA6',
								image = image_set,
								indicatoron= 0)
		image_set_button.pack(anchor="w")
		list_of_sets_name_global.append(image_set_button)

def on_key_release(event):
	if event.keysym in ('Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R', 'Left', 'Right', 'Up', 'Down'):
		return
	list_of_results = []
	list_of_set_names = []
	card_name = entry.get().strip().lower()
	auto_complete_name = ""
	set_name = ""
	i = 0
	if card_name:
		for card in card_list:
			i = i + 1
			if ('printed_name' not in card):
				continue
			if len(card_name) >= 4:
				auto_complete_name = card['printed_name'].lower()
				set_name = card['set_name']
				print(set_name)
				if (auto_complete_name.startswith(card_name) == TRUE):
					if auto_complete_name not in list_of_results and len(list_of_results) <= 5:
						list_of_results.append(auto_complete_name)
					if set_name not in list_of_set_names and len(list_of_set_names) <= 5:
						set_name = set_name.replace(" ", "_")
						list_of_set_names.append(set_name)
		creation_auto_button(list_of_results)
		creation_auto_set_name(list_of_set_names)
	for x in list_of_results:
		print(x)
	
#entry box
entry = Entry(window,
			  font=('Arial', 28),
			  width="50")
entry.insert(0, 'card name')
entry.bind("<KeyRelease>", on_key_release)
entry.focus_set()
entry.pack(side = LEFT)
	



#submit command

def submit():
	card_name = entry.get()
	recherche = "https://api.scryfall.com/cards/autocomplete?q=" + card_name
	res=requests.get(recherche)
	respons=json.loads(res.text)
	print (respons)
	print(card_name)

#button

submit_button = Button(window,
							text="submit",
							command = submit,
							font=('Arial', 20),
							fg='#49119B',
							bg= '#7954AB',
							activeforeground='#5E3B91',
							activebackground='#9B7DA6',
							relief=RAISED,
							bd = 5,
							padx = 5,
							pady = 5)
submit_button.pack(side= LEFT)

#auto_complete_button = Button(window,
#							text="auto_complete",
#							command = auto_complete,
#							font=('Arial', 20),
#							fg='#49119B',
#							bg= '#7954AB',
#							activeforeground='#5E3B91',
#							activebackground='#9B7DA6',
#							relief=RAISED,
#							bd = 5,
#							padx = 5,
#							pady = 5)
#auto_complete_button.pack(side= LEFT)


# A relier avec le save de doc en dessous (le button submit)

##### save a file #####

def savefile():
	file = filedialog.asksaveasfile(
					initialdir="/root/code/projet/sort_card_helper/collection",
					defaultextension = '.json')
	if file is None:
		return
	filetext = str(save_text.get(1.0, END))
	file.write(filetext)
	file.close() 

save_button = Button(text= 'save .json', command = savefile)
save_button.pack()

#save_text = Text(window) #a box for typing text
#save_text.pack()


##### check box #####

foil = IntVar()

def display():
	if (foil.get() == 1):
		print("Foil yes")
	else:
		print("Foil no")

check_box = Checkbutton(window,
							font=('Arial', 20), 
							text='foil',
							fg='black',
			  				bg= '#7954AB',
							activeforeground='black',
							activebackground='#7954AB',
							variable= foil,
							onvalue= 1,
							offvalue= 0,
							command= display)
check_box.pack()


##### check box #####

colors = ["colorless", "multicolor", "green", "red", "black", "blue", "white"]

couleur = IntVar()

for index in range(len(colors)):
	radiobutton = Radiobutton(window, 
						   font=('Arial', 20), 
						   text=colors[index], 
						   value=index,
						   variable= couleur,
						   relief=RAISED,
						   bd = 5,
						   padx = 5,
						   pady = 5,
						   fg='#49119B',
						   bg= '#7954AB',
						   activeforeground='#5E3B91',
						   activebackground='#9B7DA6',
						   indicatoron= 0,
						   width= 10)
	radiobutton.pack()


langue = ["Français", "Anglais"]

langua = IntVar()

for index in range(len(langue)):
	radiobutton = Radiobutton(window, 
						   font=('Arial', 20), 
						   text=langue[index], 
						   variable= langua,
						   relief=RAISED,
						   bd = 5,
						   padx = 5,
						   pady = 5,
						   fg='#49119B',
						   bg= '#7954AB',
						   activeforeground='#5E3B91',
						   activebackground='#9B7DA6',
						   indicatoron= 0,
						   width= 10,
						   value=index)
	radiobutton.pack(side=BOTTOM)


##############################

#hidden = IntVar()
#
#def display():
#	if (hidden.get() == 1):
#		
#	else:
#		print("Foil no")

button_1 = Button(window,
						font=('Arial', 20), 
						text='Caché',
						fg='black',
			  			bg= '#7954AB',
						activeforeground='black',
						activebackground='#7954AB')
						#variable= hidden,
						#onvalue= 1,
						#offvalue= 0,
						#command= display)
button_1.pack()

button_2 = Button(window,
						font=('Arial', 20), 
						text='Pas caché',
						fg='black',
						bg= '#7954AB',
						activeforeground='black',
						activebackground='#7954AB')
						#variable= hidden,
						#onvalue= 0,
						#offvalue= 1,
						#command= display)
button_2.pack()


####


#to loop
window.mainloop()

##### what to do #####
# 1) create a box to type things
# 2) create a button that we can click or press enter to validate the data
# 3) create option such as colors / fr or en / foil or not / quantity / edition
# 4) when the button is pressed, send all the data in a database
# 5) when the data-base is done, click a button to export to csv

# 6) ??? do the scrapping in the prorgam itself?

#-------------bonus-------------#
# 	auto-completion with data base of cards linked to the program
#	auto-completion of colors with the same data-base linked with the name of the card
#	reduce the number of edition to chose from based on where the card has been reprinted
# 	possibilty to go in the data base and change the data live



