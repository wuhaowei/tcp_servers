from tcp_server_single_process import TcpServer

class TcpServer_non_blocking(TcpServer):
    def __init__(self):
        self.client_list = []
    
    def tcp_worker(self):
        pass

    def listen_loop(self, main_socket):
        # set main socket as non-blocking
        main_socket.setblocking(False)
        print("---server started...---")
        try:
            while True:
                # listen to new client
                try:
                    new_socket, client_addr = main_socket.accept()
                except:
                    # no new client then except
                    pass
                else:
                    # new client, so new socket will be created
                    print("---main process: client connected: {0}---".format(client_addr))
                    # set it as non-blocking as well
                    new_socket.setblocking(False)
                    # append it to the client list
                    self.client_list.append((new_socket, client_addr))

                # receive data from connected clients
                for socket_i, addr_i in self.client_list:
                    try:
                        recv_data = socket_i.recv(1024)
                    except:
                        pass
                    else:
                        if len(recv_data) > 0:
                            print("{0}: {1}".format(addr_i, recv_data))
                        else:
                            # receive empty data (client disconnected)
                            self.client_list.remove((socket_i, addr_i))
                            print("---main process: client disconnected: {}---".format(addr_i))
        except:
            main_socket.close()
            print("---main process: server shutdown---")


def main():
    new_server = TcpServer_non_blocking()
    new_server.start(7788)

if __name__ == "__main__":
    main()
