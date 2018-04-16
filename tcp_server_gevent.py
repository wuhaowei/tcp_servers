import gevent
from gevent import socket, monkey

monkey.patch_all()

class TcpServer_coroutine():
    def __init__(self):
        pass
    
    def tcp_worker(self, new_socket, client_addr):
        try:
            while True:
                recv_data = new_socket.recv(1024)
                if len(recv_data) > 0:
                    print("{0}: {1}".format(client_addr, recv_data))
                else:
                    print(
                        "---main process: client disconnected: {}---".format(client_addr))
                    break
        finally:
            new_socket.close()
    
    def listen_loop(self, main_socket):
        print("---main process: wait for the next client...---")
        try:
            while True:
                new_socket, client_addr = main_socket.accept()
                print("---main process: client connected: {0}---".format(client_addr))
                gevent.spawn(self.tcp_worker, new_socket, client_addr)
        finally:
            main_socket.close()
            print("---main process: server shutdown---")
    
    def start(self, port):
        # initialzie main socket
        main_socket = socket.socket()
        main_socket.bind(("", port))
        main_socket.listen(5)
        self.listen_loop(main_socket)


def main():
    new_server = TcpServer_coroutine()
    new_server.start(7788)


if __name__ == "__main__":
    main()
