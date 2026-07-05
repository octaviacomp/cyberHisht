import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from ttkbootstrap import Style
from PIL import Image, ImageTk
import os
import getpass
import hashlib
import secrets
import string
import re
from functools import partial
import webbrowser  # For opening URLs in the default browser



class AddSiteWindow:
    def __init__(self, parent, client, username, callback):
        self.window = tk.Toplevel(parent)
        self.client = client
        self.username = username
        self.callback = callback

        self.window.title("Add Site Window")
        self.window.geometry("550x650")
        self.window.configure(bg="#f0f0f0")

        self.style = Style(theme='darkly')

        main_frame = tk.Frame(self.window, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        header_label = tk.Label(main_frame, text="Add New Site", font=("Arial", 16, "bold"), bg="#f0f0f0")
        header_label.pack(pady=(0, 20))

        form_frame = tk.Frame(main_frame, bg="#f0f0f0")
        form_frame.pack(fill=tk.BOTH, padx=10, pady=10)

        tk.Label(form_frame, text="Site Name:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, sticky=tk.W, pady=10)

        self.site_name_var = tk.StringVar()
        self.site_name_entry = tk.Entry(form_frame, textvariable=self.site_name_var, width=30)
        self.site_name_entry.grid(row=0, column=1, sticky=tk.W, pady=10)

        tk.Label(form_frame, text="Site Nickname: ", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, sticky=tk.W, pady=10)

        self.site_nickname_var = tk.StringVar()
        self.site_nickname_entry = tk.Entry(form_frame, textvariable=self.site_nickname_var, width=30)
        self.site_nickname_entry.grid(row=1, column=1, sticky=tk.W, pady=10)

        tk.Label(form_frame,text="Site URL:" ,font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=0, sticky=tk.W, pady=10)

        url_entry_frame = tk.Frame(form_frame, bg="#f0f0f0")
        url_entry_frame.grid(row=2, column=1, sticky=tk.W, pady=10)

        self.site_url_var = tk.StringVar()
        self.site_url_entry = tk.Entry(url_entry_frame, textvariable=self.site_url_var, width=30)
        self.site_url_entry.pack(side=tk.LEFT)

        test_url_btn = tk.Button(url_entry_frame, text="Test", command=self.test_url, fg="white", font=("Arial", 8, "bold"), padx=5, pady=2)
        test_url_btn.pack(side=tk.LEFT, padx=5)

        tk.Label(form_frame, text="Site Password:", font=("Arial", 12), bg="#f0f0f0").grid(row=3, column=0, sticky=tk.W, pady=10)

        pw_entry_frame = tk.Frame(form_frame, bg="#f0f0f0")
        pw_entry_frame.grid(row=3, column=1, sticky=tk.W, pady=10)

        self.site_password_var = tk.StringVar()
        self.site_password_entry = tk.Entry(pw_entry_frame, textvariable=self.site_password_var, width=30, show="•")
        self.site_password_entry.pack(side=tk.LEFT)

        generate_btn = tk.Button(pw_entry_frame, text="Generate", command=self.generate_password, fg="white", font=("Arial", 8, "bold"), padx=5, pady=2)
        generate_btn.pack(side=tk.LEFT, padx=5)

        self.show_password_var = tk.BooleanVar()
        show_password_cb = tk.Checkbutton(form_frame, text="Show password", variable=self.show_password_var, command=self.toggle_password_visibility, bg="#f0f0f0")
        show_password_cb.grid(row=4, column=1, sticky=tk.W, pady=5)

        self.hash_password_var = tk.BooleanVar(value=True)
        hash_password_cb = tk.Checkbutton(form_frame, text="Encrypt password (recommended)", variable=self.hash_password_var, bg="#f0f0f0")
        hash_password_cb.grid(row=5, column=1, sticky=tk.W, pady=5)

        security_info = tk.Label(form_frame, text="Encryption uses SHA-256 hashing for better security.", font=("Arail", 9), fg="#666666", bg="#f0f0f0")
        security_info.grid(row=6, column=1, sticky=tk.W, pady=(0,10))

        quick_select_frame = tk.LabelFrame(main_frame, text="Quick Add", bg="#f0f0f0", font=("Arial", 12))
        quick_select_frame.pack(fill=tk.X, padx=10, pady=20)

        social_buttons_frame = tk.Frame(quick_select_frame, bg="#f0f0f0")
        social_buttons_frame.pack(pady=10)

        self.create_social_button(social_buttons_frame, "Instagram", "https://www.instagram.com/", 0)
        self.create_social_button(social_buttons_frame, "Facebook", "https://www.facebook.com/", 1)
        self.create_social_button(social_buttons_frame, "Google", "https://www.accounts.google.com/", 2)

        buttons_frame = tk.Frame(main_frame, bg="#f0f0f0")
        buttons_frame.pack(fill=tk.X, pady=20)

        save_button = tk.Button(buttons_frame, text="Save", command=self.save_site, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=20, pady=5)
        save_button.pack(side=tk.LEFT, padx=5)

        cancel_button = tk.Button(buttons_frame, text="Cancel", command=self.window.destroy, bg="#F44336", fg="white", font=("Arial", 10, "bold"), padx=20,pady=5)
        cancel_button.pack(side=tk.LEFT, padx=5)

    def create_social_button(self, parent, name, url, col):
        btn_frame = tk.Frame(parent, bg="#f0f0f0", width=100, height=100)
        btn_frame.grid(row=0, column=col, padx=15)
        btn_frame.pack_propagate(False)


        button = tk.Button(btn_frame, text=name, fg="white", font=("Arial", 10, "bold"), command=lambda n=name, u=url: self.select_social_site(n, u))
        button.pack(fill=tk.BOTH, expand=True)

    def select_social_site(self, name, url):
        self.site_name_var.set(name)
        self.site_nickname_var.set(name.lower())
        self.site_url_var.set(url)
        messagebox.showinfo("Quick Add", f"{name} selected. please enter your password or generate one.")
        self.site_password_entry.focus()

    def test_url(self):
        url = self.site_url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a URL to test")
            return

        if not(url.startswith("http://") or url.startswith("https://")):
            url = "https://" + url
            self.site_url_var.set(url)

        try:
            webbrowser.open(url)
            messagebox.showinfo("URL Test", f"Opened {url} in your default browser.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open URL: {str(e)}")


    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.site_password_entry.config(show="")
        else:
            self.site_password_entry.config(show="•")

    def generate_password(self):
        selected_length = simpledialog.askinteger("Password Length", "Select password length", initialvalue=16, minvalue=8, maxvalue=32, parent=self.window)
        if not selected_length:
            return

        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(characters) for _ in range(selected_length))

        while not (any(c.isupper() for c in password) and
                   any(c.islower() for c in password) and
                   any(c.isdigit() for c in password) and
                   any(c in string.punctuation for c in password)):
            password = ''.join(secrets.choice(characters) for _ in range(selected_length))

        self.site_password_var.set(password)

        if not self.show_password_var.get():
            self.show_password_var.set(True)
            self.site_password_entry.config(show="")

        messagebox.showinfo("Password Generated", f"A strong {selected_length}-character password has benn generated.\n\n"
                            "The password is now visible. Make sure to copy it before hiding.")


    def save_site(self):
        site_name = self.site_name_var.get().strip()
        site_nickname = self.site_nickname_var.get().strip()
        site_url = self.site_url_var.get().strip()
        site_password = self.site_password_var.get().strip()
        hash_password = self.hash_password_var.get()

        if not site_name or not site_nickname or not site_url or not site_password:
            messagebox.showerror("Error", "All fields are required.")
            return

        if not (site_url.startswith("http://") or site_url.startswith("https://")):
            site_url = "https://" + site_url
            self.site_url_var.set(site_url)

        stored_password = site_password
        is_hashed = 0
        if hash_password:
            stored_password = hashlib.sha256(site_password.encode()).hexdigest()
            is_hashed = 1

#        try:
            # conn = sqlite3.connect("site_manager.db")
            # cursor = conn.cursor()
            #
            # cursor.execute(
            #     "SELECT id FROM allsites WHERE username = ? AND site_nickname = ?",
            #     (self.username, site_nickname)
            # )
            # if cursor.fetchone():
            #     messagebox.showerror("Error", "Site nickname already exists. Please use a different one.")
            #     conn.close()
            #     return
            #
            # cursor.execute(
            #     "INSERT INTO allsites (username, site_name, site_nickname, site_url, site_password, is_hashed) VALUES (?, ?, ?, ?, ?, ?)",
            #     (self.username, site_name, site_nickname, site_url, stored_password, is_hashed)
            # )
            #
            # conn.commit()
            # conn.close()
        sites = self.client.handle_add_site(self.username, site_name, site_nickname, site_url, site_password, is_hashed)
        print ("*** GUI *** ADD_PAGE *** sites =", sites)
        #refresh parent window after add
        self.callback(self.username)

        security_msg = "The password has been securely stored with encryption." if hash_password else "The password has been stored in plain text. Consider using encryption for better security."
        messagebox.showinfo("Success", f"Site '{site_nickname}' has been added successfully.\n\n{security_msg}")

        self.window.destroy()

        # except Exception as e:
        #     messagebox.showerror("Error", f"An error occured: {str(e)}")









