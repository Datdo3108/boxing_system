import socket

HOST = '0.0.0.0'  # Listen on all available network interfaces
PORT = 1234

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Server listening on {HOST}:{PORT}")

    conn, addr = server_socket.accept()
    # with conn:
    print("Connected by", addr)
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print("Received data:", data.decode())
