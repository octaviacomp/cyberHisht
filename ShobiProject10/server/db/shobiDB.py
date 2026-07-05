import sqlite3
import os
import hashlib



class ShobiDB:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(self.current_dir, 'shobi.db')

    def init(self):
        # Initialize the database with default admin user"""
        admin_list = [("Admin", hashlib.sha256("Admin".encode()).hexdigest())]

        # Connect to the db and create cursor
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        # Create table people
        cur.execute(''' CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT) ''')
        conn.commit()

        cur.execute('''CREATE TABLE IF NOT EXISTS allsites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            site_name TEXT,
            site_nickname TEXT,
            site_url TEXT,
            site_password TEXT,
            is_hashed INTEGER DEFAULT 0
        )
        ''')
        conn.commit()

        # Add default admin user
        self.add_user(admin_list[0][0], admin_list[0][1])

        # Display data from db
        memdata = cur.execute("SELECT * FROM users")
        for row in memdata:
            print(row)

        # Close cursor and connection to db
        cur.close()
        conn.close()

    def login_check_user(self, username, password):
        # Check if a user exists in the database with the given credentials"""
        print(">>>SHOBI-DB>>>---login_check_user_in_DB", username, password)

        try:
            # Connect to the database
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()

            # Prevent SQL injection
            cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            result = cur.fetchone()

            # Close the database connection
            conn.close()

            print(">>>SHOBI-DB>>>---login_check_user_in_DB result = ", result)
            return result is not None  # True if found

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

        except Exception as e:
            print(f"Unexpected error: {e}")
            return False

    def add_user(self, username, password):
        #Add a new user to the database if they don't already exist"""
        print(">>>SHOBI-DB>>>---add_user_to_DB", username, password)

        # Connect to the database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Check if the user already exists
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            conn.close()
            print(">>>SHOBI-DB>>>---add_user_to_DB -- user already exists")
            return False  # User already exists

        # Insert the new user into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()  # Save changes
        conn.close()  # Close the connection

        print(">>>SHOBI-DB>>>---add_user_to_DB -- user added successfully")
        return True  # User added successfully


    def load_sites(self, username):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT site_nickname, site_name, site_url FROM allsites WHERE username = ?", (username,))
        sites = cursor.fetchall()
        conn.close()
        return sites

    def search_sites(self, username, search_by, search_term):
        conn = sqlite3.connect("shobi.db")
        cursor = conn.cursor()
        #cursor.execute("SELECT site_nickname, site_name, site_url FROM allsites WHERE username = ?", (username,))

        cursor.execute(f"SELECT site_nickname, site_name, site_url FROM allsites WHERE username = ? AND {search_by} LIKE ?",(username, f"%{search_term}%"))
        sites = cursor.fetchall()
        conn.close()
        print(">>>SHOBI-DB>>>---search_sites - ", sites)
        return sites

    def site_details(self, username, site_nickname):
        conn = sqlite3.connect("shobi.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT site_name, site_url, site_password, is_hashed FROM allsites WHERE username = ? AND site_nickname = ?",
            (username, site_nickname)
        )
        site_details = cursor.fetchone()
        conn.close()

    def delete_site(self, username, site_nickname):
        conn = sqlite3.connect("shobi.db")
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM allsites WHERE username = ? AND site_nickname = ?",
            (username, site_nickname)
        )
        conn.commit()
        conn.close()


    def add_site(self, username, site_name, site_nickname, site_url, site_password, is_hashed):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        result = "ADD_OK"

        cursor.execute(
            "SELECT id FROM allsites WHERE username = ? AND site_nickname = ?",
            (username, site_nickname)
        )
        if cursor.fetchone():
            result = "ADD_FAILED_SITE_ALREADY_EXISTS"
            conn.close()
            return result

        cursor.execute(
            "INSERT INTO allsites (username, site_name, site_nickname, site_url, site_password, is_hashed) VALUES (?, ?, ?, ?, ?, ?)",
            (username, site_name, site_nickname, site_url, site_password, is_hashed)
        )

        conn.commit()
        conn.close()
        return result


if __name__ == '__main__':
    db = ShobiDB()
    db.init()
