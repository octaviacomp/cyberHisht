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
import webbrowser



class SiteDetails:
    def __init__(self, parent, client, site_details, site_nickname):
        self.window = tk.Toplevel(parent)
        self.client = client
        self.site_details = site_details
        self.site_nickname = site_nickname

        details_window = tk.Toplevel(self.window)
        details_window.title(f"Details for {site_nickname}")
        details_window.geometry("500x350")
        details_window.configure(bg="#f0f0f0")

        details_frame = tk.Frame(details_window, bg="#f0f0f0")
        details_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(details_frame, text=f"Site: {site_details[0]}", font=("Arial", 12), bg="#f0f0f0").pack(anchor=tk.W,
                                                                                                        pady=5)
        tk.Label(details_frame, text=f"Nickname: {site_nickname}", font=("Arial", 12), bg="#f0f0f0").pack(anchor=tk.W,
                                                                                                          pady=5)

        url_frame = tk.Frame(details_frame, bg="#f0f0f0")
        url_frame.pack(fill=tk.X, pady=5, anchor=tk.W)

        tk.Label(url_frame, text=f"URL: ", font=("Arial", 12), bg="#f0f0f0").pack(side=tk.LEFT)
        url_entry = tk.Entry(url_frame, width=40, readonlybackground="#222")
        url_entry.insert(0, site_details[1])
        url_entry.config(state="readonly")
        url_entry.pack(side=tk.LEFT, padx=(0, 5))

        launch_btn = tk.Button(url_frame, text="Launch", command=lambda: webbrowser.open(site_details[1]),
                               fg="white", font=("Arial", 8, "bold"), padx=5, pady=2)
        launch_btn.pack(side=tk.LEFT)

        pw_frame = tk.Frame(details_frame, bg="#f0f0f0")
        pw_frame.pack(fill=tk.X, pady=5)

        is_hashed = site_details[3] == 1
        password_display = "********" if is_hashed else site_details[2]

        tk.Label(pw_frame, text="Password", font=("Arial", 12), bg="#f0f0f0").pack(side=tk.LEFT)
        pw_var = tk.StringVar(value=password_display)
        pw_entry = tk.Entry(pw_frame, textvariable=pw_var, show="•" if not is_hashed else None, state="readonly",
                            width=30, readonlybackground="#222")
        pw_entry.pack(side=tk.LEFT)

        if not is_hashed:
            pw_shown = tk.BooleanVar(value=False)

            def toggle_password():
                if pw_shown.get():
                    pw_entry.config(show="•")
                    pw_shown.set(False)
                    show_btn.config(text="Show")
                else:
                    pw_entry.config(show="")
                    pw_shown.set(True)
                    show_btn.config(text="Hide")

            show_btn = tk.Button(pw_frame, text="Show", command=toggle_password)
            show_btn.pack(side=tk.LEFT, padx=5)

            copy_btn = tk.Button(pw_frame, text="Copy", command=lambda: self.copy_to_clipboard(site_details[2]),
                                 bg="#607D8B", fg="white", font=("Arial", 8, "bold"), padx=5, pady=2)
            copy_btn.pack(side=tk.LEFT, padx=5)
        else:
            tk.Label(pw_frame, text="(Password is encrypted)", fg="#666", bg="#f0f0f0", font=("Arial", 9)).pack(
                side=tk.LEFT, padx=5)

        security_frame = tk.Frame(details_frame, bg="#f0f0f0")
        security_frame.pack(fill=tk.X, pady=10)

        security_status = "Encrypted" if is_hashed else "Plain Text"
        security_color = "#4CAF50" if is_hashed else "#F44336"

        tk.Label(security_frame, text=f"Password Storage: ", font=("Arial", 11), bg="#f0f0f0").pack(side=tk.LEFT)
        tk.Label(security_frame, text=security_status, font=("Arial", 11, "bold"), fg=security_color, bg="#f0f0f0").pack(side=tk.LEFT)

        if not is_hashed:
            auto_login_note = tk.Label(details_frame, text="Tip: Click 'Launch' to open the site in your browser, then copy your password to log in.", font=("Arial", 9, "italic"), fg="#666666", bg="#f0f0f0")
            auto_login_note.pack(anchor=tk.W, pady=(20, 0))

        buttons_frame = tk.Frame(details_window, bg="#f0f0f0")
        buttons_frame.pack(fill=tk.X, pady=10, padx=20)

        tk.Button(buttons_frame, text="Close", command=details_window.destroy, bg="#2196F3", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5).pack(side=tk.RIGHT)

    def copy_to_clipboard(self, text):
        self.window.clipboard_clear()
        self.window.clipboard_append(text)
        self.window.update()

        messagebox.showinfo("Copied", "Password copied to clipboard")