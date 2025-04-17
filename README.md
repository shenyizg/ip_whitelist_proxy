# IP Whitelist Forward Proxy

A lightweight TCP forward proxy with IP whitelist filtering, designed to work as a secure entry point for systems like Clash or other local proxy tools. Securely share Clash for Windows over LAN by exposing a proxy port with an external IP whitelist, allowing only your own devices (e.g., iPhone, MacBook) to use the service.

This proxy listens on a specified public port, checks whether the incoming client's IP is in an allowlist, and if permitted, forwards the traffic to an internal port (e.g., Clash HTTP proxy port).


## 🛠 How It Works

1. Listens on `LISTEN_PORT` (e.g., 10809)
2. Only allows IPs listed in `whitelist.txt`
3. Forwards all traffic to `FORWARD_PORT` (e.g., 7890 on localhost)

## 📦 Usage

### 1. Clone the repository

```bash
git clone https://github.com/shenyizg/ip-whitelist-proxy.git
cd ip-whitelist-proxy
```

### 2. Add your device IPs to whitelist.txt

Each line should contain one IP address:

```
192.168.1.5
192.168.1.10
```

### 3. Run the proxy

```bash
python ip_whitelist_proxy.py
```
Your trusted devices can now connect to your proxy via the entry port (e.g., 10809), and traffic will be forwarded to the internal service (e.g., Clash at 7890).

## ⚙ Configuration

Modify the following variables in ip_whitelist_proxy.py as needed:

```python
LISTEN_PORT = 10809       # Public entry port for your devices
FORWARD_PORT = 7890      # Internal port to forward to (e.g. Clash)
WHITELIST_FILE = 'whitelist.txt'  # List of allowed IPs
LOG_FILE = 'proxy.log'    # Output log file
```