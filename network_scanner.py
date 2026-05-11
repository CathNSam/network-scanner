import socket
import argparse

parser = argparse.ArgumentParser(description="Simple Network Scanner")

parser.add_argument("target", help="Target IP address")
parser.add_argument("--ports", default="1-100", help="Port range example: 1-100")
parser.add_argument("--banner", action="store_true", help="Enable banner grabbing")

args = parser.parse_args()

target = args.target

try:
  start_port, end_port = map(int, args.ports.split("-"))
except:
  print("Invalid port range format. Use example: 1-100")
  exit()

print(f"\nScanning {target} from port {start_port} to {end_port}...\n")

for port in range(start_port, end_port + 1):

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  sock.settimeout(0.5)

  result = sock.connect_ex((target, port))

  if result == 0:

    try:
      service = socket.getservbyport(port)
    except:
      service = "Unknown"

    print(f"[OPEN] Port {port} - {service}")

    if args.banner:

      try:

        if port == 80 or port == 8080:

          sock.send(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")

        banner = sock.recv(1024).decode(errors="ignore").strip()

        if banner:
          print(f"   Banner: {banner[:100]}")

      except:
        pass

  sock.close()

print("\nScan completed.")