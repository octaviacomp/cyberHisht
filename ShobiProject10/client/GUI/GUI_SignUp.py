import ttkbootstrap
import tkinter as tk
from ttkbootstrap import Style
import ttkbootstrap as ttk
from tkinter import messagebox


class SignUpWindow:
    def __init__(self, parent, client):
        self.window = tk.Toplevel(parent)
        # self.style = Style(theme="cyborg")
        #self.style = Style(theme='darkly')

        self.window.title("SHOBI SignUp Window")
        self.window.geometry("450x350")

        self.client = client

        self.main_frame = ttk.Frame(self.window, padding=20)
        self.main_frame.pack(expand=True, fill='both')

        self.title_label = ttk.Label( self.main_frame, text="SignUp", font=('Helvetica', 24))
        self.title_label.pack(pady=20)

        self.username_frame = ttk.Frame(self.main_frame)
        self.username_frame.pack(fill='x', pady=5)

        # self.username_label = ttk.Label( self.username_frame, text="Username:", font=('Helvetica', 11))
        # self.username_label.pack(anchor='w')
        self.username_label = tk.Label(self.main_frame, text="Username:")
        self.username_label.pack()

        # self.username_entry = ttk.Entry( self.username_frame, font=('Helvetica', 11))
        # self.username_entry.pack(fill='x', pady=(5, 0))
        self.username_entry = tk.Entry(self.main_frame)
        self.username_entry.pack(pady=(0, 10))

        self.password_frame = ttk.Frame(self.main_frame)
        self.password_frame.pack(fill='x', pady=5)

        # self.password_label = ttk.Label( self.password_frame, text="Password:", font=('Helvetica', 11))
        # self.password_label.pack(anchor='w')
        self.password_label = tk.Label(self.main_frame, text="Password:")
        self.password_label.pack()

        # self.password_entry = ttk.Entry(self.password_frame, show='*', font=('Helvetica', 11))
        # self.password_entry.pack(fill='x', pady=(5, 0))
        self.password_entry = tk.Entry(self.main_frame, show="*")
        self.password_entry.pack(pady=(0, 20))

        self.sign_up = tk.Button(self.main_frame, text="SignUp", command=self.verify_signup)
        self.sign_up.pack()

    def verify_signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        print (">>>GUI signup>>> username = ", username, "  password= ", password )

        response = self.client.handle_signup(username, password)
        print(">>>GUI signup>>> response = ", response)

        if response == "SIGNUP_SUCCESS":
            messagebox.showinfo("Success", "SIGNUP successful!", icon='info')

        else:
            messagebox.showerror("Error", "Invalid username or password")
            self.password_entry.delete(0, tk.END)



