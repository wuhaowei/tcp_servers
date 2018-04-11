import select
from tcp_server_single_process import TcpServer

class TcpServer_select(TcpServer):

    def tcp_worker(self):
        pass
    
    def listen_loop(self, main_socket):
        
        socket_list = [main_socket,]

        print("---main process: wait for the next client...---")
        while True:
            # loop over list to get active sockets
            rlist, wlist, xlist = select.select(socket_list, [], [])
            
            # loop over active sockets
            for socket_i in rlist:
                # if main_socket, create new socket for client
                if socket_i == main_socket:
                    new_socket, client_addr = socket_i.accept()
                    socket_list.append(new_socket)
                    print("---main process: client connected: {0}---".format(client_addr))

                # or receive data from clients
                else:
                    recv_data = socket_i.recv(1024)
                    if len(recv_data) > 0:
                        print("{0}: {1}".format(socket_i.getsockname(), recv_data))
                    else:
                        print(
                            "---main process: client disconnected: {}---".format(socket_i.getsockname()))
                        socket_i.close()
                        socket_list.remove(socket_i)
                            

def main():
    new_server = TcpServer_select()
    new_server.start(7788)

if __name__ == "__main__":
    main()
