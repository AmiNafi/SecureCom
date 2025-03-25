import socket
import threading
from functions import*
def handle_client(client_socket):
    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(1024).decode('utf-8')
            datalist = data.split(',')
            # print(datalist)
            p = int(datalist[0])
            
            a = int(datalist[1])
            b = int (datalist[2])
            g = [0, 0]
            g[0] = int(datalist[3])
            g[1] = int(datalist[4])
            E = genE(p)
            kb = genk(E)
            kbg = pmultiply(g[0], g[1], kb, p, a, b)
            kag = [0, 0]
            kag[0] = int(datalist[5])
            # print("=======================================")
            # print(kag[0])
            kag[1] = int(datalist[6])
            iv = strtohexlist(datalist[7])
            # print(iv)
            kakbg = pmultiply(kag[0], kag[1], kb, p, a, b)
            # print("kakbg====================== ", kakbg)
            key = format(kakbg[0], '032x')
            # print("key ============ here ")
            message = str(kbg[0]) + "," + str(kbg[1])
            # print("nex message = ", message)
            client_socket.send(message.encode('utf-8'))
            message = client_socket.recv(1024).decode('utf-8')
            if (message == "okay"):
                print("Sender sends okay and I am also okay")
                client_socket.send(message.encode('utf-8'))
                message = client_socket.recv(1024).decode('utf-8')
                messagelist = message.split(',')
                # print("encrypted everything + ", messagelist)
                messagelist = CBC_decrypt(key, messagelist, iv)
                message = ""
                for m in messagelist:
                    message += m
                print(message)
        except Exception as e:
            print(f"Error: {e}")
            break

    # Close the connection when the client disconnects
    client_socket.close()

def main():
    # Set the server address and port
    host = '127.0.0.1'
    port = 5555

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    # Accept a connection from a client
    client_socket, addr = server_socket.accept()
    print(f"Accepted connection from {addr}")
    handle_client(client_socket=client_socket)
    # Start a new thread to handle the client
    # client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    # client_handler.start()

if __name__ == "__main__":
    main()
