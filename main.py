import socket


def main():
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

  server_socket.bind(('localhost', 5000))
  server_socket.listen()

  while True:
    client_socket, address = server_socket.accept()
    print(f'User <{address[0]}:{address[1]}> connected!')

    while True:
      try:
        request = client_socket.recv(2048)
      except ConnectionResetError:
        request = None
        print(f'User <{address[0]}:{address[1]}> disconnected!')

      if request:
        response = f'Data {request.strip()} received successful!\n'
        client_socket.send(response.encode())
      else:
        break


if __name__ == '__main__':
  main()
