import socket
import threading
import logging
from datetime import datetime

# Configuration
LISTEN_HOST = '0.0.0.0'         # Proxy listen address
LISTEN_PORT = 10809             # Public entry port (used by clients)
FORWARD_HOST = '127.0.0.1'      # Internal forward target (e.g., Clash)
FORWARD_PORT = 7890             # Internal proxy port to forward traffic to

WHITELIST_FILE = 'whitelist.txt'
LOG_FILE = 'proxy.log'
BUFFER_SIZE = 8192

# Initialize logger
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log(msg):
    print(msg)
    logging.info(msg)

def load_whitelist():
    """Load allowed IP addresses from whitelist.txt"""
    try:
        with open(WHITELIST_FILE, 'r') as f:
            whitelist = {line.strip() for line in f if line.strip()}
        return whitelist
    except FileNotFoundError:
        log(f"[!] Whitelist file '{WHITELIST_FILE}' not found.")
        return set()

def handle_client(client_socket, client_address):
    """Check whitelist and forward traffic if allowed"""
    ip = client_address[0]
    whitelist = load_whitelist()

    log(f"[+] Incoming connection from {ip}")

    if ip not in whitelist:
        log(f"[-] {ip} is not in the whitelist. Connection rejected.")
        client_socket.close()
        return

    try:
        forward_socket = socket.create_connection((FORWARD_HOST, FORWARD_PORT))
    except Exception as e:
        log(f"[!] Failed to connect to internal proxy: {e}")
        client_socket.close()
        return

    # Bi-directional forwarding
    def forward(src, dst):
        try:
            while True:
                data = src.recv(BUFFER_SIZE)
                if not data:
                    break
                dst.sendall(data)
        except:
            pass
        finally:
            src.close()
            dst.close()

    threading.Thread(target=forward, args=(client_socket, forward_socket), daemon=True).start()
    threading.Thread(target=forward, args=(forward_socket, client_socket), daemon=True).start()

def start_server():
    log(f"🚀 Proxy started on port {LISTEN_PORT}, forwarding to {FORWARD_PORT}")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((LISTEN_HOST, LISTEN_PORT))
    server.listen(100)

    try:
        while True:
            client_sock, addr = server.accept()
            threading.Thread(target=handle_client, args=(client_sock, addr), daemon=True).start()
    except KeyboardInterrupt:
        log("🔌 Server manually stopped.")
    finally:
        server.close()

if __name__ == '__main__':
    start_server()
