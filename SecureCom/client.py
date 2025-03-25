import socket
import threading
from functions import*


# def receive_messages(client_socket):
#     while True:
#         try:
#             # Receive and print messages from the server
#             message = client_socket.recv(1024).decode('utf-8')
#             if (message == "handshake1"):
#             print(message)
#         except Exception as e:
#             print(f"Error: {e}")
#             break

def main():
    keytesting()
    # Set the server address and port
    host = '127.0.0.1'
    port = 5555

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((host, port))
    print(f"Connected to {host}:{port}")

    # Start a thread to receive messages from the server
    # receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    # receive_thread.start()

    # Send messages to the server
    while True:
        input("press any key to start")
        p = genP(128)
        a, b = genab(p)
        g = genG(a, b, p)
        E = genE(p)
        ka = genk(E)
        kag = pmultiply(g[0], g[1], ka, p, a, b)
        iv = iv_gen()
        # print(iv)
        # print(BitVector(hexstring="b2").get_bitvector_in_utf-8())
        # print(hexlisttostr(iv))
        message = str(p) + "," + str(a) + "," + str(b) + "," + str(g[0]) + "," + str(g[1]) + "," + str(kag[0]) + "," + str(kag[1]) + "," + hexlisttostr(iv)
        # print(message)
        client_socket.send(message.encode('utf-8'))
        try:
            # Receive and print messages from the server
            message = client_socket.recv(1024).decode('utf-8')
            slist = message.split(',')
            kbg = int(slist[0]), int(slist[1])
            kakbg = pmultiply(kbg[0], kbg[1], ka, p, a, b)
            key = format(kakbg[0], '032x')
            message = "okay"
            print("I am okay")
            client_socket.send(message.encode('utf-8'))
            message = client_socket.recv(1024).decode('utf-8')
            if (message == "okay"):
                print("Receiver is also okay")
                message = input("Enter Message to encrypt and send: ")
                res = ""
                strlist = CBC_encrypt(key=key, message=message, iv=iv)
                # print(" liiiiiiiiiiiiiiiiiiiiiiiiiiiiiii ")
                # print(strlist)
                # print("strrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr ")
                for i in range(0, len(strlist)):
                    if (i != 0):
                        res += ","
                    res += strlist[i]
                message = res
                client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Error: {e}")
            break

    # Close the connection when done
    client_socket.close()

if __name__ == "__main__":
    main()
