import re
import sys
from multiprocessing import Process
from tcp_server_single_process import TcpServer

HTML_ROOT_DIR = "./html"

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

    # response header
    def start_response(self, status, headers):
        server_headers = [
            ("Server", "My Server")
        ] + headers
        response_headers = "HTTP1.1" + status + "\r\n"
        for header in headers:
            response_headers += "{0}:{1}\r\n".format(header[0], header[1])
        self.response_headers = response_headers

    # client handler
    def tcp_worker(self, new_socket, client_addr):
        try:
            recv_data = new_socket.recv(1024)

            if len(recv_data) > 0:
                # parse the http request
                # please put your index.html file in the following directory

                req_headers = recv_data.decode("utf-8").splitlines()
                #print(req_headers)

                req_path = re.match(r"\w+ +(/[^ ]*)", req_headers[0]).group(1)
                http_method = re.match(r"[^\s]+", req_headers[0]).group(0)
                env = {
                    'method': http_method,
                }

                # handle the default path
                if req_path == "/":
                    req_path = "/index.html"
                req_file = HTML_ROOT_DIR + req_path


                if req_path.endswith(".py"):
                    module_name = req_path[1:-3]
                    try:
                        m = __import__(module_name)
                    except Exception:
                        self.start_response("404 Not Found", [])
                        res_body = "This module is not found!"
                    else:
                        res_body = m.application(env, self.start_response)
                else:
                    # look for the requested file
                    try:
                        with open(req_file, "rb") as f:
                            res_body = f.read().decode("utf-8")
                            self.start_response("200 OK", [])
                    except IOError:
                        self.start_response("404 Not Found", [])
                        res_body = "This page is not found!"

                # send the response (res_headers + res_body)
                print(res_body)
                res = self.response_headers + "\r\n" + res_body
                new_socket.send(bytes(res, "utf-8"))

            else:
                print("---main process: client disconnected: {}---".format(client_addr))
        finally:
            new_socket.close()


def main():
    sys.path.insert(1,"./wsgipython")
    new_server = WebServerStatic()
    new_server.start(7788)


if __name__ == "__main__":
    main()
