import select
import socket

MONITOR = []


def accept_connection(server_socket):
  client_socket, address = server_socket.accept()
  print(f'Connected from: {address}')
  global MONITOR
  MONITOR.append(client_socket)


def send_message(client_socket):
  try:
    client_socket.send('Hello World!\n'.encode()) if client_socket.recv(2048) else client_socket.close()
  except ConnectionResetError:
    client_socket.close()


def event_loop(server_socket):
  while True:
    try:
      ready_to_read, _, _ = select.select(MONITOR, [], [])

      for sock in ready_to_read:
        accept_connection(sock) if sock is server_socket else send_message(sock)

    except ValueError:
      MONITOR.pop()


def create_server_socket():
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
  server_socket.bind(('localhost', 5000))
  server_socket.listen()

  return server_socket


if __name__ == '__main__':
  sock = create_server_socket()
  MONITOR.append(sock)
  event_loop(sock)
