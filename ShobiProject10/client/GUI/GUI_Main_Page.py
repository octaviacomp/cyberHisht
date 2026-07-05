import tkinter as tk
from tkinter import ttk, messagebox, Tk, Text, Scrollbar, simpledialog
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

from client.GUI import GUI_Add_site, GUI_Site_Details


class SiteManager:
    def __init__(self, parent, client, username):
        self.window = tk.Toplevel(parent)
        self.window.title("Site Manager")
        self.window.geometry("700x550")
        self.style = Style(theme='darkly')
        self.window.configure(bg="#f0f0f0")
        self.username = username

        self.client = client

        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack(expand=True, fill='both')

        self.title_label = ttk.Label(self.main_frame, text=f"Welcome, {self.username}!", background="#222", foreground="white", font=('Helvetica', 24, "bold"))
        self.title_label.pack(pady=20)

        search_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        search_frame.pack(fill=tk.X, padx=10, pady=(0,10))

        tk.Label(search_frame, text="Search:", bg="#f0f0f0", font=("Arial", 11)).pack(side=tk.LEFT, padx=(0,5))
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=25)
        search_entry.pack(side=tk.LEFT, padx=(0, 5))

        search_name_btn = tk.Button(search_frame, text="Search Site Name", command=lambda: self.search_sites(username, "site_name"), bg="#FF9880", fg="white", font=("Arial", 9, "bold"), padx=5, pady=2)
        search_name_btn.pack(side=tk.LEFT, padx=5)

        search_nickname_btn = tk.Button(search_frame, text="Search Nickname", command=lambda: self.search_sites(username, "site_nickname"), bg="#FF9800", fg="white", font=("Arial", 9, "bold"), padx=5, pady=2)
        search_nickname_btn.pack(side=tk.LEFT, padx=5)

        reset_search_btn =tk.Button(search_frame, text="Reset", command=self.load_sites, bg="#9E9E9E", fg="white", font=("Arial", 9, "bold"), padx=5, pady=2)
        reset_search_btn.pack(side=tk.LEFT, padx=5)

        self.sites_frame = tk.LabelFrame(self.main_frame, text="Your Sites", bg="#f0f0f0", font=("Arial", 12))
        self.sites_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.sites_tree = ttk.Treeview(self.sites_frame, columns=("Nickname", "Site", "URL"), show="headings")
        self.sites_tree.heading("Nickname", text="Site Nickname")
        self.sites_tree.heading("Site", text="Site Name")
        self.sites_tree.heading("URL", text="URL")
        self.sites_tree.column("Nickname", width=150)
        self.sites_tree.column("Site", width=150)
        self.sites_tree.column("URL", width=350)
        self.sites_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(self.sites_tree, orient="vertical", command=self.sites_tree.yview)
        self.sites_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.load_sites(username)

        self.sites_tree.bind("<Double-1>", self.on_treeview_double_click)

        button_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=10)

        add_button =tk.Button(button_frame, text="Add New Site", command=self.open_add_site_window, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
        add_button.pack(side=tk.LEFT, padx=5)

        view_button = tk.Button(button_frame, text="View Details", command=lambda: self.view_site_details(username), bg="#2196F3", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
        view_button.pack(side=tk.LEFT, padx=5)

        launch_button = tk.Button(button_frame, text="Launch In Browser", command=self.launch_site_in_browser, bg="#9C27B0", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
        launch_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(button_frame, text="Delete Site", command=lambda: self.delete_site(username), bg="#F44336", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
        delete_button.pack(side=tk.LEFT, padx=5)


    # def setup_database(self):
    #     conn = sqlite3.connect("site_manager.db")
    #     cursor = conn.cursor()
    #     cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS allsites (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         username TEXT,
    #         site_name TEXT,
    #         site_nickname TEXT,
    #         site_url TEXT,
    #         site_password TEXT,
    #         is_hashed INTEGER DEFAULT 0
    #     )
    #     ''')
    #     conn.commit()
    #     conn.close()

    def load_sites(self, username):
        for item in self.sites_tree.get_children():
            self.sites_tree.delete(item)

        sites = self.client.handle_load_sites(username)
        print (" *** GUI *** MAIN_PAGE *** sites = " , sites)
        for site in eval(sites):
            print (" *** GUI *** MAIN_PAGE *** site1 = " , site)
            self.sites_tree.insert("", tk.END, values=site)

    def on_treeview_double_click(self, event):
        item = self.sites_tree.identify('item', event.x, event.y)
        if item:
            self.launch_site_in_browser()

    def search_sites(self, username, search_by):
        search_term = self.search_var.get().strip()
        if not search_term:
            messagebox.showinfo("Search Error", "Please enter a search term.")
            return

        for item in self.sites_tree.get_children():
            self.sites_tree.delete(item)

        # conn = sqlite3.connect("site_manager.db")
        # cursor = conn.cursor()
        # cursor.execute(
        #         f"SELECT site_nickname, site_name, site_url FROM allsites WHERE username = ? AND {search_by} LIKE ?",
        #     (self.username, f"%{search_term}%")
        # )
        # sites =cursor.fetchall()
        # conn.close()

        sites = self.client.handle_search_sites(username, search_by, search_term)

        if sites:
            for site in sites:
                self.sites_tree.insert("", tk.END, values=site)
        else:
            messagebox.showinfo("Search Results", f"No sites found matching '{search_term}'.")
            self.load_sites(self.username)



    def open_add_site_window(self):
        add_window = self.goto_add_Site()

    def view_site_details(self, username):
        selected_item = self.sites_tree.selection()
        if not selected_item:
            messagebox.showinfo("Selection Required", "Please select a site to view details")
            return

        site_nickname = self.sites_tree.item(selected_item[0], "values")[0]

        site_details = self.client.handle_site_details(username, site_nickname)
        # conn = sqlite3.connect("site_manager.db")
        # cursor = conn.cursor()
        # cursor.execute(
        #     "SELECT site_name, site_url, site_password, is_hashed FROM allsites WHERE username = ? AND site_nickname = ?",
        #     (self.username, site_nickname)
        # )
        # site_details = cursor.fetchone()
        # conn.close()

        if site_details:
            root5 = tk.Tk()
            app5 = GUI_Site_Details.SiteDetails(root5, self.client, site_details, site_nickname)
            root5.mainloop()
        else:
            messagebox.showerror("Error", "Could not find side details.")

    def launch_site_in_browser(self):
        selected_item = self.sites_tree.selection()
        if not selected_item:
            messagebox.showinfo("Selection Required", "Please select a site to launch in browser.")
            return

        site_url = self.sites_tree.item(selected_item[0], "values")[2]

        if not (site_url.startswith("http://") or site_url.startswith("https://")):
            site_url = "https://" + site_url
        try:
            webbrowser.open(site_url)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open browser: {str(e)}")


    def delete_site(self, username):
        selected_item = self.sites_tree.selection()
        if not selected_item:
            messagebox.showinfo("Selection Requires", "Please select a site to delete.")
            return

        site_nickname = self.sites_tree.item(selected_item[0], "values")[0]

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{site_nickname}'"):
            # conn = sqlite3.connect("site_manager.db")
            # cursor = conn.cursor()
            # cursor.execute(
            #     "DELETE FROM allsites WHERE username = ? AND site_nickname = ?",
            #     (self.username, site_nickname)
            # )
            # conn.commit()
            # conn.close()

            x = self.client.handle_delete_site(username, site_nickname)

            self.load_sites(self.username)
            messagebox.showinfo("Success", f"Site '{site_nickname}' has been deleted")


    def goto_add_Site(self):
        app4 = GUI_Add_site.AddSiteWindow(self.window, self.client, self.username, callback=self.load_sites)





