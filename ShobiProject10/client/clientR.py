import os
import socket
import sys
import threading
import time
import tkinter as tk
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import protocol.protocol as pr
import GUI.GUI_Login as gl



class ClientShobi:

    def __init__(self, host=pr.HOST, port=pr.PORT):
        self.server_address = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((pr.HOST, pr.PORT))
        self.login_status = None
        self.signup_status = None
        # Start background listening thread
        self.start_listener()
        self.load_status = None
        self.loadsites_data = None
        self.add_site_data = None
        self.add_site_status = None
        self.search_status = None
        self.searchsites_data = None
        self.details_status = None
        self.sitedetails_data = None

    def start_listener(self):
        self.listener_thread = threading.Thread(target=self.listen_to_server, daemon=True)
        self.listener_thread.start()

    def listen_to_server(self):
        while True:
            try:
                # Receive response from server
                response = self.socket.recv(1024)
                command, data = pr.parse_message(response)

                #print(">>>CLIENT>>> listen_to_server >> data = ", data)

                if command == pr.LOGINRESP:
                    if data == "True":
                        print(">>>CLIENT>>> Login successful!")
                        self.login_status = "LOGIN_SUCCESS"
                    else:
                        print(">>>CLIENT>>> Authentication failure")
                        self.login_status = "LOGIN_FAIL"
                elif command == pr.SIGNUPRESP:
                    if data == "True":
                        print(">>>CLIENT>>> Signup successful!")
                        self.signup_status = "SIGNUP_SUCCESS"
                    else:
                        print(">>>CLIENT>>> Authentication failure")
                        self.signup_status = "SIGNUP_FAIL"
                elif command == pr.LOADSITESRESP:
                    if data != None:
                        self.loadsites_data = data
                        print(">>>CLIENT>>> Load_Sites successfull")
                        print(">>>CLIENT>>> data =  ", data)
                        self.load_status = "LOADSITES_SUCCESS"
                    else:
                        print(">>>CLIENT>>> Load_Sites failure")
                        self.load_status = "LOADSITES_FAIL"
                elif command == pr.ADDSITERESP:
                    if data != None:
                        self.add_site_data = data
                        print(">>>CLIENT>>> Add_Sites successful")
                        self.add_site_status = "ADDSITE_SUCCESS"
                    else:
                        print(">>>CLIENT>>> Add_Sites failure")
                        self.add_site_status = "ADDSITE_FAIL"
                elif command == pr.SEARCHSITESRESP:
                    if data != None:
                        self.searchsites_data = data
                        print(">>>CLIENT>>> Search_Sites successful")
                        self.search_status = "SEARCHSITES_SUCCESS"
                    else:
                        print(">>>CLIENT>>> Search_Sites failure")
                        self.search_status = "SEARCHSITES_FAIL"
                elif command == pr.SITEDETAILSRESP:
                    if data != None:
                        self.sitedetails_data = data
                        print(">>>CLIENT>>> Details_Sites successful")
                        self.details_status = "SITEDETAILS_SUCCESS"
                    else:
                        print(">>>CLIENT>>> Details_Sites failure")
                        self.details_status = "SITEDETAILS_FAIL"
                elif command == pr.DELETESITERESP:
                    if data != None:
                        self.delete_site_data = data
                        print(">>>CLIENT>>> Delete_Site successful")
                        self.delete_status = "DELETESITE_SUCCESS"
                    else:
                        print(">>>CLIENT>>> Delete_Site failure")
                        self.delete_status = "DELETESITE_FAIL"

            except Exception as e:
                print(f"Listen to server error: {e}")
                break

    def handle_login(self, username, password):
        print (">>>CLIENT>>> handle_login --  username= ", username, "  password= ", password)
        self.login_status = None
        msg = pr.create_message(pr.LOGINREQ, f"{username},{password}")
        self.socket.send(msg)

        # wait till login finish the REQUEST RESPONSE
        timeout = 5  # seconds
        start_time = time.time()
        while self.login_status is None:
            if time.time() - start_time > timeout:
                print(">>>CLIENT>>> handle_login - Timeout")
                return "LOGIN_TIMEOUT"
            time.sleep(0.1)
        if self.login_status != "LOGIN_SUCCESS":
            return "LOGIN_FAIL"

        #TODO --- open the main page

        return "LOGIN_SUCCESS"

    def handle_signup(self, username, password):
        print (">>>CLIENT>>> handle_signup --  username= ", username, "  password= ", password)
        self.signup_status = None
        msg = pr.create_message(pr.SIGNUPREQ, f"{username},{password}")
        self.socket.send(msg)
        # wait till signup finish the REQUEST RESPONSE
        timeout = 5  # seconds
        start_time = time.time()
        while self.signup_status is None:
            if time.time() - start_time > timeout:
                print(">>>CLIENT>>> handle_signup - Timeout")
                return "SIGNUP_TIMEOUT"
            time.sleep(0.1)
        if self.signup_status != "SIGNUP_SUCCESS":
            return "SIGNUP_FAIL"

        else:
            return "SIGNUP_SUCCESS"

    def handle_load_sites(self, username):
        print(">>>CLIENT>>> handle_load_sites --  username= ", username)

        msg = pr.create_message(pr.LOADSITESREQ, f"{username}")
        self.socket.send(msg)

        # wait till login finish the REQUEST RESPONSE
        timeout = 5  # seconds
        start_time = time.time()
        while self.load_status is None:
            if time.time() - start_time > timeout:
                print(">>>CLIENT>>> handle_load_sites - Timeout")
                return "LOADSITES_TIMEOUT"
            time.sleep(0.1)
        if self.load_status == "LOADSITES_SUCCESS":
            print (">>>CLIENT>>> LOADSITES_SUCCESS - load_status = ", self.loadsites_data)
            return self.loadsites_data

        # if self.load_status == "LOADSITES_SUCCESS":
        #     print(">>>CLIENT>>> handle_load_sites", self.loadsites_data)
        #     return self.loadsites_data
        # else:
        #     return "LOADSITES_FAIL"

    def handle_search_sites(self, username, search_by, search_term):
        print(">>>CLIENT>>> handle_search_sites -- username= ", username, " ", "search_by ", search_by, "", "search_term ", search_term)

        msg = pr.create_message(pr.SEARCHSITESREQ, f"{username, search_by, search_term}")
        self.socket.send(msg)

        # wait till SEARCH SITE finish the REQUEST RESPONSE
        timeout = 5  # seconds
        start_time = time.time()
        while self.search_status is None:
            if time.time() - start_time > timeout:
                print(">>>CLIENT>>> handle_add_site - Timeout")
                return "SEARCH_SITE_TIMEOUT"
            time.sleep(0.1)
        if self.search_status != "SEARCHSITE_SUCCESS":
            return "SEARCH_SITE_FAIL"
        if self.search_status == "SEARCHSITES_SUCCESS":
            print(">>>CLIENT>>> handle_search_sites", self.searchsites_data)
            return self.searchsites_data
        else:
            return "SEARCHSITES_FAIL"

    def handle_site_details(self, username, site_nickname):
        print(">>>CLIENT>>> handle_site_details -- username= ", username, " ", "site_nickname ", site_nickname)

        msg = pr.create_message(pr.SITEDETAILSREQ, f"{username, site_nickname}")
        self.socket.send(msg)
        if self.details_status == "SITEDETAILS_SUCCESS":
            print(">>>CLIENT>>> handle_site_details ", self.sitedetails_data)
            return self.sitedetails_data
        else:
            return "SITEDETAILS_FAIL"

    def handle_add_site(self, username, site_name, site_nickname, site_url, site_password, is_hashed):
        print(">>>CLIENT>>> handle_add_site --  username= ", username, "site_name= ", site_name)
        self.load_status = None
        msg = pr.create_message(pr.ADDSITEREQ, f"{username, site_name, site_nickname, site_url, site_password, is_hashed}")
        self.socket.send(msg)

        print(">>>CLIENT>>> handle_add_site -- after send - add_site_status", self.add_site_status)
        print(">>>CLIENT>>> handle_add_site -- after send - add_site_status", self.add_site_status)

        # wait till ADD SITE finish the REQUEST RESPONSE
        timeout = 5  # seconds
        start_time = time.time()
        while self.add_site_status is None:
            if time.time() - start_time > timeout:
                print(">>>CLIENT>>> handle_add_site - Timeout")
                return "ADD_SITE_TIMEOUT"
            time.sleep(0.1)
        if self.add_site_status != "ADDSITE_SUCCESS":
            return "ADD_SITE_FAIL"
        if self.add_site_status == "ADDSITE_SUCCESS":
            print(">>>CLIENT>>> handle_add_site", self.add_site_data)
            return self.add_site_data
        else:
            return "ADDSITE_FAIL"

    def handle_delete_site(self, username, site_nickname):
        print(">>>CLIENT>>> handle_delete_site -- username= ", username, " ", "site_nickname ", site_nickname)

        msg = pr.create_message(pr.DELETESITEREQ, f"{username, site_nickname}")
        self.socket.send(msg)
        if self.details_status == "DELETESITE_SUCCESS":
            print(">>>CLIENT>>> handle_delete_site")
            return self.delete_site_data
        else:
            return "DELETESITE_FAIL"



def main():
    root = tk.Tk()
    client = ClientShobi()  # makes object of clientShobi
    app = gl.LoginApp(root, client)

    root.mainloop()

if __name__ == '__main__':
    main()