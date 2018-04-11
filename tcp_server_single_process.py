import socket

class TcpServer():
    def __init__(self):
        pass

    def start(self, port):
        # initialzie main socket
        main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        main_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        main_addr = ("", port)
        main_socket.bind(main_addr)
        main_socket.listen(5)
        self.listen_loop(main_socket)

    def listen_loop(self, main_socket):
        try:
            while True:
                print("---main process: wait for the next client...---")
                new_socket, client_addr = main_socket.accept()
                print("---main process: client connected: {0}---".format(client_addr))
                self.tcp_worker(new_socket, client_addr)
        finally:
            print("---main process: server shutdown---")
            main_socket.close()

    def tcp_worker(self, new_socket, client_addr):
        try:
            while True:
                recv_data = new_socket.recv(1024)
                if len(recv_data) > 0:
                    print("{0}: {1}".format(client_addr, recv_data))
                else:
                    print("---main process: client disconnected: {}---".format(client_addr))
                    break
        finally:
            new_socket.close()


def main():
    new_server = TcpServer()
    new_server.start(7788)

if __name__ == "__main__":
    main()
