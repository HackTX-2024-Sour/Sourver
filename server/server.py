import socket
import database

def receive_message(client):
    data = b""
    buffer = 1024

    while True:
        packet = client.recv(buffer)
        if not packet:
            break
        data += packet
        
    return data.decode()

def process_get(cmd):
    base64_str = cmd[1]
    responses = 1

    if len(cmd) >= 3:
        responses = int(cmd[2])

    results = database.search_face(base64_str, responses)

    if results == None:
        return "NO_FACE"
    
    response = ""

    for result in results:
        response += str(result) + " "
    
    return response


def process_put(cmd):
    base64_str = cmd[1]
    fname = cmd[2]
    lname = ""

    if len(cmd) >= 4:
        lname = cmd[3]

    result = database.add_face(fname, lname, base64_str)

    if result == 0:
        return "SUCCESS"
    elif result == -1:
        return "NO_FACE"
    else:
        return "ERROR"

def process_command(cmd):
    try:
        command : str = cmd[0]
        if command.lower() == "get":
            return process_get(cmd)
        elif command.lower() == "put":
            return process_put(cmd)
        else:
            return "ERROR"
    except:
        return "ERROR"

def start_server(host='0.0.0.0', port=42069, reset=False):
    
    database.server_setup(reset)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))

    server_socket.listen(1)

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        query = receive_message(client_socket).split()

        try:
            if query[0] == "SHUTDOWN":
                break
        except:
            pass
        
        response = process_command(query)

        client_socket, client_address = server_socket.accept()
        
        client_socket.send(response.encode())

        client_socket.close()

start_server(reset=True)