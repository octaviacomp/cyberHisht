
HOST = "10.0.0.5"  # Standard loopback interface address (localhost)
PORT = 65433  # Port to listen on (non-privileged ports are > 1023)

# Define protocol messages
LOGINREQ = "LOGINREQ"
LOGINRESP = "LOGINRESP"
SIGNUPREQ = "SIGNUPREQ"
SIGNUPRESP = "SIGNUPRESP"
LOADSITESREQ = "LOADSITESREQ"
LOADSITESRESP = "LOADSITESRESP"
ADDSITEREQ = "ADDSITEREQ"
ADDSITERESP = "ADDSITERESP"
SEARCHSITESREQ = "SEARCHSITESREQ"
SEARCHSITESRESP = "SEARCHSITESRESP"
SITEDETAILSREQ = "SITEDETAILSREQ"
SITEDETAILSRESP = "SITEDETAILSRESP"
DELETESITEREQ = "DELETESITEREQ"
DELETESITERESP = "DELETESITERESP"

# Helper function to format messages
def create_message(command, data):
    msg = f"{command}:{data}".encode()
    print("PROTO---create_message", msg)
    return msg

# Helper function to parse messages
def parse_message(message):
    try:
        command, data = message.decode().split(":", 1)
        print("PROTO---parse_message", command, data)
        return command, data
    except ValueError:
        return None, None

