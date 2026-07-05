import socket
import threading
import hashlib
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import protocol.protocol as pr
import db.shobiDB as shdb




def hashing_util(password):
    return hashlib.sha256(password.encode()).hexdigest()


def handle_connection(client_socket, addr):
    try:
        with client_socket:
            print(">>>SERVER>>> connected ", addr)
            # socket connection open - permanent
            while True:
                data = client_socket.recv(1024)         #receive data from client
                cmd,msg = pr.parse_message(data)
                print(">>>SERVER>>> recv ", cmd, msg)

                if cmd == pr.LOGINREQ:
                    username, password = msg.split(',')
                    #check in db that user exists or not
                    with db_lock:
                        db_auth = db.login_check_user(username, hashing_util(password))
                    resp = pr.create_message(pr.LOGINRESP, db_auth)
                    client_socket.send(resp)
                elif cmd == pr.SIGNUPREQ:
                    username, password = msg.split(',')
                    print(">>>SERVER>>> recv SIGNUPREQ ", username, password)
                    with db_lock:
                        db_auth = db.add_user(username, hashing_util(password))
                    resp = pr.create_message(pr.SIGNUPRESP, db_auth)
                    client_socket.send(resp)
                elif cmd == pr.LOADSITESREQ:
                    username = msg
                    print(">>>SERVER>>> LOADSITESREQ ", username)
                    with db_lock:
                        allsites = db.load_sites(username)
                    resp = pr.create_message(pr.LOADSITESRESP, allsites)
                    client_socket.send(resp)
                elif cmd == pr.ADDSITEREQ:
                    cleaned = msg.strip("()").replace("'", "")
                    username, site_name, site_nickname, site_url, site_password, is_hashed = cleaned.split(",")
                    print(">>>SERVER>>> recv ADDSITEREQ ", username, site_name, site_nickname, site_url, site_password, is_hashed)
                    with db_lock:
                        addsite = db.add_site(username, site_name, site_nickname, site_url, site_password, is_hashed)
                    resp = pr.create_message(pr.ADDSITERESP, addsite)
                    client_socket.send(resp)
                elif cmd == pr.SEARCHSITESREQ:
                    username, search_by, search_term = msg.split(",")
                    print(">>>SERVER>>> recv SEARCHSITESREQ " , username, search_by, search_term)
                    with db_lock:
                        searchsites = db.search_sites(username, search_by, search_term)
                    resp = pr.create_message(pr.SEARCHSITESRESP, searchsites)
                    client_socket.send(resp)
                elif cmd == pr.SITEDETAILSREQ:
                    username, site_nickname = msg.split(",")
                    print(">>>SERVER>>> recv SITEDETAILSREQ ", username, site_nickname)
                    with db_lock:
                        sitedetails = db.site_details(username, site_nickname)
                    resp = pr.create_message(pr.SITEDETAILSRESP, sitedetails)
                    client_socket.send(resp)
                elif cmd == pr.DELETESITEREQ:
                    username, site_nickname = msg.split(',')
                    print(">>>SERVER>>> recv DELETESITESREQ ", username, site_nickname)
                    with db_lock:
                        deletesite = db.delete_site(username, site_nickname)
                    resp = pr.create_message(pr.DELETESITERESP, deletesite)
                    client_socket.send(resp)



    except Exception as e:
        print(f"Error from client {addr}: {e}")
    finally:
        print(f"Connection with {addr} closed")


if __name__ == '__main__':
    #DB init - call functions from shobiDB database
    #inside we have table users - for keeping the username and password - login/signup
    db = shdb.ShobiDB()
    db.init()

    #avoid write/access to DB by several clients in the same time
    db_lock = threading.Lock()

    #server socket connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((pr.HOST, pr.PORT))
        server_socket.listen()
        print(">>>SERVER>>> waiting for clients...")

        while True:
            #get connection from client
            client_socket, addr = server_socket.accept()
            #open new thread per client
            threading.Thread(target=handle_connection, args=(client_socket, addr)).start()