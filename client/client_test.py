from PIL import Image

import socket
import base64
import io
import os

def base64_encode(path):
    with open(path, "rb") as file:
        base64_str = base64.b64encode(file.read()).decode("utf-8")
    return base64_str

host = 'localhost'
port = 42069

def shutdown():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    client.send("SHUTDOWN".encode())
    client.close()

def send_put(path, fname, lname):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    send = f"PUT {base64_encode(path)} {fname} {lname}"
    client.send(send.encode())
    client.close()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    response = client.recv(1024)
    client.close()

    return response

def send_get(path, fname):

    print(f"Testing {fname}")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    send = f"GET {base64_encode(path)}"
    client.send(send.encode())
    client.close()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    response = client.recv(1024).decode()
    client.close()
    print(response)
    

def send_array(path, pics, fname, lname):
    for name in pics:
        print(send_put(path + name, fname, lname).decode())

anik_dir = "images/Anik/"
caleb_dir = "images/Caleb/"
vivek_dir = "images/Vivek/"

anik_pics = os.listdir(anik_dir)
caleb_pics = os.listdir(caleb_dir)
vivek_pics = os.listdir(vivek_dir)

anik_put = anik_pics[:-3]
caleb_put = caleb_pics[:-3]
vivek_put = vivek_pics[:-3]

anik_test = anik_pics[-1]
caleb_test = caleb_pics[-1]
vivek_test = vivek_pics[-1]

send_array(anik_dir, anik_pics, 'Anik', 'Patel')
send_array(caleb_dir, caleb_pics, 'Caleb', 'Devon')
send_array(vivek_dir, vivek_pics, 'Vivek', 'Keval')

# send_get(anik_dir + anik_test, 'Anik')
# send_get(caleb_dir + caleb_test, 'Caleb')
# send_get(vivek_dir + vivek_test, 'Vivek')

# shutdown()

