import socket
from threading import Thread, Lock
import time


def receive_messages(udp_socket):
    lock = Lock()
    while True:
        lock.acquire()
        data, client_address = udp_socket.recvfrom(1024)
        lock.release()
        if data.decode("utf-8") == "BYE":
            print(f"BYE received from {client_address}\nInput QUIT to quit")
            udp_socket.sendto("BYE".encode("utf-8"), client_address)
            break
        print(f"{client_address}: {data.decode('utf-8')}")
        time.sleep(2.0)


def main():
    server = (input("server ip: "), 1234)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto("hello".encode("utf-8"), server)
    thread_receive = Thread(target=lambda: receive_messages(s))
    thread_receive.start()
    while True:
        message = input("")
        if message == "QUIT":
            s.close()
            break
        lock = Lock()
        lock.acquire()
        s.sendto(message.encode("utf-8"), server)
        lock.release()



if __name__ == "__main__":
    main()
