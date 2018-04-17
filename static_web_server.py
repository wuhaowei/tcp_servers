from multiprocessing import Process
from tcp_server_single_process import TcpServer
import re


class WebServerStatic(TcpServer):
    def __init__(self):
        pass

    # make it as a multi-processing server
    def listen_loop(self, main_socket):
        try:
            while True:
                print("---main process: wait for the next client...---")
                new_socket, client_addr = main_socket.accept()
                print("client connected: {0}---".format(client_addr))
                p = Process(target=self.tcp_worker, args=(new_socket, client_addr))
                p.start()
                new_socket.close()
        finally:
            main_socket.close()
            print("---main process: server shutdown---")

    # client handler
    def tcp_worker(self, new_socket, client_addr):
        try:
            recv_data = new_socket.recv(1024)

            if len(recv_data) > 0:
                # parse the http request
                # please put your index.html file in the following directory
                HTML_ROOT_DIR = "./html"
                first_line = recv_data.splitlines()[0].decode("utf-8")
                req_path = re.match(r"\w+ +(/[^ ]*)", first_line).group(1)
                if req_path == "/":
                    req_path = "/index.html"
                req_file = HTML_ROOT_DIR + req_path

                # look for the requested file
                try:
                    with open(req_file, "rb") as f:
                        res_body = f.read()
                        res_start_line = "HTTP/1.1 200 OK\r\n"
                        res_headers = "Server: My Server\r\n"
                        res = res_start_line + res_headers + "\r\n" +res_body.decode("utf-8")
                        new_socket.send(bytes(res, "utf-8"))
                except IOError:
                    res_start_line = "HTTP/1.1 404 Not Found\r\n"
                    res_headers = "Server: My Server\r\n"
                    res_body = "This page is not found!"
                    res = res_start_line + res_headers + "\r\n" + res_body
                    new_socket.send(bytes(res, "utf-8"))

            else:
                print("---main process: client disconnected: {}---".format(client_addr))
        finally:
            new_socket.close()


def main():
    new_server = WebServerStatic()
    new_server.start(7788)


if __name__ == "__main__":
    main()
