import select
from tcp_server_single_process import TcpServer

class TcpServer_epoll(TcpServer):
    
    def tcp_worker(self):
        pass
    
    def listen_loop(self, main_socket):
        epoll = select.epoll()
        epoll.register(main_socket.fileno(), select.EPOLLIN | select.EPOLLET)
        socket_dict = {}
        print("---main process: server started...---")
        while True:
            epoll_list = epoll.poll()

            # loop over events
            for fd, events in epoll_list:
                # if main socket, then create new socket
                if fd == main_socket.fileno():
                    new_socket, client_addr = main_socket.accept()
                    print("---main process: client connected: {0}---".format(client_addr))
                    # save this socket in the dictionary: fd->socket
                    socket_dict[new_socket.fileno()] = new_socket
                    # register this socket into epoll
                    epoll.register(new_socket.fileno(), select.EPOLLIN | select.EPOLLET)
                # if client, receive data
                elif events == select.EPOLLIN:
                    this_socket = socket_dict[fd]
                    recv_data = this_socket.recv(1024)
                    # receive data
                    if len(recv_data) > 0:
                        print("{0}: {1}".format(this_socket.getsockname(), recv_data))
                    # empty data: disconnected
                    else:
                        print("---main process: client disconnected: {}---".format(this_socket.getsockname()))
                        # close the socket and remove it from epoll
                        this_socket.close()
                        epoll.unregister(fd)


def main():
    new_server = TcpServer_epoll()
    new_server.start(7788)

if __name__ == "__main__":
    main()