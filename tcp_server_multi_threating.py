import threading
from tcp_server_single_process import TcpServer

class TcpServer_multi_threading(TcpServer):
    def __init__(self):
        self.case_num = 0

    def listen_loop(self, main_socket):
        try:
            while True:
                print("---main process: wait for the next client...---")
                new_socket, client_addr = main_socket.accept()
                self.case_num += 1
                print("---case<{1}>: client connected: {0}---".format(client_addr, self.case_num))
                t = threading.Thread(target=self.tcp_worker, args=(new_socket, client_addr))
                t.start()
        finally:
            main_socket.close()
            print("---main process: server shutdown---")


def main():
    new_server = TcpServer_multi_threading()
    new_server.start(7788)

if __name__ == "__main__":
    main()
