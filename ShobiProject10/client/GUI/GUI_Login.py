import ttkbootstrap
import tkinter as tk
from ttkbootstrap import Style
import ttkbootstrap as ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from client.GUI import GUI_SignUp, GUI_Main_Page

tk
class LoginApp:
    def __init__(self, root, client):
        self.root = root
        self.style = Style(theme='darkly')
        self.root.title("SHOBI Login Application")
        self.root.geometry("850x350")

        self.client = client

        # self.main_frame = ttk.Frame(self.root, padding=20)
        # self.main_frame.pack(expand=True, fill='both')

        # Create main container frame
        self.container_frame = ttk.Frame(self.root)
        self.container_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Create left frame for image
        self.image_frame = ttk.Frame(self.container_frame)
        self.image_frame.pack(side='left', fill='both', padx=(20, 0) )

        # Create right frame for login form
        self.main_frame = ttk.Frame(self.container_frame, padding=20)
        self.main_frame.pack(side='right', expand=True, fill='both')


        self.title_label = ttk.Label( self.main_frame, text="Login", font=('Helvetica', 24))
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

        # self.login_button = ttk.Button( self.main_frame, text="Login", command=self.verify_login(), bootstyle='success', width=20)
        # self.login_button.pack(pady=20)
        self.login_button = ttk.Button(self.main_frame, text="Login", command=self.verify_login, bootstyle="OUTLINE-SUCCESS")
        self.login_button.pack()

        # Load and display image
        self.load_image()

        self.sign_up = ttk.Button(self.main_frame, text="SignUp", command=self.goto_signup, bootstyle="OUTLINE-LIGHT")
        self.sign_up.pack()

        self.root.bind('<Return>', lambda event: self.verify_login())

        self.username_entry.focus()

    def verify_login(self):

        username = self.username_entry.get()
        password = self.password_entry.get()
        print (">>>GUI login>>> username = ", username, "  password= ", password )

        response = self.client.handle_login(username, password)
        print(">>>GUI login>>> response = ", response)
        if response == "LOGIN_SUCCESS":
            messagebox.showinfo("Success", "Login successful!", icon='info')
            self.clear_fields()
            self.goto_thingy(username)



        else:
            messagebox.showerror("Error", "Invalid username or password")
            self.password_entry.delete(0, tk.END)
        #
        # if  username == "admin" and password == "123456":
        #     messagebox.showinfo("Success", "Login successful!", icon='info')
        #     self.clear_fields()
        # else:
        #     messagebox.showerror("Error", "Invalid username or password")
        #     self.password_entry.delete(0, tk.END)

    def goto_signup(self):
        #root2 = tk.Tk()
        app2 = GUI_SignUp.SignUpWindow(self.root, self.client)
        #root2.mainloop()

    def goto_thingy(self, username):
        #root3 = tk.Tk()
        app3 = GUI_Main_Page.SiteManager(self.root, self.client, username)
        #root3.mainloop()

    def clear_fields(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.username_entry.focus()


    def load_image(self):
        """Load and display the shobi.png image"""
        try:
            # Try to load the image
            if os.path.exists("shobi.gif"):
                # Load the image
                image = Image.open("shobi.gif")

                # Resize image to fit nicely (adjust size as needed)
                image = image.resize((300, 300), Image.Resampling.LANCZOS)

                # Convert to PhotoImage
                self.photo = ImageTk.PhotoImage(image)

                # Create label to display image
                self.image_label = ttk.Label(self.image_frame, image=self.photo)
                self.image_label.pack(expand=True)

            else:
                # If image file doesn't exist, show placeholder text
                placeholder_label = ttk.Label(
                    self.image_frame,
                    text="shobi.gif\nnot found",
                    font=('Helvetica', 12),
                    foreground='gray'
                )
                placeholder_label.pack(expand=True)

        except Exception as e:
            # If there's an error loading the image, show error message
            error_label = ttk.Label(
                self.image_frame,
                text=f"Error loading\nshobi.gif:\n{str(e)}",
                font=('Helvetica', 10),
                foreground='red'
            )
            error_label.pack(expand=True)
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = LoginApp(root)
#     root.mainloop()