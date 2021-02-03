from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]

    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]

    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers

    random.shuffle(password_list)

    new_password = "".join(password_list)

    pass_entry.delete(0, END)
    pass_entry.insert(0, new_password)
    pyperclip.copy(new_password)

# ---------------------------- SAVE PASSWORD ------------------------------- #

def add_password():
    website = web_entry.get()
    email = user_entry.get()
    password = pass_entry.get()
    storable = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if website == "" or email == "" or password == "":
        messagebox.showinfo(title="Oops", message="Please fill out all fields!")
    else:
        # is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email}\n"
        #                                               f"Password: {password}\nIs it ok to save?")
        # if is_ok:
        try:
            with open("data.json", mode="r") as data_file:
                data = json.load(data_file)
                data.update(storable)

            with open("data.json", mode="w") as data_file:
                json.dump(data, data_file, indent=4)

        except FileNotFoundError:
            with open("data.json", mode="w") as data_file:
                json.dump(storable, data_file, indent=4)

        web_entry.delete(0, END)
        user_entry.delete(0, END)
        pass_entry.delete(0, END)

# -------------------------- SEARCH PASSWORD -------------------------- #

def search_password():
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="No passwords have been saved.")
    else:
        website = web_entry.get()
        try:
            username = data[website]["email"]
            password = data[website]["password"]
        except KeyError:
            messagebox.showinfo(title=website, message="Website not in database.")
        else:
            messagebox.showinfo(title=website, message=f"Username: {username}\n"
                                                       f"Password: {password}")

# ---------------------------- UI SETUP ------------------------------- #

# Set up window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Set up lock pic
lock = Canvas(width=200, height=200)
lock_png = PhotoImage(file="logo.png")
lock.create_image(100, 100, image=lock_png)
lock.grid(column=1, row=0)

# Website Label
web_label = Label(text="Website:")
web_label.grid(column=0, row=1)

# Website Entry
web_entry = Entry(width=33)
web_entry.grid(column=1, row=1)
web_entry.focus()

# Search Password Button
search_button = Button(text="Search", command=search_password, width=15)
search_button.grid(column=2, row=1)

# Username Label
user_label = Label(text="Email/Username:")
user_label.grid(column=0, row=2)

# Username Entry
user_entry = Entry(width=51)
user_entry.grid(column=1, row=2, columnspan=2)
user_entry.insert(0, "hintzejordan@gmail.com")

# Password Label
pass_label = Label(text="Password:")
pass_label.grid(column=0, row=3)

# Password Entry
pass_entry = Entry(width=33)
pass_entry.grid(column=1, row=3)

# Generate Password Button
pass_button = Button(text="Generate Password", command=generate_password)
pass_button.grid(column=2, row=3)

# Add Button
add_button = Button(text="Add", width=45, command=add_password)
add_button.grid(column=1, row=4, columnspan=2)


window.mainloop()